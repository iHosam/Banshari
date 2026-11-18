"""
Search Engine & Facet Aggregation Engine
Supports dual-mode queries (part number vs automotive synonym fulltext),
VIN fitment verification, faceted filters, and landed cost enrichment.
"""

from typing import List, Dict, Any, Optional
from ..schemas.unified_part import UnifiedPartListing, ListingType, ItemCondition, AuthenticityTier, HazmatClass
from ..schemas.search import (
    SearchFilters, VehicleGarageFilter, EnrichedPartListing,
    FacetsDistribution, FacetCount, SearchQueryMetadata, SearchResponse
)
from .normalizer import PartNormalizer
from .query_parser import QueryParser
from .logistics import LogisticsEngine
from .federated_aggregator import FederatedAggregator
from ..data.mock_catalog import MOCK_CATALOG

class SearchEngine:
    def __init__(self, catalog: Optional[List[UnifiedPartListing]] = None):
        self.catalog = catalog or MOCK_CATALOG

    def _matches_vehicle(self, listing: UnifiedPartListing, garage: VehicleGarageFilter) -> bool:
        """Verifies vehicle fitment based on ACES 5.0 Year/Make/Model/Engine"""
        if not garage.make and not garage.model and not garage.year:
            return True

        for fit in listing.aces_fitments:
            make_match = not garage.make or garage.make.lower() in fit.make_name.lower()
            model_match = not garage.model or garage.model.lower() in fit.model_name.lower()
            year_match = True
            if garage.year:
                year_match = fit.year_start <= garage.year <= fit.year_end

            if make_match and model_match and year_match:
                return True
        return False

    def _matches_shipping(self, listing: UnifiedPartListing, country: str, only_direct: bool) -> bool:
        """Verifies if seller ships to user country or freight forwarding is eligible"""
        country_code = country.upper()
        if listing.shipping.ships_worldwide:
            return True
        if country_code in listing.shipping.ships_to:
            return True
        if not only_direct and listing.shipping.freight_forwarder_permitted:
            return True
        return False

    def search(
        self,
        query: str = "",
        filters: Optional[SearchFilters] = None,
        garage: Optional[VehicleGarageFilter] = None,
        currency: Optional[str] = None,
        search_mode: str = "auto"
    ) -> SearchResponse:
        filters = filters or SearchFilters()
        garage = garage or VehicleGarageFilter()
        user_country = filters.destination_country.upper()

        # Step 1: Query Parsing & Detection
        detected_mode, clean_pn, synonyms, vin_data = QueryParser.parse_query(query, search_mode=search_mode)
        interchange_set = PartNormalizer.get_interchange_numbers(clean_pn) if clean_pn else set()

        # If VIN decoded, auto-enrich vehicle garage
        if vin_data and not garage.make:
            garage.make = vin_data.get("make")
            garage.year = vin_data.get("model_year")

        # Step 2: Candidate Matching
        matched_candidates: List[UnifiedPartListing] = []

        import re

        def _norm_token_str(s: str) -> str:
            t = s.lower()
            t = re.sub(r'\biii\b', '3', t)
            t = re.sub(r'\biv\b', '4', t)
            t = re.sub(r'\bii\b', '2', t)
            t = re.sub(r'\bcrfp\b', 'cfrp', t)
            t = re.sub(r'\bsiliva\b', 'silvia', t)
            t = re.sub(r'\bslivia\b', 'silvia', t)
            t = re.sub(r'\bsilva\b', 'silvia', t)
            t = re.sub(r'\bsklyine\b', 'skyline', t)
            t = re.sub(r'\bskiline\b', 'skyline', t)
            t = re.sub(r'\bmaita\b', 'miata', t)
            t = re.sub(r'\bciviv\b', 'civic', t)
            return t

        for item in self.catalog:
            # Check Hazmat filter
            if filters.exclude_hazmat and item.shipping.hazmat_class in [HazmatClass.CLASS_1_EXPLOSIVE, HazmatClass.CLASS_9_LITHIUM]:
                continue

            # Shipping filter
            if not self._matches_shipping(item, user_country, filters.only_direct_shipping):
                continue

            # Text / Part Number / VIN Matching
            matches_query = False
            if not query.strip():
                matches_query = True
            elif detected_mode == "vin":
                # Matches if part fits decoded VIN vehicle
                matches_query = self._matches_vehicle(item, garage)
            elif detected_mode == "part_number":
                # Exact or Interchange OEM match
                item_clean = item.clean_part_number
                item_interchanges = {PartNormalizer.clean(ic) for ic in item.interchange_part_numbers}
                if (clean_pn == item_clean or 
                    clean_pn in item_interchanges or 
                    any(ic in interchange_set for ic in item_interchanges.union({item_clean}))):
                    matches_query = True
                elif clean_pn in item_clean:
                    matches_query = True
            else:
                # Keyword search with automotive synonym expansion & token matching
                fits_str = " ".join(f"{f.make_name} {f.model_name} {f.submodel_name or ''}" for f in item.aces_fitments)
                item_text_raw = f"{item.title} {item.brand} {item.part_type} {item.clean_part_number} {fits_str}"
                item_text = _norm_token_str(item_text_raw)
                q_norm = _norm_token_str(query)
                q_words = [w for w in q_norm.split() if len(w) > 1 and w not in ["with", "for", "the", "and", "in", "of"]]

                # 1. Exact phrase match
                if q_norm in item_text:
                    matches_query = True
                elif len(q_words) == 1:
                    # Single word query (e.g. "airbag", "caliper", "bride")
                    search_terms = synonyms if synonyms else [q_words[0]]
                    if any(_norm_token_str(term) in item_text for term in search_terms):
                        matches_query = True
                elif q_words:
                    # Multi-word query: all key query tokens must be matched
                    if all(w in item_text for w in q_words):
                        matches_query = True
                    else:
                        all_tokens_matched = True
                        for w in q_words:
                            token_synonyms = QueryParser.expand_synonyms(w)
                            if not any(_norm_token_str(ts) in item_text for ts in token_synonyms):
                                all_tokens_matched = False
                                break
                        if all_tokens_matched:
                            matches_query = True

            if matches_query:
                matched_candidates.append(item)

        # Step 2b: Federated Live Multi-Platform Search Aggregation
        # If catalog matching yielded 0 or few results for an active query,
        # query/synthesize candidates across the 14 global platforms dynamically
        if len(matched_candidates) < 4 and query.strip():
            fed_listings = FederatedAggregator.aggregate_for_query(
                query=query,
                detected_mode=detected_mode,
                clean_pn=clean_pn,
                destination_country=user_country
            )
            existing_platforms = {m.source_platform for m in matched_candidates}
            for fed_item in fed_listings:
                if filters.exclude_hazmat and fed_item.shipping.hazmat_class in [HazmatClass.CLASS_1_EXPLOSIVE, HazmatClass.CLASS_9_LITHIUM]:
                    continue
                if not self._matches_shipping(fed_item, user_country, filters.only_direct_shipping):
                    continue
                if fed_item.source_platform not in existing_platforms or len(matched_candidates) == 0:
                    matched_candidates.append(fed_item)

        # Step 3: Compute Facets Distribution on candidate set before selective filter narrowing
        facets = self._compute_facets(matched_candidates)

        # Step 4: Apply Faceted Filters
        filtered_results: List[UnifiedPartListing] = []
        for item in matched_candidates:
            # Listing Type filter
            if filters.listing_types and item.listing_type not in filters.listing_types:
                continue
            # Condition filter
            if filters.conditions and item.condition not in filters.conditions:
                continue
            # Authenticity tier filter
            if filters.authenticity_tiers and item.authenticity_tier not in filters.authenticity_tiers:
                continue
            # Source filter
            if filters.sources and item.source_platform not in filters.sources:
                continue

            filtered_results.append(item)

        # Step 5: Enrich with Landed Cost & Vehicle Fitment Verification
        enriched_results: List[EnrichedPartListing] = []
        for item in filtered_results:
            price = item.buy_now_price if item.listing_type == ListingType.BUY_NOW else (item.current_bid or 50.0)
            landed = LogisticsEngine.calculate_landed_cost(
                item_price_usd=price,
                weight_kg=item.pies_attributes.weight_kg,
                destination_country=user_country,
                preferred_currency=currency,
                hazmat_class=item.shipping.hazmat_class
            )

            # Check garage fitment
            fitment_ok = self._matches_vehicle(item, garage) if (garage.make or garage.model or garage.year) else False
            fitment_note = None
            if fitment_ok:
                fitment_note = f"Verified fit for {garage.year or ''} {garage.make or ''} {garage.model or ''}".strip()

            enriched_results.append(
                EnrichedPartListing(
                    listing=item,
                    landed_cost=landed,
                    fitment_verified=fitment_ok,
                    fitment_notes=fitment_note
                )
            )

        # Sort: Auctions ending soonest or lowest total landed cost
        enriched_results.sort(key=lambda r: (
            0 if r.listing.listing_type == ListingType.AUCTION else 1,
            r.landed_cost.total_landed_cost_usd
        ))

        active_currency = currency if currency in LogisticsEngine.EXCHANGE_RATES else LogisticsEngine.COUNTRY_TARIFFS.get(user_country, {}).get("currency", "USD")

        return SearchResponse(
            query_meta=SearchQueryMetadata(
                raw_query=query,
                detected_mode=detected_mode,
                cleaned_part_number=clean_pn,
                expanded_synonyms=synonyms,
                decoded_vin=vin_data
            ),
            total_matches=len(matched_candidates),
            returned_count=len(enriched_results),
            selected_currency=active_currency,
            destination_country=user_country,
            facets=facets,
            results=enriched_results
        )

    def _compute_facets(self, listings: List[UnifiedPartListing]) -> FacetsDistribution:
        """Aggregates counts for each faceted filter dimension"""
        lt_counts: Dict[str, int] = {}
        cond_counts: Dict[str, int] = {}
        tier_counts: Dict[str, int] = {}
        src_counts: Dict[str, int] = {}
        brand_counts: Dict[str, int] = {}

        for item in listings:
            lt_counts[item.listing_type.value] = lt_counts.get(item.listing_type.value, 0) + 1
            cond_counts[item.condition.value] = cond_counts.get(item.condition.value, 0) + 1
            tier_counts[item.authenticity_tier.value] = tier_counts.get(item.authenticity_tier.value, 0) + 1
            src_counts[item.source_platform] = src_counts.get(item.source_platform, 0) + 1
            brand_counts[item.brand] = brand_counts.get(item.brand, 0) + 1

        def to_facet_list(d: Dict[str, int]) -> List[FacetCount]:
            return [FacetCount(key=k, count=v, label=k.replace("_", " ").title()) for k, v in d.items()]

        return FacetsDistribution(
            listing_types=to_facet_list(lt_counts),
            conditions=to_facet_list(cond_counts),
            authenticity_tiers=to_facet_list(tier_counts),
            sources=to_facet_list(src_counts),
            brands=to_facet_list(brand_counts)
        )

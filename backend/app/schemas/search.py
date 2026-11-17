"""
Search and Filter Request / Response Schemas
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from .unified_part import ListingType, ItemCondition, AuthenticityTier, UnifiedPartListing


class VehicleGarageFilter(BaseModel):
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    engine: Optional[str] = None
    vin: Optional[str] = None


class SearchFilters(BaseModel):
    listing_types: Optional[List[ListingType]] = None
    conditions: Optional[List[ItemCondition]] = None
    authenticity_tiers: Optional[List[AuthenticityTier]] = None
    sources: Optional[List[str]] = None
    destination_country: str = "SA"  # ISO 3166-1 alpha-2, e.g. SA, US, AE, DE, GB
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    only_direct_shipping: bool = False
    exclude_hazmat: bool = False


class LandedCostEstimate(BaseModel):
    item_price_usd: float
    shipping_usd: float
    duty_rate_percent: float
    customs_duty_usd: float
    tax_vat_percent: float
    tax_vat_usd: float
    total_landed_cost_usd: float
    local_currency_code: str
    exchange_rate: float
    total_landed_cost_local: float
    hazmat_warning: Optional[str] = None
    air_courier_eligible: bool = True


class EnrichedPartListing(BaseModel):
    listing: UnifiedPartListing
    landed_cost: LandedCostEstimate
    fitment_verified: bool = False
    fitment_notes: Optional[str] = None


class FacetCount(BaseModel):
    key: str
    count: int
    label: str


class FacetsDistribution(BaseModel):
    listing_types: List[FacetCount]
    conditions: List[FacetCount]
    authenticity_tiers: List[FacetCount]
    sources: List[FacetCount]
    brands: List[FacetCount]


class SearchQueryMetadata(BaseModel):
    raw_query: str
    detected_mode: str  # "part_number", "vin", "fulltext_keyword"
    cleaned_part_number: Optional[str] = None
    expanded_synonyms: List[str] = []
    decoded_vin: Optional[Dict[str, Any]] = None


class SearchResponse(BaseModel):
    query_meta: SearchQueryMetadata
    total_matches: int
    returned_count: int
    selected_currency: str
    destination_country: str
    facets: FacetsDistribution
    results: List[EnrichedPartListing]

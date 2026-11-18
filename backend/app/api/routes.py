"""
Banshari REST API Routes
"""

from fastapi import APIRouter, Query
from typing import Optional, List
from ..schemas.search import (
    SearchResponse, SearchFilters, VehicleGarageFilter, LandedCostEstimate
)
from ..schemas.unified_part import ListingType, ItemCondition, AuthenticityTier, HazmatClass
from ..engine.search_engine import SearchEngine
from ..engine.query_parser import QueryParser
from ..engine.normalizer import PartNormalizer
from ..engine.logistics import LogisticsEngine

router = APIRouter(prefix="/api")
engine = SearchEngine()

@router.get("/health")
def health():
    return {
        "status": "healthy",
        "app": "Banshari Global Automotive Metasearch",
        "version": "1.0.2",
        "standards": ["ACES 5.0", "PIES 8.0", "TecDoc", "ISO 3779", "HS 8708"]
    }

@router.post("/search", response_model=SearchResponse)
def post_search(
    query: str = "",
    filters: Optional[SearchFilters] = None,
    garage: Optional[VehicleGarageFilter] = None,
    currency: Optional[str] = None,
    mode: str = "auto"
):
    return engine.search(query=query, filters=filters, garage=garage, currency=currency, search_mode=mode)

@router.get("/search", response_model=SearchResponse)
def get_search(
    q: str = Query("", description="Search term, OEM Part Number, or VIN"),
    country: str = Query("SA", description="Destination Country ISO alpha-2"),
    currency: Optional[str] = Query(None, description="Preferred display currency"),
    mode: str = Query("auto", description="Search mode: auto, pn, text/keyword"),
    listing_type: Optional[List[ListingType]] = Query(None),
    condition: Optional[List[ItemCondition]] = Query(None),
    tier: Optional[List[AuthenticityTier]] = Query(None),
    source: Optional[List[str]] = Query(None),
    year: Optional[int] = Query(None),
    make: Optional[str] = Query(None),
    model: Optional[str] = Query(None),
    exclude_hazmat: bool = Query(False)
):
    filters = SearchFilters(
        destination_country=country,
        listing_types=listing_type,
        conditions=condition,
        authenticity_tiers=tier,
        sources=source,
        exclude_hazmat=exclude_hazmat
    )
    garage = VehicleGarageFilter(year=year, make=make, model=model)
    return engine.search(query=q, filters=filters, garage=garage, currency=currency, search_mode=mode)

@router.get("/vin/{vin}")
def decode_vin(vin: str):
    res = QueryParser.decode_vin(vin)
    if not res:
        return {"is_valid": False, "message": "Invalid 17-character VIN"}
    return res

@router.get("/interchange/{part_number}")
def get_interchange(part_number: str):
    cleaned = PartNormalizer.clean(part_number)
    interchanges = PartNormalizer.get_interchange_numbers(cleaned)
    return {
        "input": part_number,
        "clean_part_number": cleaned,
        "interchange_numbers": sorted(list(interchanges))
    }

@router.get("/landed-cost", response_model=LandedCostEstimate)
def estimate_landed_cost(
    price: float = Query(..., description="Item price in USD"),
    weight: float = Query(1.0, description="Weight in KG"),
    country: str = Query("SA", description="Destination country ISO alpha-2"),
    currency: Optional[str] = Query(None),
    hazmat: HazmatClass = Query(HazmatClass.NONE)
):
    return LogisticsEngine.calculate_landed_cost(
        item_price_usd=price,
        weight_kg=weight,
        destination_country=country,
        preferred_currency=currency,
        hazmat_class=hazmat
    )

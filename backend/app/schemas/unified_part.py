"""
Banshari Unified Part Data Model
Adheres to:
 - ACES 5.0 (Aftermarket Catalog Exchange Standard via VCdb / PCdb)
 - PIES 8.0 (Product Information Exchange Standard)
 - TecDoc (K-Type / N-Type)
 - Schema.org/Product & Schema.org/Offer
"""

from typing import List, Optional, Dict, Any
from enum import Enum
from pydantic import BaseModel, Field
from datetime import datetime


class ListingType(str, Enum):
    BUY_NOW = "buy_now"
    AUCTION = "auction"


class ItemCondition(str, Enum):
    NEW_SEALED = "new_factory_sealed"
    NEW_REMANUFACTURED = "new_remanufactured"
    USED_GRADE_A = "used_grade_a"      # Minor wear, fully functional
    USED_GRADE_B = "used_grade_b"      # Moderate wear, inspected
    USED_GRADE_C = "used_grade_c"      # Salvage core / heavy wear


class AuthenticityTier(str, Enum):
    OEM_GENUINE = "oem_genuine"
    OES_TIER1 = "oes_tier1"                   # e.g., Bosch, Brembo, Denso, Lemförder
    AFTERMARKET_PERF = "aftermarket_performance" # e.g., Bilstein, Akebono, K&N
    AFTERMARKET_VALUE = "aftermarket_economy"     # e.g., Dorman, Meyle, Febi


class HazmatClass(str, Enum):
    NONE = "none"
    CLASS_1_EXPLOSIVE = "class_1_airbag_pyrotechnic" # SRS inflators
    CLASS_2_GAS = "class_2_pressurized_gas"         # Gas shock absorbers / struts
    CLASS_9_LITHIUM = "class_9_lithium_battery"     # Hybrid / EV traction or auxiliary
    CLASS_3_FLAMMABLE = "class_3_flammable_liquid"  # Brake fluid, oils


# --- ACES 5.0 Vehicle Fitment (VCdb / PCdb) ---
class ACESFitment(BaseModel):
    base_vehicle_id: Optional[int] = Field(None, description="VCdb BaseVehicleID")
    make_name: str
    model_name: str
    year_start: int
    year_end: int
    submodel_name: Optional[str] = None
    engine_base_id: Optional[int] = Field(None, description="VCdb EngineBaseID (e.g., 3.0L L6 Turbo)")
    engine_description: Optional[str] = None
    pcdb_part_terminology_id: Optional[int] = Field(None, description="PCdb PartTerminologyID (e.g. 1896 for Brake Rotor)")
    pcdb_position: Optional[str] = Field("Front", description="Mounting position e.g., Front Left, Rear")
    notes: Optional[str] = None


# --- TecDoc Standard (European/Asian Catalogs) ---
class TecDocFitment(BaseModel):
    k_type: Optional[int] = Field(None, description="TecDoc K-Type passenger vehicle ID")
    n_type: Optional[int] = Field(None, description="TecDoc N-Type commercial vehicle ID")
    generic_article_id: Optional[int] = Field(None, description="TecDoc Generic Article Number")
    article_number: Optional[str] = None


# --- PIES 8.0 Product Attributes ---
class PIESAttributes(BaseModel):
    weight_kg: float = 1.0
    dimensions_cm: Dict[str, float] = Field(
        default_factory=lambda: {"length": 25.0, "width": 25.0, "height": 10.0}
    )
    material: Optional[str] = None
    country_of_origin: Optional[str] = "DE" # ISO 3166-1 alpha-2
    warranty_months: Optional[int] = 24
    unspc_code: Optional[str] = None


# --- Shipping & Landed Cost Compliance ---
class ShippingCompliance(BaseModel):
    hs_code: str = Field("8708.30.00", description="Harmonized Tariff Code (Chapter 8708 for Auto Parts)")
    hazmat_class: HazmatClass = HazmatClass.NONE
    air_freight_restricted: bool = False
    ships_to: List[str] = Field(
        default_factory=lambda: ["US", "CA", "GB", "DE", "FR", "JP", "SA", "AE", "QA", "KW", "OM", "BH", "AU"],
        description="ISO 3166-1 alpha-2 countries seller directly ships to"
    )
    ships_worldwide: bool = True
    freight_forwarder_permitted: bool = True
    base_shipping_cost_usd: float = 25.00


# --- Unified Normalized Part Listing Schema ---
class UnifiedPartListing(BaseModel):
    id: str = Field(..., description="Unique listing identifier across platforms")
    source_platform: str = Field(..., description="Source: ebay_motors, rockauto, partsouq, autodoc, yahoo_auctions, car_part")
    source_listing_id: str
    source_url: str
    source_logo_url: Optional[str] = None

    # Title & Branding
    title: str
    brand: str
    manufacturer_part_number: str
    clean_part_number: str = Field(..., description="Normalized alphanumeric only part number (uppercase, no punctuation)")
    interchange_part_numbers: List[str] = Field(default_factory=list, description="Equivalent OEM / OES / Aftermarket part numbers")

    # Images
    primary_image_url: str
    additional_image_urls: List[str] = Field(default_factory=list)

    # Classification & Fitment
    part_type: str = Field(..., description="Standardized part name (e.g. Brake Rotor, Fuel Injector)")
    aces_fitments: List[ACESFitment] = Field(default_factory=list)
    tecdoc_fitments: List[TecDocFitment] = Field(default_factory=list)
    pies_attributes: PIESAttributes = Field(default_factory=PIESAttributes)

    # Commercial & Auction Details
    listing_type: ListingType
    condition: ItemCondition
    authenticity_tier: AuthenticityTier

    # Pricing & Currencies
    currency: str = "USD"
    buy_now_price: Optional[float] = None
    current_bid: Optional[float] = None
    bid_count: Optional[int] = None
    auction_end_time: Optional[datetime] = None

    # Seller & Location
    seller_name: str
    seller_rating: float = 4.8
    seller_country: str = "US" # ISO 3166-1 alpha-2

    # Logistics
    shipping: ShippingCompliance = Field(default_factory=ShippingCompliance)

    # SEO Structured Data
    def to_schema_org_json(self) -> Dict[str, Any]:
        """Generate Schema.org/Product and Offer structured JSON-LD"""
        price = self.buy_now_price if self.listing_type == ListingType.BUY_NOW else self.current_bid
        return {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": self.title,
            "image": [self.primary_image_url],
            "description": f"{self.authenticity_tier.value} {self.part_type} for {self.brand}. MPN: {self.clean_part_number}",
            "sku": self.clean_part_number,
            "mpn": self.manufacturer_part_number,
            "brand": {
                "@type": "Brand",
                "name": self.brand
            },
            "offers": {
                "@type": "Offer",
                "url": self.source_url,
                "priceCurrency": self.currency,
                "price": price,
                "itemCondition": "https://schema.org/NewCondition" if "new" in self.condition.value else "https://schema.org/UsedCondition",
                "availability": "https://schema.org/InStock",
                "seller": {
                    "@type": "Organization",
                    "name": self.seller_name
                }
            }
        }

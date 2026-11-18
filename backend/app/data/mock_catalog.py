"""
Realistic Mock Aggregated Auto Parts Catalog
Contains listings across eBay Motors, RockAuto, Partsouq, AutoDoc, Yahoo! Japan, and Car-Part.com
"""

from datetime import datetime, timedelta, timezone
from typing import List
from ..schemas.unified_part import (
    UnifiedPartListing, ListingType, ItemCondition, AuthenticityTier,
    ACESFitment, TecDocFitment, PIESAttributes, ShippingCompliance, HazmatClass
)
from ..engine.deep_linker import DeepLinker

now = datetime.now(timezone.utc)

MOCK_CATALOG: List[UnifiedPartListing] = [
    # 1. BMW F30 / G20 Front Brake Rotor (OEM Genuine - Partsouq)
    UnifiedPartListing(
        id="ps-bmw-34116792223",
        source_platform="Partsouq",
        source_listing_id="PS-7889102",
        source_url="https://partsouq.com/en/search/all?q=34116792223",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="BMW Genuine Front Brake Disc Rotor 340x30mm (OEM)",
        brand="BMW Genuine",
        manufacturer_part_number="34-11-6-792-223",
        clean_part_number="34116792223",
        interchange_part_numbers=["09C39913", "150348320", "55523", "DF6603S", "34116855006"],
        primary_image_url="https://images.unsplash.com/photo-1600790142055-619df03207e6?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="330i",
                year_start=2016,
                year_end=2024,
                submodel_name="M Sport",
                engine_base_id=2034,
                engine_description="2.0L L4 Turbo B48",
                pcdb_part_terminology_id=1896,
                pcdb_position="Front Axle Both Sides",
                notes="M-Sport Brake Package S2NHA"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82, article_number="34116792223")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=9.8,
            dimensions_cm={"length": 34.0, "width": 34.0, "height": 7.3},
            material="High Carbon Cast Iron / Aluminum Hat",
            country_of_origin="DE",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=178.50,
        seller_name="Partsouq Direct Middle East",
        seller_rating=4.9,
        seller_country="AE",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            air_freight_restricted=False,
            ships_to=["US", "SA", "AE", "GB", "DE", "KW", "QA", "OM"],
            ships_worldwide=True,
            base_shipping_cost_usd=38.00
        )
    ),

    # 2. BMW Front Brake Rotor - Brembo Aftermarket Performance (RockAuto)
    UnifiedPartListing(
        id="ra-brembo-09c39913",
        source_platform="RockAuto",
        source_listing_id="RA-BRM-09C39913",
        source_url="https://www.rockauto.com/en/parts/brembo,09C39913,rotor,1896",
        source_logo_url="https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=100&h=100&fit=crop",
        title="Brembo Prime Coated High Carbon Front Brake Rotor",
        brand="Brembo",
        manufacturer_part_number="09.C399.13",
        clean_part_number="09C39913",
        interchange_part_numbers=["34116792223", "150348320", "55523"],
        primary_image_url="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="330i",
                year_start=2016,
                year_end=2024,
                submodel_name="Base / M-Sport",
                engine_base_id=2034,
                engine_description="2.0L L4 Turbo",
                pcdb_part_terminology_id=1896,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82, article_number="09.C399.13")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=9.5,
            dimensions_cm={"length": 34.0, "width": 34.0, "height": 7.3},
            material="UV Coated High Carbon",
            country_of_origin="IT",
            warranty_months=36
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=112.79,
        seller_name="RockAuto US Warehouse",
        seller_rating=4.7,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE"],
            ships_worldwide=True,
            base_shipping_cost_usd=42.00
        )
    ),

    # 3. BMW Front Brake Rotor - Zimmermann Sport Coat Z (AutoDoc EU)
    UnifiedPartListing(
        id="ad-zimm-150348320",
        source_platform="AutoDoc",
        source_listing_id="AD-ZIM-150348320",
        source_url="https://www.autodoc.de/zimmermann/7891234",
        source_logo_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=100&h=100&fit=crop",
        title="Otto Zimmermann Coat Z Drilled Sport Brake Disc Front",
        brand="Zimmermann",
        manufacturer_part_number="150.3483.20",
        clean_part_number="150348320",
        interchange_part_numbers=["34116792223", "09C39913", "DF6603S"],
        primary_image_url="https://images.unsplash.com/photo-1517524008697-84bbe3c3fd98?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="330i",
                year_start=2016,
                year_end=2024,
                pcdb_part_terminology_id=1896,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82, article_number="150.3483.20")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=9.6,
            dimensions_cm={"length": 34.0, "width": 34.0, "height": 7.3},
            material="Drilled Cast Iron Coat Z Anti-Corrosion",
            country_of_origin="DE",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        buy_now_price=128.90,
        seller_name="AutoDoc SE Germany",
        seller_rating=4.6,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["DE", "FR", "GB", "SA", "AE", "US"],
            ships_worldwide=True,
            base_shipping_cost_usd=39.50
        )
    ),

    # 4. BMW M-Sport Big Brake Pair - Salvage Grade A (eBay Motors Auction)
    UnifiedPartListing(
        id="ebay-bmw-rotor-pair",
        source_platform="eBay Motors",
        source_listing_id="EBAY-389104192",
        source_url="https://www.ebay.com/itm/389104192",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="OEM BMW F30 335i 340i M-Performance Front 370mm Dimpled Rotors (Pair)",
        brand="BMW Genuine",
        manufacturer_part_number="34116792223",
        clean_part_number="34116792223",
        interchange_part_numbers=["34116855006", "09C39913"],
        primary_image_url="https://images.unsplash.com/photo-1563720223185-11003d516935?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="340i",
                year_start=2015,
                year_end=2021,
                engine_description="3.0L L6 Turbo B58",
                pcdb_part_terminology_id=1896,
                pcdb_position="Front Left & Right"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82)
        ],
        pies_attributes=PIESAttributes(
            weight_kg=18.4,
            dimensions_cm={"length": 38.0, "width": 38.0, "height": 18.0},
            material="Cast iron / Alloy",
            country_of_origin="DE",
            warranty_months=6
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        current_bid=95.00,
        bid_count=14,
        auction_end_time=now + timedelta(hours=6, minutes=45),
        seller_name="BavarianSalvageRecyclers",
        seller_rating=4.95,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=55.00
        )
    ),

    # 5. Toyota Camry / RAV4 Brake Pads - Akebono ProACT Ultra Ceramic (RockAuto)
    UnifiedPartListing(
        id="ra-akebono-act1210",
        source_platform="RockAuto",
        source_listing_id="RA-AKE-ACT1210",
        source_url="https://www.rockauto.com/en/parts/akebono,ACT1210,brake+pad,1684",
        source_logo_url="https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=100&h=100&fit=crop",
        title="Akebono ProACT Ultra-Premium Ceramic Front Disc Brake Pad Set",
        brand="Akebono",
        manufacturer_part_number="ACT1210",
        clean_part_number="ACT1210",
        interchange_part_numbers=["0446542180", "04465AZ001", "BC1210", "D1210", "SP2138"],
        primary_image_url="https://images.unsplash.com/photo-1508974239320-0a029497e820?w=600&h=450&fit=crop",
        part_type="Brake Pads",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=132890,
                make_name="Toyota",
                model_name="Camry",
                year_start=2018,
                year_end=2024,
                engine_base_id=2500,
                engine_description="2.5L L4 A25A-FKS",
                pcdb_part_terminology_id=1684,
                pcdb_position="Front"
            ),
            ACESFitment(
                base_vehicle_id=134900,
                make_name="Toyota",
                model_name="RAV4",
                year_start=2019,
                year_end=2024,
                engine_base_id=2500,
                engine_description="2.5L L4 Dynamic Force",
                pcdb_part_terminology_id=1684,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=131002, generic_article_id=402, article_number="ACT1210")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=1.8,
            dimensions_cm={"length": 16.0, "width": 12.0, "height": 8.0},
            material="Ceramic Friction Compound",
            country_of_origin="US",
            warranty_months=36
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=48.79,
        seller_name="RockAuto Certified",
        seller_rating=4.8,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "KW"],
            ships_worldwide=True,
            base_shipping_cost_usd=22.00
        )
    ),

    # 6. Toyota Camry OEM Brake Pad Set (Partsouq OEM)
    UnifiedPartListing(
        id="ps-toyota-0446542180",
        source_platform="Partsouq",
        source_listing_id="PS-TY-0446542180",
        source_url="https://partsouq.com/en/search/all?q=0446542180",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="Toyota Genuine Parts Front Disc Brake Pad Kit OEM",
        brand="Toyota Genuine",
        manufacturer_part_number="04465-42180",
        clean_part_number="0446542180",
        interchange_part_numbers=["ACT1210", "04465AZ001", "BC1210"],
        primary_image_url="https://images.unsplash.com/photo-1600790142055-619df03207e6?w=600&h=450&fit=crop",
        part_type="Brake Pads",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=132890,
                make_name="Toyota",
                model_name="Camry",
                year_start=2018,
                year_end=2024,
                engine_base_id=2500,
                pcdb_part_terminology_id=1684,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=131002, generic_article_id=402, article_number="0446542180")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=1.9,
            dimensions_cm={"length": 16.5, "width": 12.0, "height": 8.0},
            material="Semi-Metallic OEM",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=64.20,
        seller_name="Partsouq Gulf Hub",
        seller_rating=4.9,
        seller_country="AE",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "SA", "AE", "KW", "QA", "OM", "BH", "GB"],
            ships_worldwide=True,
            base_shipping_cost_usd=18.50
        )
    ),

    # 7. Mercedes-Benz C300 Bosch Oxygen Sensor (AutoDoc)
    UnifiedPartListing(
        id="ad-bosch-0258007057",
        source_platform="AutoDoc",
        source_listing_id="AD-BSH-0258007057",
        source_url="https://www.autodoc.de/bosch/1149583",
        source_logo_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=100&h=100&fit=crop",
        title="Bosch Premium Wideband Lambda Oxygen Sensor (Pre-Cat)",
        brand="Bosch",
        manufacturer_part_number="0 258 007 057",
        clean_part_number="0258007057",
        interchange_part_numbers=["0045420718", "A0045420718", "17014"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="Oxygen Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=128450,
                make_name="Mercedes-Benz",
                model_name="C300",
                year_start=2015,
                year_end=2023,
                engine_description="2.0L Turbo M274 / M264",
                pcdb_part_terminology_id=5132,
                pcdb_position="Upstream Pre-Catalyst"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=108420, generic_article_id=3922, article_number="0258007057")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.25,
            dimensions_cm={"length": 15.0, "width": 8.0, "height": 5.0},
            material="Zirconia Ceramic / Stainless Housing",
            country_of_origin="DE",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=89.50,
        seller_name="AutoDoc Official Store",
        seller_rating=4.7,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["DE", "FR", "GB", "SA", "AE", "US", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=24.00
        )
    ),

    # 8. Porsche 911 Bilstein B6 Front Damper / Strut (Pressurized Gas - Hazmat Class 2)
    UnifiedPartListing(
        id="ebay-bilstein-porsche-damper",
        source_platform="eBay Motors",
        source_listing_id="EBAY-294819401",
        source_url="https://www.ebay.com/itm/294819401",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Bilstein B6 Performance Front Monotube Shock Absorber Strut",
        brand="Bilstein",
        manufacturer_part_number="24-062899",
        clean_part_number="24062899",
        interchange_part_numbers=["99734304104", "35122074", "V364127"],
        primary_image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=600&h=450&fit=crop",
        part_type="Shock Absorber",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=115670,
                make_name="Porsche",
                model_name="911",
                year_start=2005,
                year_end=2012,
                submodel_name="Carrera S (997)",
                engine_description="3.8L Flat 6",
                pcdb_part_terminology_id=7556,
                pcdb_position="Front Right"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=18744, generic_article_id=854, article_number="24-062899")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=4.2,
            dimensions_cm={"length": 62.0, "width": 14.0, "height": 14.0},
            material="High Pressure Nitrogen Monotube Steel",
            country_of_origin="DE",
            warranty_months=60
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        current_bid=215.00,
        bid_count=8,
        auction_end_time=now + timedelta(days=1, hours=3, minutes=10),
        seller_name="EuroParts_Direct_Warehouse",
        seller_rating=4.9,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.80.00",
            hazmat_class=HazmatClass.CLASS_2_GAS,
            air_freight_restricted=False,
            ships_to=["DE", "GB", "US", "SA", "AE", "JP"],
            ships_worldwide=True,
            base_shipping_cost_usd=52.00
        )
    ),

    # 9. Nissan GT-R R35 Fuel Injector Rail - JDM Yahoo Auctions Japan / Buyee
    UnifiedPartListing(
        id="yj-nissan-gtr-injector",
        source_platform="Yahoo! Auctions Japan",
        source_listing_id="YJ-JDM-4910283",
        source_url="https://auctions.yahoo.co.jp/item/4910283",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="JDM Nissan GT-R R35 OEM High Flow Injector 570cc Top Feed",
        brand="Nissan OEM",
        manufacturer_part_number="16600-JF00A",
        clean_part_number="16600JF00A",
        interchange_part_numbers=["0280158130", "F314", "16600EY00A"],
        primary_image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=450&fit=crop",
        part_type="Fuel Injector",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=121400,
                make_name="Nissan",
                model_name="GT-R",
                year_start=2008,
                year_end=2024,
                submodel_name="Premium / Nismo",
                engine_description="3.8L V6 Twin Turbo VR38DETT",
                pcdb_part_terminology_id=6010,
                pcdb_position="Engine Fuel Rail"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=29990, generic_article_id=3905, article_number="16600JF00A")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.15,
            dimensions_cm={"length": 9.0, "width": 4.0, "height": 4.0},
            material="Composite / Anodized Alloy",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        current_bid=68.00,
        bid_count=21,
        auction_end_time=now + timedelta(hours=2, minutes=15),
        seller_name="JDM_Tuning_Garage_Osaka",
        seller_rating=4.98,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=28.00
        )
    ),

    # 10. Audi A4 B9 Aluminum Front Wing / Fender (Car-Part Salvage Network)
    UnifiedPartListing(
        id="cp-audi-a4-fender",
        source_platform="Car-Part.com",
        source_listing_id="CP-AUD-882194",
        source_url="https://www.car-part.com/audi-a4-fender",
        source_logo_url="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=100&h=100&fit=crop",
        title="OEM Audi A4 S-Line Front Passenger Wing / Fender Glacier White Metallic (Grade B)",
        brand="Audi Genuine",
        manufacturer_part_number="8W0-821-106-B",
        clean_part_number="8W0821106B",
        interchange_part_numbers=["8W0821106", "AU1241158"],
        primary_image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?w=600&h=450&fit=crop",
        part_type="Fender",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=139880,
                make_name="Audi",
                model_name="A4",
                year_start=2017,
                year_end=2023,
                submodel_name="Premium Plus / Prestige",
                pcdb_part_terminology_id=1344,
                pcdb_position="Front Right"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=117390, generic_article_id=258, article_number="8W0821106B")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=5.8,
            dimensions_cm={"length": 110.0, "width": 80.0, "height": 22.0},
            material="Stamped Automotive Aluminum",
            country_of_origin="DE",
            warranty_months=3
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.USED_GRADE_B,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=145.00,
        seller_name="Midwest Prestige Auto Recyclers",
        seller_rating=4.65,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE"],
            ships_worldwide=False,
            freight_forwarder_permitted=True,
            base_shipping_cost_usd=95.00 # Oversized dimensional freight
        )
    ),

    # 11. BMW M-Sport Steering Wheel Airbag Module (Class 1.4G Pyrotechnic Hazmat Flagged)
    UnifiedPartListing(
        id="ebay-bmw-airbag-module",
        source_platform="eBay Motors",
        source_listing_id="EBAY-9941031",
        source_url="https://www.ebay.com/itm/9941031",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="OEM BMW F30 F80 F82 M3 M4 Dual-Stage Driver Steering Wheel Airbag",
        brand="BMW Genuine",
        manufacturer_part_number="32307845798",
        clean_part_number="32307845798",
        interchange_part_numbers=["32308092711"],
        primary_image_url="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=450&fit=crop",
        part_type="Airbag Module",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="M3",
                year_start=2015,
                year_end=2020,
                pcdb_part_terminology_id=9820,
                pcdb_position="Driver Steering Wheel"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=105501, generic_article_id=459, article_number="32307845798")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=1.4,
            dimensions_cm={"length": 20.0, "width": 20.0, "height": 14.0},
            material="Leather / SRS Pyrotechnic Canister",
            country_of_origin="DE",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=399.00,
        seller_name="BavarianSRS_OEM",
        seller_rating=4.92,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.95.00",
            hazmat_class=HazmatClass.CLASS_1_EXPLOSIVE,
            air_freight_restricted=True,
            ships_to=["DE", "FR", "NL", "BE"], # Restrictive due to pyrotechnic air ban
            ships_worldwide=False,
            freight_forwarder_permitted=False,
            base_shipping_cost_usd=80.00
        )
    ),

    # 12. FCP Euro - BMW Brake Rotor with Lifetime Replacement Guarantee
    UnifiedPartListing(
        id="fcp-bmw-34116792223",
        source_platform="FCP Euro",
        source_listing_id="FCP-BRM-34116792223",
        source_url="https://www.fcpeuro.com/products/bmw-brake-disc-front-34116792223",
        source_logo_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=100&h=100&fit=crop",
        title="BMW Front Brake Rotor 340mm - Genuine BMW (Lifetime Replacement)",
        brand="BMW Genuine",
        manufacturer_part_number="34116792223",
        clean_part_number="34116792223",
        interchange_part_numbers=["09C39913", "150348320", "DF6603S"],
        primary_image_url="https://images.unsplash.com/photo-1600790142055-619df03207e6?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="330i",
                year_start=2016,
                year_end=2024,
                submodel_name="M Sport",
                pcdb_part_terminology_id=1896,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82, article_number="34116792223")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=9.8,
            dimensions_cm={"length": 34.0, "width": 34.0, "height": 7.3},
            material="High Carbon Cast Iron",
            country_of_origin="DE",
            warranty_months=120 # Lifetime replacement guarantee
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=164.99,
        seller_name="FCP Euro Official",
        seller_rating=4.96,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=45.00
        )
    ),

    # 13. Amayama - Toyota OEM Brake Pads Direct from Japan
    UnifiedPartListing(
        id="ama-toyota-0446542180",
        source_platform="Amayama",
        source_listing_id="AMA-TY-0446542180",
        source_url="https://www.amayama.com/en/part/toyota/0446542180",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="Toyota Genuine Brake Pad Set Front (Direct Nagoya Warehouse)",
        brand="Toyota Genuine",
        manufacturer_part_number="04465-42180",
        clean_part_number="0446542180",
        interchange_part_numbers=["ACT1210", "04465AZ001", "BC1210"],
        primary_image_url="https://images.unsplash.com/photo-1508974239320-0a029497e820?w=600&h=450&fit=crop",
        part_type="Brake Pads",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=132890,
                make_name="Toyota",
                model_name="Camry",
                year_start=2018,
                year_end=2024,
                engine_base_id=2500,
                pcdb_part_terminology_id=1684,
                pcdb_position="Front"
            ),
            ACESFitment(
                base_vehicle_id=134900,
                make_name="Toyota",
                model_name="RAV4",
                year_start=2019,
                year_end=2024,
                pcdb_part_terminology_id=1684,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=131002, generic_article_id=402, article_number="0446542180")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=1.85,
            dimensions_cm={"length": 16.0, "width": 12.0, "height": 8.0},
            material="JDM Semi-Metallic Friction",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=54.60,
        seller_name="Amayama Trading Co. Japan",
        seller_rating=4.94,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "KW", "QA", "OM", "BH", "GB", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=21.00
        )
    ),

    # 14. Allegro - Audi A4 B9 Aluminum Fender (Poland / EU Auction)
    UnifiedPartListing(
        id="all-audi-a4-fender",
        source_platform="Allegro",
        source_listing_id="ALL-PL-9821034",
        source_url="https://allegro.pl/oferta/blotnik-audi-a4-b9-prawy-przod-9821034",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Oryginalny Błotnik Przód Prawy Audi A4 B9 S-Line Mythos Black (Used Grade A)",
        brand="Audi Genuine",
        manufacturer_part_number="8W0 821 106 B",
        clean_part_number="8W0821106B",
        interchange_part_numbers=["8W0821106", "AU1241158"],
        primary_image_url="https://images.unsplash.com/photo-1502877338535-766e1452684a?w=600&h=450&fit=crop",
        part_type="Fender",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=139880,
                make_name="Audi",
                model_name="A4",
                year_start=2017,
                year_end=2023,
                pcdb_part_terminology_id=1344,
                pcdb_position="Front Right"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=117390, generic_article_id=258, article_number="8W0821106B")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=5.8,
            dimensions_cm={"length": 110.0, "width": 80.0, "height": 22.0},
            material="Aluminum Alloy",
            country_of_origin="DE",
            warranty_months=6
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        current_bid=110.00,
        bid_count=18,
        auction_end_time=now + timedelta(hours=9, minutes=30),
        seller_name="VAG_AutoParts_Poznan",
        seller_rating=4.91,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["DE", "FR", "GB", "PL", "SA", "AE", "US"],
            ships_worldwide=True,
            base_shipping_cost_usd=85.00
        )
    ),

    # 15. B-Parts - Mercedes-Benz C300 O2 Sensor (European Certified Recycled)
    UnifiedPartListing(
        id="bp-mercedes-o2-sensor",
        source_platform="B-Parts",
        source_listing_id="BP-FR-449102",
        source_url="https://www.b-parts.com/auto-parts/engine/oxygen-sensor-mercedes-c-class-0045420718",
        source_logo_url="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=100&h=100&fit=crop",
        title="Certified OEM Oxygen Lambda Sensor Mercedes C-Class W205 C300 (Tested)",
        brand="Mercedes-Benz",
        manufacturer_part_number="A0045420718",
        clean_part_number="0045420718",
        interchange_part_numbers=["0258007057", "17014"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="Oxygen Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=128450,
                make_name="Mercedes-Benz",
                model_name="C300",
                year_start=2015,
                year_end=2023,
                pcdb_part_terminology_id=5132,
                pcdb_position="Upstream Pre-Cat"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=108420, generic_article_id=3922, article_number="0045420718")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.25,
            dimensions_cm={"length": 15.0, "width": 8.0, "height": 5.0},
            material="Stainless / Ceramic",
            country_of_origin="DE",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=58.00,
        seller_name="B-Parts Certified Recycler France",
        seller_rating=4.88,
        seller_country="DE",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["DE", "FR", "GB", "SA", "AE", "US", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=19.50
        )
    ),

    # 16. Up Garage - Nissan GT-R R35 VR38DETT Injectors (JDM Tuning)
    UnifiedPartListing(
        id="cro-nissan-gtr-injectors",
        source_platform="Up Garage",
        source_listing_id="CRO-UP-8849102",
        source_url="https://www.croooober.com/en/cpart/8849102",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="Up Garage JDM Nissan GT-R R35 High Performance Injectors Set of 6",
        brand="Nissan OEM",
        manufacturer_part_number="16600-JF00A",
        clean_part_number="16600JF00A",
        interchange_part_numbers=["0280158130", "F314", "16600EY00A"],
        primary_image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=450&fit=crop",
        part_type="Fuel Injector",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=121400,
                make_name="Nissan",
                model_name="GT-R",
                year_start=2008,
                year_end=2024,
                engine_description="3.8L V6 Twin Turbo VR38DETT",
                pcdb_part_terminology_id=6010,
                pcdb_position="Fuel Rail"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=29990, generic_article_id=3905, article_number="16600JF00A")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.9,
            dimensions_cm={"length": 20.0, "width": 15.0, "height": 6.0},
            material="Anodized Alloy / Composite",
            country_of_origin="JP",
            warranty_months=6
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        current_bid=180.00,
        bid_count=32,
        auction_end_time=now + timedelta(hours=4, minutes=10),
        seller_name="Up Garage Machida Yokohama",
        seller_rating=4.95,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=32.00
        )
    ),

    # 17. Megazip - Honda Civic OEM Alternator Direct Exporter
    UnifiedPartListing(
        id="mz-honda-alternator",
        source_platform="Megazip",
        source_listing_id="MZ-HND-31100R40A01",
        source_url="https://www.megazip.net/zapchasti-dlya/honda/alternator-assy-31100R40A01",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="Honda Genuine Alternator Assembly 105A Denso OEM",
        brand="Honda Genuine",
        manufacturer_part_number="31100-R40-A01",
        clean_part_number="31100R40A01",
        interchange_part_numbers=["1042105910", "AL1298X", "2100656"],
        primary_image_url="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=450&fit=crop",
        part_type="Alternator",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=129500,
                make_name="Honda",
                model_name="Civic",
                year_start=2016,
                year_end=2022,
                engine_description="2.0L L4 K20C2",
                pcdb_part_terminology_id=2412,
                pcdb_position="Front Engine Accessory Drive"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=115201, generic_article_id=4, article_number="31100R40A01")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=6.4,
            dimensions_cm={"length": 25.0, "width": 22.0, "height": 18.0},
            material="Cast Aluminum / Copper Windings",
            country_of_origin="JP",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=245.00,
        seller_name="Megazip Global Hub",
        seller_rating=4.89,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.99.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "SA", "AE", "JP", "KW", "QA", "OM", "GB", "DE", "CA", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=48.00
        )
    ),

    # 18. ECS Tuning - Porsche 911 Bilstein B6 Strut
    UnifiedPartListing(
        id="ecs-porsche-damper",
        source_platform="ECS Tuning",
        source_listing_id="ECS-BIL-24062899",
        source_url="https://www.ecstuning.com/b-bilstein-parts/front-b6-performance-strut/24-062899/",
        source_logo_url="https://images.unsplash.com/photo-1549399542-7e3f8b79c341?w=100&h=100&fit=crop",
        title="Bilstein B6 Performance Front Monotube Strut Porsche 997 Carrera",
        brand="Bilstein",
        manufacturer_part_number="24-062899",
        clean_part_number="24062899",
        interchange_part_numbers=["99734304104", "35122074", "V364127"],
        primary_image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=600&h=450&fit=crop",
        part_type="Shock Absorber",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=115670,
                make_name="Porsche",
                model_name="911",
                year_start=2005,
                year_end=2012,
                submodel_name="Carrera S (997)",
                pcdb_part_terminology_id=7556,
                pcdb_position="Front Right"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=18744, generic_article_id=854, article_number="24-062899")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=4.2,
            dimensions_cm={"length": 62.0, "width": 14.0, "height": 14.0},
            material="High Pressure Monotube",
            country_of_origin="DE",
            warranty_months=60
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        buy_now_price=229.00,
        seller_name="ECS Tuning Enthusiast Depot",
        seller_rating=4.82,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.80.00",
            hazmat_class=HazmatClass.CLASS_2_GAS,
            air_freight_restricted=False,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE"],
            ships_worldwide=True,
            base_shipping_cost_usd=54.00
        )
    ),

    # 19. Summit Racing - Brembo Coated Front Brake Rotor
    UnifiedPartListing(
        id="sum-brembo-09c39913",
        source_platform="Summit Racing",
        source_listing_id="SUM-BRM-09C39913",
        source_url="https://www.summitracing.com/parts/brm-09c39913",
        source_logo_url="https://images.unsplash.com/photo-1558981403-c5f9899a28bc?w=100&h=100&fit=crop",
        title="Brembo Prime Coated High Carbon Front Brake Disc 340mm",
        brand="Brembo",
        manufacturer_part_number="09.C399.13",
        clean_part_number="09C39913",
        interchange_part_numbers=["34116792223", "150348320", "55523"],
        primary_image_url="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=450&fit=crop",
        part_type="Brake Rotor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=141029,
                make_name="BMW",
                model_name="330i",
                year_start=2016,
                year_end=2024,
                pcdb_part_terminology_id=1896,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=119421, generic_article_id=82, article_number="09.C399.13")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=9.5,
            dimensions_cm={"length": 34.0, "width": 34.0, "height": 7.3},
            material="UV Coated High Carbon Cast Iron",
            country_of_origin="IT",
            warranty_months=36
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=118.50,
        seller_name="Summit Racing Equipment",
        seller_rating=4.93,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE", "AU", "MX"],
            ships_worldwide=True,
            base_shipping_cost_usd=44.00
        )
    ),

    # 20. Yahoo! Auctions Japan - Nissan Silvia S14 S15 SR20DET MAF Sensor (22680-69F01)
    UnifiedPartListing(
        id="yj-nissan-maf-2268069f01",
        source_platform="Yahoo! Auctions Japan",
        source_listing_id="YJ-MAF-2268069F01",
        source_url="https://auctions.yahoo.co.jp/item/s15-maf-2268069f01",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="JDM OEM Nissan Silvia S14 S15 SR20DET Mass Air Flow MAF Sensor (22680-69F01)",
        brand="Nissan Genuine",
        manufacturer_part_number="22680-69F01",
        clean_part_number="2268069F01",
        interchange_part_numbers=["2268069F00", "A36608E60", "22680AD21A", "AFH7014", "MAF0042"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="MAF Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1993,
                year_end=2002,
                submodel_name="S14 / S15 Spec-R",
                engine_description="2.0L Turbo SR20DET",
                pcdb_part_terminology_id=5128,
                pcdb_position="Intake Air Duct"
            ),
            ACESFitment(
                base_vehicle_id=118925,
                make_name="Nissan",
                model_name="200SX",
                year_start=1994,
                year_end=2000,
                submodel_name="Turbo",
                engine_description="2.0L Turbo SR20DET",
                pcdb_part_terminology_id=5128,
                pcdb_position="Intake Air Duct"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=14619, generic_article_id=3926, article_number="2268069F01")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.45,
            dimensions_cm={"length": 14.0, "width": 10.0, "height": 9.0},
            material="PBT Thermoplastic / Hot Wire Element",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        current_bid=148.00,
        bid_count=24,
        auction_end_time=now + timedelta(hours=5, minutes=45),
        seller_name="JDM_Direct_Osaka",
        seller_rating=4.97,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="9026.10.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "DE", "CA", "KW", "QA"],
            ships_worldwide=True,
            base_shipping_cost_usd=28.00
        )
    ),

    # 21. Amayama - Nissan Genuine MAF Sensor 22680-69F01 (Direct Factory New Japan)
    UnifiedPartListing(
        id="ama-nissan-maf-2268069f01",
        source_platform="Amayama",
        source_listing_id="AMA-NI-2268069F01",
        source_url="https://www.amayama.com/en/part/nissan/2268069f01",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="Nissan Genuine Mass Air Flow Sensor Meter 22680-69F01 (Direct Japan)",
        brand="Nissan Genuine",
        manufacturer_part_number="22680-69F01",
        clean_part_number="2268069F01",
        interchange_part_numbers=["2268069F00", "A36608E60", "22680AD21A", "AFH7014"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="MAF Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1993,
                year_end=2002,
                submodel_name="S14 / S15 Spec-R",
                engine_description="2.0L Turbo SR20DET",
                pcdb_part_terminology_id=5128,
                pcdb_position="Intake"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=14619, generic_article_id=3926, article_number="2268069F01")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.45,
            dimensions_cm={"length": 14.0, "width": 10.0, "height": 9.0},
            material="OEM PBT Housing & Platinum Hot Wire",
            country_of_origin="JP",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=375.00,
        seller_name="Amayama Trading Co. Tokyo",
        seller_rating=4.95,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="9026.10.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "KW", "QA", "OM", "BH", "GB", "DE", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=22.50
        )
    ),

    # 22. Up Garage - Nissan Silvia S15 JDM MAF Sensor (A36-608 E60)
    UnifiedPartListing(
        id="cro-nissan-maf-a36608e60",
        source_platform="Up Garage",
        source_listing_id="CRO-UP-2268069F01",
        source_url="https://www.croooober.com/en/cpart/maf-2268069f01",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="Up Garage Nissan Silvia S15 Spec-R JDM Air Flow Meter A36-608 E60 (Grade A)",
        brand="Unisia Jecs",
        manufacturer_part_number="A36-608 E60",
        clean_part_number="A36608E60",
        interchange_part_numbers=["2268069F01", "2268069F00", "22680AD21A"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="MAF Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1999,
                year_end=2002,
                submodel_name="S15 Spec-R",
                engine_description="2.0L Turbo SR20DET",
                pcdb_part_terminology_id=5128,
                pcdb_position="Air Filter Housing"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=14619, generic_article_id=3926, article_number="A36608E60")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.45,
            dimensions_cm={"length": 14.0, "width": 10.0, "height": 9.0},
            material="Composite / Platinum Sensor",
            country_of_origin="JP",
            warranty_months=6
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=165.00,
        seller_name="Up Garage Chiba Shiroi",
        seller_rating=4.92,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="9026.10.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "DE", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=30.00
        )
    ),

    # 23. Partsouq - Nissan Genuine MAF Sensor 22680-69F01 (Gulf Hub)
    UnifiedPartListing(
        id="ps-nissan-maf-2268069f01",
        source_platform="Partsouq",
        source_listing_id="PS-NI-2268069F01",
        source_url="https://partsouq.com/en/search/all?q=2268069F01",
        source_logo_url="https://images.unsplash.com/photo-1617788138017-80ad40651399?w=100&h=100&fit=crop",
        title="Nissan Genuine Mass Airflow Meter Sensor (22680-69F01)",
        brand="Nissan Genuine",
        manufacturer_part_number="22680-69F01",
        clean_part_number="2268069F01",
        interchange_part_numbers=["2268069F00", "A36608E60", "22680AD21A"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="MAF Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1993,
                year_end=2002,
                pcdb_part_terminology_id=5128,
                pcdb_position="Intake"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=14619, generic_article_id=3926, article_number="2268069F01")
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.45,
            dimensions_cm={"length": 14.0, "width": 10.0, "height": 9.0},
            material="OEM Sensor Assembly",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.OEM_GENUINE,
        currency="USD",
        buy_now_price=398.00,
        seller_name="Partsouq Direct Middle East",
        seller_rating=4.91,
        seller_country="AE",
        shipping=ShippingCompliance(
            hs_code="9026.10.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "SA", "AE", "KW", "QA", "OM", "BH", "GB", "DE"],
            ships_worldwide=True,
            base_shipping_cost_usd=24.00
        )
    ),

    # 24. eBay Motors - Remanufactured OEM MAF Sensor 22680-69F01
    UnifiedPartListing(
        id="ebay-nissan-maf-2268069f01",
        source_platform="eBay Motors",
        source_listing_id="EBAY-MAF-2268069F01",
        source_url="https://www.ebay.com/itm/nissan-silvia-maf-2268069f01",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="OEM Mass Air Flow Sensor MAF for Nissan 200SX Silvia S14 S15 SR20DET 22680-69F01",
        brand="Hitachi / Unisia Jecs",
        manufacturer_part_number="22680-69F01",
        clean_part_number="2268069F01",
        interchange_part_numbers=["A36608E60", "2268069F00"],
        primary_image_url="https://images.unsplash.com/photo-1580273916550-e323be2ae537?w=600&h=450&fit=crop",
        part_type="MAF Sensor",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1993,
                year_end=2002,
                engine_description="2.0L Turbo SR20DET",
                pcdb_part_terminology_id=5128,
                pcdb_position="Intake"
            )
        ],
        tecdoc_fitments=[
            TecDocFitment(k_type=14619, generic_article_id=3926)
        ],
        pies_attributes=PIESAttributes(
            weight_kg=0.45,
            dimensions_cm={"length": 14.0, "width": 10.0, "height": 9.0},
            material="Refurbished OEM Hitachi Module",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_REMANUFACTURED,
        authenticity_tier=AuthenticityTier.OES_TIER1,
        currency="USD",
        buy_now_price=189.00,
        seller_name="JDM_Electronics_Reman",
        seller_rating=4.94,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="9026.10.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=25.00
        )
    ),

    # 25. Up Garage - BRIDE Zeta III Full Bucket Seat CFRP Carbon
    UnifiedPartListing(
        id="upg-bride-zeta3-crfp",
        source_platform="Up Garage",
        source_listing_id="UPG-BRD-ZETA3-CRFP",
        source_url="https://www.upgarage.com/en/ec/search?q=BRIDE+ZETA+III",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="BRIDE Zeta III Full Bucket Racing Seat CFRP Carbon Finish Black (Genuine JDM)",
        brand="BRIDE",
        manufacturer_part_number="F31AMR",
        clean_part_number="F31AMR",
        interchange_part_numbers=["F31HMR", "BRIDE-ZETA3"],
        primary_image_url="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=600&h=450&fit=crop",
        part_type="Racing Bucket Seat",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Universal",
                model_name="Racing Seat / Track Car",
                year_start=1990,
                year_end=2026,
                pcdb_part_terminology_id=9100,
                pcdb_position="Driver Side (Right/Left)"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=7.2,
            dimensions_cm={"length": 88.0, "width": 50.0, "height": 48.0},
            material="CFRP Carbon Fiber Composite / Fire-Resistant Fabric",
            country_of_origin="JP",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        buy_now_price=640.00,
        seller_name="Up Garage Yokohama GT-Depot",
        seller_rating=4.96,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "DE", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=95.00
        )
    ),

    # 26. Yahoo! Auctions Japan - BRIDE Zeta 3 Black Bucket Seat S14 S15 R34
    UnifiedPartListing(
        id="yj-bride-zeta3-black",
        source_platform="Yahoo! Auctions Japan",
        source_listing_id="YJ-BRD-ZETA3-F31HMR",
        source_url="https://buyee.jp/item/search/query/BRIDE%20ZETA%20III?translationType=1",
        source_logo_url="https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=100&h=100&fit=crop",
        title="JDM BRIDE Zeta 3 (Zeta III) FRP Black Bucket Seat S13 S14 S15 R32 R34 GT-R",
        brand="BRIDE",
        manufacturer_part_number="F31HMR",
        clean_part_number="F31HMR",
        interchange_part_numbers=["F31AMR"],
        primary_image_url="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=600&h=450&fit=crop",
        part_type="Racing Bucket Seat",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Universal",
                model_name="Racing Seat",
                year_start=1990,
                year_end=2026,
                pcdb_part_terminology_id=9100,
                pcdb_position="Driver"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=7.4,
            dimensions_cm={"length": 88.0, "width": 50.0, "height": 48.0},
            material="FRP Silver Shell / Flame Retardant Fabric",
            country_of_origin="JP",
            warranty_months=6
        ),
        listing_type=ListingType.AUCTION,
        condition=ItemCondition.USED_GRADE_A,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        current_bid=420.00,
        bid_count=31,
        auction_end_time=now + timedelta(hours=6, minutes=30),
        seller_name="JDM_Tuning_Osaka",
        seller_rating=4.95,
        seller_country="JP",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["JP", "US", "SA", "AE", "AU", "GB", "DE", "CA"],
            ships_worldwide=True,
            base_shipping_cost_usd=90.00
        )
    ),

    # 27. eBay Motors - Authentic BRIDE Zeta III Carbon CFRP Racing Bucket Seat
    UnifiedPartListing(
        id="ebay-bride-zeta3-crfp",
        source_platform="eBay Motors",
        source_listing_id="EBAY-BRD-ZETA3-CFRP",
        source_url="https://www.ebay.com/sch/i.html?_nkw=BRIDE+Zeta+III+CFRP&_sacat=6000",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Authentic BRIDE Zeta III Carbon CFRP Racing Bucket Seat - Black Logo",
        brand="BRIDE",
        manufacturer_part_number="F31AMR",
        clean_part_number="F31AMR",
        interchange_part_numbers=["F31HMR"],
        primary_image_url="https://images.unsplash.com/photo-1542282088-72c9c27ed0cd?w=600&h=450&fit=crop",
        part_type="Racing Bucket Seat",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Universal",
                model_name="Track / Motorsport",
                year_start=1990,
                year_end=2026,
                pcdb_part_terminology_id=9100,
                pcdb_position="Front"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=7.2,
            dimensions_cm={"length": 88.0, "width": 50.0, "height": 48.0},
            material="CFRP Carbon Fiber Composite Shell",
            country_of_origin="JP",
            warranty_months=24
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_PERF,
        currency="USD",
        buy_now_price=799.00,
        seller_name="Motorsport_JDM_USA",
        seller_rating=4.98,
        seller_country="US",
        shipping=ShippingCompliance(
            hs_code="8708.29.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["US", "CA", "SA", "AE", "GB", "DE", "AU"],
            ships_worldwide=True,
            base_shipping_cost_usd=85.00
        )
    ),
    # 28. AliExpress - Nissan Silvia S15 Smoke LED DRL Tail Lights Assembly (Direct Fit)
    UnifiedPartListing(
        id="ali-s15-led-tail",
        source_platform="AliExpress",
        source_listing_id="ALI-9844102",
        source_url="https://www.aliexpress.com/wholesale?SearchText=s15+tail+lights",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Nissan Silvia S15 Smoke LED DRL Tail Lights Assembly (Direct Fit)",
        brand="AliExpress Direct",
        manufacturer_part_number="B6550-85F00",
        clean_part_number="B655085F00",
        interchange_part_numbers=["B6550-85F00", "B6555-85F00"],
        primary_image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=600&h=450&fit=crop",
        part_type="Lighting",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1999,
                year_end=2002,
                submodel_name="Spec-R / Spec-S",
                pcdb_part_terminology_id=9000,
                pcdb_position="Rear Assembly Left & Right Pair"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=4.2,
            dimensions_cm={"length": 45.0, "width": 30.0, "height": 22.0},
            material="OEM Polycarbonate / LED Boards",
            country_of_origin="CN",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_VALUE,
        currency="USD",
        buy_now_price=189.00,
        seller_name="Guangzhou_Auto_Lighting_Direct",
        seller_rating=4.82,
        seller_country="CN",
        shipping=ShippingCompliance(
            hs_code="8512.20.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["*"],
            ships_worldwide=True,
            base_shipping_cost_usd=28.00
        )
    ),
    # 29. AliExpress - High Performance Ignition Coil Pack Set for Nissan SR20DET (Pack of 4)
    UnifiedPartListing(
        id="ali-sr20det-coils",
        source_platform="AliExpress",
        source_listing_id="ALI-3819441",
        source_url="https://www.aliexpress.com/wholesale?SearchText=sr20det+coilpack",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="High Performance Ignition Coil Pack Set for Nissan SR20DET S14 S15 (Set of 4)",
        brand="AliExpress Direct",
        manufacturer_part_number="22448-91F00",
        clean_part_number="2244891F00",
        interchange_part_numbers=["22448-91F00", "2244891F00", "DIS-005"],
        primary_image_url="https://images.unsplash.com/photo-1619642751034-765dfdf7c58e?w=600&h=450&fit=crop",
        part_type="Ignition Coil",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1993,
                year_end=2002,
                submodel_name="SR20DET",
                pcdb_part_terminology_id=7000,
                pcdb_position="Engine Bay / Cylinder Head"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=1.8,
            dimensions_cm={"length": 25.0, "width": 18.0, "height": 12.0},
            material="High Temp Copper / Epoxy",
            country_of_origin="CN",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_VALUE,
        currency="USD",
        buy_now_price=78.50,
        seller_name="RacingPower_Direct_Store",
        seller_rating=4.79,
        seller_country="CN",
        shipping=ShippingCompliance(
            hs_code="8511.30.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["*"],
            ships_worldwide=True,
            base_shipping_cost_usd=16.00
        )
    ),
    # 30. AliExpress - Nissan Silvia S15 Spec-R Full LED Projector Headlights (Pair)
    UnifiedPartListing(
        id="ali-s15-led-headlight",
        source_platform="AliExpress",
        source_listing_id="ALI-7721903",
        source_url="https://www.aliexpress.com/wholesale?SearchText=Nissan+Silvia+S15+LED+Headlights",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Nissan Silvia S15 Spec-R Full LED Projector Headlights Assembly (Pair)",
        brand="AliExpress Direct",
        manufacturer_part_number="26010-85F00",
        clean_part_number="2601085F00",
        interchange_part_numbers=["26010-85F00", "26060-85F00"],
        primary_image_url="https://images.unsplash.com/photo-1511919884226-fd3cad34687c?w=600&h=450&fit=crop",
        part_type="Lighting",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1999,
                year_end=2002,
                submodel_name="Spec-R / Spec-S",
                pcdb_part_terminology_id=9000,
                pcdb_position="Front Headlamp Pair"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=5.8,
            dimensions_cm={"length": 55.0, "width": 35.0, "height": 25.0},
            material="UV Polycarbonate / Bi-LED Projectors",
            country_of_origin="CN",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_VALUE,
        currency="USD",
        buy_now_price=245.00,
        seller_name="Guangzhou_Auto_Lighting_Direct",
        seller_rating=4.85,
        seller_country="CN",
        shipping=ShippingCompliance(
            hs_code="8512.20.00",
            hazmat_class=HazmatClass.NONE,
            ships_to=["*"],
            ships_worldwide=True,
            base_shipping_cost_usd=32.00
        )
    ),
    # 31. AliExpress - Nissan Silvia S15 Front Bumper Lip Spoiler (Carbon Fiber Style)
    UnifiedPartListing(
        id="ali-s15-carbon-lip",
        source_platform="AliExpress",
        source_listing_id="ALI-5510291",
        source_url="https://www.aliexpress.com/wholesale?SearchText=Nissan+Silvia+S15+Front+Lip+Spoiler",
        source_logo_url="https://images.unsplash.com/photo-1557804506-669a67965ba0?w=100&h=100&fit=crop",
        title="Nissan Silvia S15 Front Bumper Lip Spoiler (Carbon Fiber Style Polyurethane)",
        brand="AliExpress Direct",
        manufacturer_part_number="96010-85F00",
        clean_part_number="9601085F00",
        interchange_part_numbers=[],
        primary_image_url="https://images.unsplash.com/photo-1503376780353-7e6692767b70?w=600&h=450&fit=crop",
        part_type="Body Styling",
        aces_fitments=[
            ACESFitment(
                base_vehicle_id=118920,
                make_name="Nissan",
                model_name="Silvia",
                year_start=1999,
                year_end=2002,
                submodel_name="Spec-R / Spec-S",
                pcdb_part_terminology_id=9100,
                pcdb_position="Front Lower Bumper"
            )
        ],
        tecdoc_fitments=[],
        pies_attributes=PIESAttributes(
            weight_kg=3.5,
            dimensions_cm={"length": 160.0, "width": 45.0, "height": 15.0},
            material="Flexible Polyurethane / Hydro-dip Carbon",
            country_of_origin="CN",
            warranty_months=12
        ),
        listing_type=ListingType.BUY_NOW,
        condition=ItemCondition.NEW_SEALED,
        authenticity_tier=AuthenticityTier.AFTERMARKET_VALUE,
        currency="USD",
        buy_now_price=115.00,
        seller_name="AeroDynamics_Factory_Direct",
        seller_rating=4.76,
        seller_country="CN",
        shipping=ShippingCompliance(
            hs_code="8708.29.90",
            hazmat_class=HazmatClass.NONE,
            ships_to=["*"],
            ships_worldwide=True,
            base_shipping_cost_usd=38.00
        )
    )
]

# Ensure every catalog listing has a live, guaranteed functional deep link
# directly into the actual retailer part page rather than an empty root page
for _item in MOCK_CATALOG:
    _make = _item.aces_fitments[0].make_name if _item.aces_fitments else ""
    _item.source_url = DeepLinker.get_live_url(
        platform=_item.source_platform,
        mpn=_item.manufacturer_part_number,
        clean_pn=_item.clean_part_number,
        title=_item.title,
        make=_make,
        brand=_item.brand,
        listing_id=_item.source_listing_id
    )

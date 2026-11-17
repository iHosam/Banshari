"""
International Logistics, HS Tariff Classification, Hazmat Compliance, and Landed Cost Engine
"""

from typing import Dict, Any, Optional
from ..schemas.unified_part import HazmatClass
from ..schemas.search import LandedCostEstimate

class LogisticsEngine:
    # Exchange rates relative to 1.00 USD
    EXCHANGE_RATES: Dict[str, float] = {
        "USD": 1.00,
        "SAR": 3.75,
        "AED": 3.67,
        "EUR": 0.92,
        "GBP": 0.78,
        "CAD": 1.36,
        "JPY": 154.50,
        "KWD": 0.31,
        "QAR": 3.64
    }

    CURRENCY_SYMBOLS: Dict[str, str] = {
        "USD": "$",
        "SAR": "SAR ",
        "AED": "AED ",
        "EUR": "€",
        "GBP": "£",
        "CAD": "CA$",
        "JPY": "¥",
        "KWD": "KD ",
        "QAR": "QR "
    }

    # Country Specific Customs Duty & VAT/GST Rates
    COUNTRY_TARIFFS: Dict[str, Dict[str, float]] = {
        "SA": {"duty": 0.05, "vat": 0.15, "currency": "SAR"},  # Saudi Arabia (5% duty, 15% VAT)
        "AE": {"duty": 0.05, "vat": 0.05, "currency": "AED"},  # UAE (5% duty, 5% VAT)
        "US": {"duty": 0.025, "vat": 0.00, "currency": "USD"}, # USA
        "GB": {"duty": 0.045, "vat": 0.20, "currency": "GBP"}, # UK
        "DE": {"duty": 0.045, "vat": 0.19, "currency": "EUR"}, # Germany / EU
        "CA": {"duty": 0.06, "vat": 0.13, "currency": "CAD"},  # Canada
        "JP": {"duty": 0.00, "vat": 0.10, "currency": "JPY"},  # Japan
        "KW": {"duty": 0.05, "vat": 0.00, "currency": "KWD"},  # Kuwait
        "QA": {"duty": 0.05, "vat": 0.00, "currency": "QAR"},  # Qatar
    }

    # HS Tariff Mapping (Chapter 8708)
    HS_CODE_MAP: Dict[str, str] = {
        "brake": "8708.30.00",      # Brakes, servo-brakes and parts
        "rotor": "8708.30.00",
        "pad": "8708.30.00",
        "suspension": "8708.80.00", # Suspension systems & shock absorbers
        "strut": "8708.80.00",
        "shock": "8708.80.00",
        "body": "8708.29.00",       # Other parts and accessories of bodies
        "fender": "8708.29.00",
        "hood": "8708.29.00",
        "bumper": "8708.10.00",     # Bumpers and parts thereof
        "gearbox": "8708.40.00",    # Gear boxes and parts
        "driveshaft": "8708.50.00", # Drive-axles with differential
        "radiator": "8708.91.00",   # Radiators and parts
        "silencer": "8708.92.00",   # Silencers and exhaust pipes
        "muffler": "8708.92.00",
        "airbag": "8708.95.00",     # Safety airbags with inflator system
        "battery": "8507.60.00",    # Lithium-ion accumulators
    }

    @classmethod
    def get_hs_code(cls, part_title: str) -> str:
        """Determines appropriate HS Code based on part nomenclature"""
        lower = part_title.lower()
        for kw, hs in cls.HS_CODE_MAP.items():
            if kw in lower:
                return hs
        return "8708.99.00" # Parts and accessories, not elsewhere specified

    @classmethod
    def assess_hazmat(cls, part_title: str) -> Dict[str, Any]:
        """
        Assesses if an automotive item has IATA / IMDG hazmat restrictions.
        """
        lower = part_title.lower()
        if any(w in lower for w in ["airbag", "srs", "inflator", "pyrotechnic", "squib"]):
            return {
                "hazmat_class": HazmatClass.CLASS_1_EXPLOSIVE,
                "air_restricted": True,
                "warning": "Class 1.4G Pyrotechnic Airbag Inflator: Restricted from passenger aircraft. Requires hazmat ground/sea freight."
            }
        elif any(w in lower for w in ["gas shock", "pressurized strut", "nitrogen damper"]):
            return {
                "hazmat_class": HazmatClass.CLASS_2_GAS,
                "air_restricted": False,
                "warning": "Class 2.2 Non-Flammable Gas: Pressurized gas shock absorber under UN3164. Declared air freight only."
            }
        elif any(w in lower for w in ["lithium", "hybrid battery", "traction battery", "ev cell"]):
            return {
                "hazmat_class": HazmatClass.CLASS_9_LITHIUM,
                "air_restricted": True,
                "warning": "Class 9 Miscellaneous Dangerous Goods: High-capacity lithium-ion battery requires UN3480 certified packaging."
            }
        elif any(w in lower for w in ["brake fluid", "oil", "fluid", "aerosol", "lubricant"]):
            return {
                "hazmat_class": HazmatClass.CLASS_3_FLAMMABLE,
                "air_restricted": True,
                "warning": "Class 3 Flammable Liquid: Strict shipping declaration required."
            }
        
        return {
            "hazmat_class": HazmatClass.NONE,
            "air_restricted": False,
            "warning": None
        }

    @classmethod
    def calculate_landed_cost(
        cls,
        item_price_usd: float,
        weight_kg: float,
        destination_country: str = "SA",
        preferred_currency: Optional[str] = None,
        hazmat_class: HazmatClass = HazmatClass.NONE
    ) -> LandedCostEstimate:
        """
        Calculates CIF Landed Cost:
        CIF = Cost (Item) + Insurance + Freight + Customs Duty + Import VAT/GST
        """
        country_info = cls.COUNTRY_TARIFFS.get(destination_country.upper(), cls.COUNTRY_TARIFFS["SA"])
        target_currency = preferred_currency if preferred_currency in cls.EXCHANGE_RATES else country_info["currency"]
        rate = cls.EXCHANGE_RATES.get(target_currency, 1.0)

        # Shipping Calculation: Base $20 + $6.50/kg
        base_shipping = 20.00 + (weight_kg * 6.50)
        if hazmat_class != HazmatClass.NONE:
            base_shipping += 35.00 # Hazardous handling surcharge

        # Customs Duty (levied on CIF basis in most jurisdictions)
        duty_rate = country_info["duty"]
        customs_duty_usd = (item_price_usd + base_shipping) * duty_rate

        # Import VAT / GST (levied on [Item + Shipping + Duty])
        vat_rate = country_info["vat"]
        vat_usd = (item_price_usd + base_shipping + customs_duty_usd) * vat_rate

        # Total landed cost in USD
        total_usd = item_price_usd + base_shipping + customs_duty_usd + vat_usd

        # Converted local value
        total_local = round(total_usd * rate, 2)

        # Hazmat alerts
        hazmat_warning = None
        air_eligible = True
        if hazmat_class in [HazmatClass.CLASS_1_EXPLOSIVE, HazmatClass.CLASS_9_LITHIUM, HazmatClass.CLASS_3_FLAMMABLE]:
            hazmat_warning = "Restricted Cargo: Dangerous Goods shipping surcharge and specialized customs clearance required."
            air_eligible = False

        return LandedCostEstimate(
            item_price_usd=round(item_price_usd, 2),
            shipping_usd=round(base_shipping, 2),
            duty_rate_percent=duty_rate * 100,
            customs_duty_usd=round(customs_duty_usd, 2),
            tax_vat_percent=vat_rate * 100,
            tax_vat_usd=round(vat_usd, 2),
            total_landed_cost_usd=round(total_usd, 2),
            local_currency_code=target_currency,
            exchange_rate=rate,
            total_landed_cost_local=total_local,
            hazmat_warning=hazmat_warning,
            air_courier_eligible=air_eligible
        )

"""
Dual-Mode Query Parser, Automotive Synonym Expander, and ISO 3779 VIN Decoder
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from .normalizer import PartNormalizer

class QueryParser:
    # ISO 3779 WMI (World Manufacturer Identifier) Table
    WMI_DATABASE = {
        "1HG": {"make": "Honda", "country": "United States"},
        "1FA": {"make": "Ford", "country": "United States"},
        "1GC": {"make": "Chevrolet", "country": "United States"},
        "2T1": {"make": "Toyota", "country": "Canada"},
        "3VW": {"make": "Volkswagen", "country": "Mexico"},
        "JTD": {"make": "Toyota", "country": "Japan"},
        "JT2": {"make": "Toyota", "country": "Japan"},
        "JN1": {"make": "Nissan", "country": "Japan"},
        "JF1": {"make": "Subaru", "country": "Japan"},
        "JM1": {"make": "Mazda", "country": "Japan"},
        "WBA": {"make": "BMW", "country": "Germany"},
        "WBS": {"make": "BMW M", "country": "Germany"},
        "WDB": {"make": "Mercedes-Benz", "country": "Germany"},
        "WDD": {"make": "Mercedes-Benz", "country": "Germany"},
        "WAU": {"make": "Audi", "country": "Germany"},
        "WP0": {"make": "Porsche", "country": "Germany"},
        "SAL": {"make": "Land Rover", "country": "United Kingdom"},
        "SAJ": {"make": "Jaguar", "country": "United Kingdom"},
        "KMH": {"make": "Hyundai", "country": "South Korea"},
        "KNA": {"make": "Kia", "country": "South Korea"},
        "VF1": {"make": "Renault", "country": "France"},
        "VF3": {"make": "Peugeot", "country": "France"},
    }

    # ISO 3779 Year Character Map (Position 10)
    YEAR_CODES = {
        "A": 2010, "B": 2011, "C": 2012, "D": 2013, "E": 2014,
        "F": 2015, "G": 2016, "H": 2017, "J": 2018, "K": 2019,
        "L": 2020, "M": 2021, "N": 2022, "P": 2023, "R": 2024,
        "S": 2025, "T": 2026, "V": 2027, "W": 2028, "X": 2029, "Y": 2030,
        "1": 2001, "2": 2002, "3": 2003, "4": 2004, "5": 2005,
        "6": 2006, "7": 2007, "8": 2008, "9": 2009
    }

    # Automotive Synonym Expansion (Cross-Atlantic & Technical Synonyms)
    SYNONYM_GROUPS: List[List[str]] = [
        ["brake rotor", "brake disc", "disc rotor", "brake disk"],
        ["brake pads", "disc brake pad", "friction pads", "brake pad set"],
        ["maf sensor", "mass air flow sensor", "mass airflow sensor", "air flow meter", "afm", "maf", "air mass meter", "air mass sensor"],
        ["map sensor", "manifold absolute pressure sensor", "manifold pressure sensor"],
        ["oxygen sensor", "o2 sensor", "lambda sensor"],
        ["fender", "wing", "front wing", "quarter panel"],
        ["hood", "bonnet", "engine cover"],
        ["trunk", "boot", "tailgate", "decklid", "boot lid"],
        ["muffler", "silencer", "exhaust backbox", "exhaust box"],
        ["shock absorber", "damper", "strut", "suspension strut", "shock"],
        ["windshield", "windscreen", "front glass"],
        ["oil pan", "engine sump", "crankcase sump"],
        ["driveshaft", "propeller shaft", "prop shaft", "half shaft", "cv axle"],
        ["sway bar", "anti-roll bar", "stabilizer bar", "roll bar"],
        ["spark plug", "ignition plug", "glow plug"],
        ["alternator", "generator", "dynamo"],
        ["caliper", "brake caliper", "calliper"],
        ["racing seat", "bucket seat", "full bucket seat", "sports seat", "bride zeta"],
        ["headlight", "head light", "headlamp", "head lamp", "front lamp", "headlight assembly", "projector headlight", "xenon headlight"],
        ["taillight", "tail light", "taillamp", "tail lamp", "rear lamp", "rear light", "tail light assembly"],
        ["fog light", "fog lamp", "driving light"],
        ["bumper", "front bumper", "rear bumper", "bumper cover", "fascia", "bumper bar"],
        ["side mirror", "wing mirror", "door mirror", "rear view mirror"],
        ["radiator", "engine cooler", "cooling radiator", "heat exchanger"],
        ["intercooler", "charge air cooler"],
        ["turbocharger", "turbo", "turbocompressor", "turbo kit"],
        ["intake manifold", "inlet manifold", "intake plenum"],
        ["exhaust manifold", "header", "extractors", "downpipe"],
        ["coilover", "coilovers", "suspension kit", "lowering kit", "adjustable damper"],
        ["steering wheel", "sports steering wheel"]
    ]

    # Chassis & Model Knowledge Graph for Natural Language Search Queries
    CHASSIS_REGISTRY = {
        "S15": {"make": "Nissan", "model": "Silvia", "generation": "S15 (Spec-R / Spec-S)", "years": (1999, 2002), "pcdb_vehicle_id": 118920},
        "S14": {"make": "Nissan", "model": "Silvia / 240SX", "generation": "S14 (Kouki / Zenki)", "years": (1994, 1998), "pcdb_vehicle_id": 118915},
        "S13": {"make": "Nissan", "model": "Silvia / 180SX / 240SX", "generation": "S13", "years": (1989, 1994), "pcdb_vehicle_id": 118910},
        "180SX": {"make": "Nissan", "model": "180SX", "generation": "RPS13", "years": (1989, 1998), "pcdb_vehicle_id": 118911},
        "R34": {"make": "Nissan", "model": "Skyline / GT-R", "generation": "BNR34 / ER34", "years": (1998, 2002), "pcdb_vehicle_id": 118934},
        "R33": {"make": "Nissan", "model": "Skyline / GT-R", "generation": "BCNR33 / ECR33", "years": (1993, 1998), "pcdb_vehicle_id": 118933},
        "R32": {"make": "Nissan", "model": "Skyline / GT-R", "generation": "BNR32 / HCR32", "years": (1989, 1994), "pcdb_vehicle_id": 118932},
        "R35": {"make": "Nissan", "model": "GT-R", "generation": "R35", "years": (2008, 2024), "pcdb_vehicle_id": 118935},
        "350Z": {"make": "Nissan", "model": "350Z / Fairlady Z", "generation": "Z33", "years": (2003, 2008), "pcdb_vehicle_id": 118936},
        "370Z": {"make": "Nissan", "model": "370Z / Fairlady Z", "generation": "Z34", "years": (2009, 2020), "pcdb_vehicle_id": 118937},
        "MK4": {"make": "Toyota", "model": "Supra", "generation": "JZA80 (MK4)", "years": (1993, 2002), "pcdb_vehicle_id": 105480},
        "A80": {"make": "Toyota", "model": "Supra", "generation": "JZA80 (MK4)", "years": (1993, 2002), "pcdb_vehicle_id": 105480},
        "JZA80": {"make": "Toyota", "model": "Supra", "generation": "JZA80", "years": (1993, 2002), "pcdb_vehicle_id": 105480},
        "MK5": {"make": "Toyota", "model": "GR Supra", "generation": "A90 (MK5)", "years": (2019, 2025), "pcdb_vehicle_id": 105490},
        "A90": {"make": "Toyota", "model": "GR Supra", "generation": "A90 (MK5)", "years": (2019, 2025), "pcdb_vehicle_id": 105490},
        "AE86": {"make": "Toyota", "model": "Corolla Levin / Sprinter Trueno", "generation": "AE86", "years": (1983, 1987), "pcdb_vehicle_id": 105486},
        "FD": {"make": "Mazda", "model": "RX-7", "generation": "FD3S", "years": (1992, 2002), "pcdb_vehicle_id": 108713},
        "FD3S": {"make": "Mazda", "model": "RX-7", "generation": "FD3S", "years": (1992, 2002), "pcdb_vehicle_id": 108713},
        "FC": {"make": "Mazda", "model": "RX-7", "generation": "FC3S", "years": (1985, 1991), "pcdb_vehicle_id": 108712},
        "FC3S": {"make": "Mazda", "model": "RX-7", "generation": "FC3S", "years": (1985, 1991), "pcdb_vehicle_id": 108712},
        "MIATA": {"make": "Mazda", "model": "MX-5 Miata", "generation": "NA/NB/NC/ND", "years": (1990, 2025), "pcdb_vehicle_id": 108705},
        "E46": {"make": "BMW", "model": "3 Series / M3", "generation": "E46", "years": (1999, 2006), "pcdb_vehicle_id": 102446},
        "E36": {"make": "BMW", "model": "3 Series / M3", "generation": "E36", "years": (1992, 1999), "pcdb_vehicle_id": 102436},
        "E92": {"make": "BMW", "model": "3 Series / M3", "generation": "E92 / E90", "years": (2007, 2013), "pcdb_vehicle_id": 102492},
        "F30": {"make": "BMW", "model": "3 Series", "generation": "F30 / F80", "years": (2012, 2019), "pcdb_vehicle_id": 102430},
        "F80": {"make": "BMW", "model": "M3", "generation": "F80", "years": (2014, 2018), "pcdb_vehicle_id": 102480},
        "G20": {"make": "BMW", "model": "3 Series", "generation": "G20 / G80", "years": (2019, 2025), "pcdb_vehicle_id": 102420},
        "EVO": {"make": "Mitsubishi", "model": "Lancer Evolution", "generation": "Evo I-X", "years": (1992, 2016), "pcdb_vehicle_id": 109840},
        "CT9A": {"make": "Mitsubishi", "model": "Lancer Evolution VII/VIII/IX", "generation": "CT9A", "years": (2001, 2007), "pcdb_vehicle_id": 109849},
        "WRX": {"make": "Subaru", "model": "Impreza WRX / STI", "generation": "GC/GD/GR/VA", "years": (1992, 2021), "pcdb_vehicle_id": 114520},
        "GDB": {"make": "Subaru", "model": "Impreza WRX STI", "generation": "GDB (GD)", "years": (2000, 2007), "pcdb_vehicle_id": 114522},
        "CIVIC": {"make": "Honda", "model": "Civic", "generation": "All Generations", "years": (1990, 2025), "pcdb_vehicle_id": 104200},
        "S2000": {"make": "Honda", "model": "S2000", "generation": "AP1 / AP2", "years": (2000, 2009), "pcdb_vehicle_id": 104220},
        "INTEGRA": {"make": "Honda", "model": "Integra / RSX", "generation": "DC2 / DC5", "years": (1994, 2006), "pcdb_vehicle_id": 104225},
        "CORVETTE": {"make": "Chevrolet", "model": "Corvette", "generation": "C5/C6/C7/C8", "years": (1997, 2025), "pcdb_vehicle_id": 101850}
    }

    @classmethod
    def resolve_vehicle_context(cls, query: str) -> Optional[Dict[str, Any]]:
        """
        Extracts vehicle make, model, chassis, and year range from natural language query.
        e.g. 's15 head light' -> Nissan Silvia S15 (1999-2002)
             'e46 m3 bumper' -> BMW 3 Series / M3 E46 (1999-2006)
             'mk4 supra wing' -> Toyota Supra JZA80 (1993-2002)
        """
        upper_q = query.upper()
        tokens = re.split(r'[\s\-_]+', upper_q)

        # Check direct chassis codes
        for token in tokens:
            if token in cls.CHASSIS_REGISTRY:
                return cls.CHASSIS_REGISTRY[token]

        # Multi-word checks
        if "SILVIA" in upper_q:
            if "15" in upper_q or "S15" in upper_q:
                return cls.CHASSIS_REGISTRY["S15"]
            elif "14" in upper_q or "S14" in upper_q:
                return cls.CHASSIS_REGISTRY["S14"]
            elif "13" in upper_q or "S13" in upper_q:
                return cls.CHASSIS_REGISTRY["S13"]
            return {"make": "Nissan", "model": "Silvia", "generation": "S13/S14/S15", "years": (1989, 2002), "pcdb_vehicle_id": 118920}

        if "SUPRA" in upper_q:
            if "MK4" in upper_q or "A80" in upper_q or "4" in upper_q:
                return cls.CHASSIS_REGISTRY["MK4"]
            elif "MK5" in upper_q or "A90" in upper_q or "5" in upper_q:
                return cls.CHASSIS_REGISTRY["MK5"]
            return cls.CHASSIS_REGISTRY["MK4"]

        if "SKYLINE" in upper_q or "GTR" in upper_q or "GT-R" in upper_q:
            if "34" in upper_q or "R34" in upper_q:
                return cls.CHASSIS_REGISTRY["R34"]
            elif "33" in upper_q or "R33" in upper_q:
                return cls.CHASSIS_REGISTRY["R33"]
            elif "32" in upper_q or "R32" in upper_q:
                return cls.CHASSIS_REGISTRY["R32"]
            elif "35" in upper_q or "R35" in upper_q:
                return cls.CHASSIS_REGISTRY["R35"]

        return None

    @classmethod
    def decode_vin(cls, vin: str) -> Optional[Dict[str, Any]]:
        """
        Validates and extracts WMI, Model Year, and Country from a 17-character VIN.
        """
        vin_clean = re.sub(r"[^A-HJ-NPR-Z0-9]", "", vin.upper())
        if len(vin_clean) != 17:
            return None

        wmi = vin_clean[:3]
        year_char = vin_clean[9]

        mfg_info = cls.WMI_DATABASE.get(wmi, {"make": "Generic Vehicle", "country": "International"})
        year = cls.YEAR_CODES.get(year_char, 2020)

        return {
            "vin": vin_clean,
            "wmi": wmi,
            "make": mfg_info["make"],
            "country_of_manufacture": mfg_info["country"],
            "model_year": year,
            "serial_number": vin_clean[11:],
            "is_valid_format": True
        }

    @classmethod
    def expand_synonyms(cls, keyword: str) -> List[str]:
        """
        Given a part description keyword, returns all equivalent automotive synonyms.
        """
        normalized_kw = keyword.lower().strip()
        matched_synonyms = set()

        for group in cls.SYNONYM_GROUPS:
            if any(term in normalized_kw for term in group):
                for term in group:
                    matched_synonyms.add(term)

        if not matched_synonyms:
            matched_synonyms.add(normalized_kw)

        return list(matched_synonyms)

    @classmethod
    def extract_embedded_part_number(cls, query: str) -> Optional[str]:
        """
        Extracts candidate part number from mixed natural language queries.
        Handles hyphenated, slashed, spaced, and continuous part numbers.
        e.g. 'maf sensor with part number 2268069f01' -> '2268069F01'
             'brake pads for camry 04465-42180' -> '0446542180'
             '0 258 007 057' -> '0258007057'
        Does NOT falsely flag phrases with model/generation numbers (e.g. 'bride zeta 3 crfp').
        """
        clean_q = query.strip()
        stripped_full = re.sub(r"[^A-Za-z0-9]", "", clean_q).upper()
        if stripped_full in PartNormalizer.INTERCHANGE_GRAPH:
            return stripped_full

        tokens = re.findall(r'[A-Za-z0-9]+(?:[-./][A-Za-z0-9]+)*', clean_q)
        
        # If the entire query is multiple pure numeric chunks (e.g. '0 258 007 057' or '34 11 6 792 223'):
        if len(tokens) >= 2 and all(t.isdigit() for t in tokens) and len("".join(tokens)) >= 7:
            return "".join(tokens)

        for token in tokens:
            upper = token.upper()
            alnum = re.sub(r"[^A-Za-z0-9]", "", upper)

            # Skip 4-digit years (e.g. 1990 - 2035)
            if len(alnum) == 4 and alnum.isdigit() and 1980 <= int(alnum) <= 2035:
                continue

            # Skip single digit (e.g. '3', '4', '1') or short numbers
            if len(alnum) <= 3:
                continue

            # Skip displacement e.g. 2.0, 3.5, 2.5L
            if re.match(r'^\d\.\d[A-Z]?$', upper):
                continue

            # A real automotive part number MUST have:
            # 1. BOTH letters and digits within the same token (e.g. 2268069F01, A36608E60, 16600JF00A, ACT1210)
            # 2. OR contain punctuation separator with digits (e.g. 22680-69F01, 04465-42180, 34-11-6-792-223)
            # 3. OR be purely numeric with at least 6 digits (e.g. 34116792223, 0446542180)
            has_digits = any(c.isdigit() for c in alnum)
            has_letters = any(c.isalpha() for c in alnum)
            has_hyphen_or_dot = any(sep in token for sep in ["-", ".", "/"])

            is_valid_pn = False
            if has_digits and has_letters and 5 <= len(alnum) <= 18:
                is_valid_pn = True
            elif has_digits and has_hyphen_or_dot and 5 <= len(alnum) <= 18:
                is_valid_pn = True
            elif alnum.isdigit() and 6 <= len(alnum) <= 18:
                is_valid_pn = True

            if is_valid_pn:
                return alnum

        return None

    @classmethod
    def parse_query(cls, query: str, search_mode: str = "auto") -> Tuple[str, Optional[str], List[str], Optional[Dict[str, Any]]]:
        """
        Detects query intention:
         1. 'vin': exactly 17 alphanumeric chars
         2. 'part_number': contains alphanumeric part pattern or embedded part number
         3. 'keyword': natural language full-text with synonym expansion
        Returns (detected_mode, cleaned_part_number, synonyms, vin_dict)
        """
        clean_input = query.strip()
        if not clean_input:
            return "keyword", None, [], None

        # 0. User explicit override from UI radio buttons
        if search_mode in ["keyword", "text"]:
            synonyms = cls.expand_synonyms(clean_input)
            return "keyword", None, synonyms, None

        if search_mode in ["part_number", "pn"]:
            alnum_only = re.sub(r"[^A-Za-z0-9]", "", clean_input).upper()
            return "part_number", alnum_only, [], None

        # 1. Check if VIN (17 chars, no I, O, Q)
        alnum_only = re.sub(r"[^A-Za-z0-9]", "", clean_input).upper()
        if len(alnum_only) == 17 and not any(bad_char in alnum_only for bad_char in ["I", "O", "Q"]):
            vin_data = cls.decode_vin(alnum_only)
            if vin_data:
                return "vin", None, [], vin_data

        # 2. Extract potential embedded part number
        embedded_pn = cls.extract_embedded_part_number(clean_input)
        if embedded_pn:
            # Also extract remaining text for keyword matching/synonyms
            # Remove the detected token and common glue words
            remaining = re.sub(r'\b[A-Za-z0-9\-./]{5,18}\b', ' ', clean_input, flags=re.IGNORECASE)
            remaining = re.sub(r'\b(with|part|parts|number|no|pn|for|the|and|in|of|oem|genuine)\b', ' ', remaining, flags=re.IGNORECASE)
            remaining_clean = " ".join(remaining.split()).strip()
            synonyms = cls.expand_synonyms(remaining_clean) if remaining_clean else []
            return "part_number", embedded_pn, synonyms, None

        # 3. Otherwise treat as natural language automotive keyword
        synonyms = cls.expand_synonyms(clean_input)
        return "keyword", None, synonyms, None

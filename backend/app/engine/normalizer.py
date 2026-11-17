"""
Part Number Normalizer & Cross-Reference Interchange Engine
Strips punctuation, canonicalizes numbers, and manages OEM-to-Aftermarket equivalence.
"""

import re
from typing import Set, List, Dict

class PartNormalizer:
    # Interchange Knowledge Graph (Canonical interchange groups)
    # Allows bidirectional lookup: OEM <-> OES <-> Aftermarket
    INTERCHANGE_GRAPH: Dict[str, Set[str]] = {
        # BMW F30 / G20 Front Brake Rotor
        "34116792223": {"34116792223", "09C39913", "150348320", "55523", "DF6603S", "34116855006"},
        "09C39913": {"34116792223", "09C39913", "150348320", "55523", "DF6603S", "34116855006"},
        
        # Toyota Camry / RAV4 Front Brake Pads
        "0446542180": {"0446542180", "04465AZ001", "ACT1210", "BC1210", "D1210", "SP2138", "0446542190"},
        "ACT1210": {"0446542180", "04465AZ001", "ACT1210", "BC1210", "D1210", "SP2138"},
        
        # Mercedes-Benz C300 / E350 Bosch Oxygen Sensor
        "0045420718": {"0045420718", "0258007057", "A0045420718", "17014", "ES2031712B1"},
        "0258007057": {"0045420718", "0258007057", "A0045420718", "17014", "ES2031712B1"},

        # Nissan GT-R R35 / 370Z Twin Turbo / Fuel Injector
        "16600JF00A": {"16600JF00A", "0280158130", "F314", "16600EY00A"},

        # Porsche 911 / Cayman Bilstein B6 Damper / Strut
        "99734304104": {"99734304104", "24062899", "35122074", "V364127"},
        
        # Honda Civic / Accord Denso Alternator
        "31100R40A01": {"31100R40A01", "1042105910", "AL1298X", "2100656"},

        # Nissan Silvia S14 / S15 SR20DET Mass Air Flow (MAF) Sensor
        "2268069F01": {"2268069F01", "2268069F00", "A36608E60", "A36608", "22680AD21A", "AFH7014", "MAF0042"},
        "2268069F00": {"2268069F01", "2268069F00", "A36608E60", "A36608", "22680AD21A", "AFH7014", "MAF0042"},
        "A36608E60": {"2268069F01", "2268069F00", "A36608E60", "A36608", "22680AD21A", "AFH7014", "MAF0042"},
        "A36608": {"2268069F01", "2268069F00", "A36608E60", "A36608", "22680AD21A", "AFH7014", "MAF0042"}
    }

    @staticmethod
    def clean(part_number: str) -> str:
        """
        Strips spaces, hyphens, slashes, dots, and special characters.
        Canonicalizes to uppercase alphanumeric characters.
        Example: '34-11-6-792-223' -> '34116792223'
                 '0 258 007 057'  -> '0258007057'
                 'A-004.542/0718' -> 'A0045420718'
        """
        if not part_number:
            return ""
        # Remove anything that isn't ASCII alphanumeric
        cleaned = re.sub(r"[^A-Za-z0-9]", "", part_number).upper()
        return cleaned

    @classmethod
    def get_interchange_numbers(cls, part_number: str) -> Set[str]:
        """
        Returns all known equivalent OEM and aftermarket part numbers
        for the given input number.
        """
        cleaned = cls.clean(part_number)
        interchange = set()
        
        # Direct graph lookup
        if cleaned in cls.INTERCHANGE_GRAPH:
            interchange.update(cls.INTERCHANGE_GRAPH[cleaned])
        
        # Prefix / suffix tolerance check (e.g. Mercedes 'A' prefix)
        if cleaned.startswith("A") and cleaned[1:] in cls.INTERCHANGE_GRAPH:
            interchange.update(cls.INTERCHANGE_GRAPH[cleaned[1:]])
            
        interchange.add(cleaned)
        return interchange

    @classmethod
    def is_match(cls, searched_pn: str, target_pn: str, target_interchange: List[str] = None) -> bool:
        """
        Verifies if searched part number matches target part number or any of its interchange numbers.
        """
        clean_search = cls.clean(searched_pn)
        clean_target = cls.clean(target_pn)
        
        if clean_search == clean_target:
            return True
            
        if clean_search in cls.get_interchange_numbers(clean_target):
            return True
            
        if target_interchange:
            clean_interchanges = {cls.clean(ic) for ic in target_interchange}
            if clean_search in clean_interchanges:
                return True
                
        return False

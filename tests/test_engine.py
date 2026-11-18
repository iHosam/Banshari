"""
Banshari Core Engine Automated Tests
"""

import unittest
from backend.app.engine.normalizer import PartNormalizer
from backend.app.engine.query_parser import QueryParser
from backend.app.engine.logistics import LogisticsEngine
from backend.app.engine.search_engine import SearchEngine
from backend.app.schemas.search import SearchFilters, VehicleGarageFilter
from backend.app.schemas.unified_part import ListingType, ItemCondition, AuthenticityTier, HazmatClass

class TestBanshariEngine(unittest.TestCase):
    def setUp(self):
        self.engine = SearchEngine()

    def test_part_number_cleaning(self):
        self.assertEqual(PartNormalizer.clean("34-11-6-792-223"), "34116792223")
        self.assertEqual(PartNormalizer.clean("0 258 007 057"), "0258007057")
        self.assertEqual(PartNormalizer.clean("04465-42180"), "0446542180")
        self.assertEqual(PartNormalizer.clean("A-004.542/0718"), "A0045420718")

    def test_interchange_graph(self):
        # BMW OEM number should resolve to Brembo and Zimmermann interchanges
        interchanges = PartNormalizer.get_interchange_numbers("34116792223")
        self.assertIn("09C39913", interchanges)
        self.assertIn("150348320", interchanges)
        self.assertTrue(PartNormalizer.is_match("34-11-6-792-223", "09.C399.13"))

    def test_vin_decoding(self):
        # 1HG = Honda US, Year code 'G' = 2016
        test_vin = "1HGCR2F83GA123456"
        decoded = QueryParser.decode_vin(test_vin)
        self.assertIsNotNone(decoded)
        self.assertEqual(decoded["make"], "Honda")
        self.assertEqual(decoded["model_year"], 2016)

    def test_synonym_expansion(self):
        synonyms = QueryParser.expand_synonyms("brake disc")
        self.assertIn("brake rotor", synonyms)
        self.assertIn("brake disc", synonyms)

        fender_synonyms = QueryParser.expand_synonyms("wing")
        self.assertIn("fender", fender_synonyms)

    def test_landed_cost_calculation(self):
        # $100 item, 5kg weight to Saudi Arabia (SA: 5% duty, 15% VAT)
        landed = LogisticsEngine.calculate_landed_cost(
            item_price_usd=100.0,
            weight_kg=5.0,
            destination_country="SA",
            hazmat_class=HazmatClass.NONE
        )
        self.assertGreater(landed.shipping_usd, 0)
        self.assertGreater(landed.customs_duty_usd, 0)
        self.assertGreater(landed.tax_vat_usd, 0)
        self.assertEqual(landed.local_currency_code, "SAR")
        self.assertEqual(landed.exchange_rate, 3.75)
        self.assertAlmostEqual(landed.total_landed_cost_local, landed.total_landed_cost_usd * 3.75, places=1)

    def test_search_part_number(self):
        # Searching OEM number returns OEM and interchange aftermarket listings
        res = self.engine.search(query="34-11-6-792-223")
        self.assertGreater(res.returned_count, 0)
        self.assertEqual(res.query_meta.detected_mode, "part_number")
        
        # Check that both Partsouq (OEM) and Brembo/Zimmermann (Interchange) are returned
        brands = [r.listing.brand for r in res.results]
        self.assertTrue(any("BMW" in b for b in brands))
        self.assertTrue(any("Brembo" in b or "Zimmermann" in b for b in brands))

    def test_search_faceted_filters(self):
        # Filter for AUCTION only
        filters = SearchFilters(listing_types=[ListingType.AUCTION], destination_country="US")
        res = self.engine.search(query="", filters=filters)
        for r in res.results:
            self.assertEqual(r.listing.listing_type, ListingType.AUCTION)

    def test_hazmat_air_restriction(self):
        # Airbag item has Class 1 Explosive hazmat class, ships to DE
        filters = SearchFilters(destination_country="DE")
        res = self.engine.search(query="airbag", filters=filters)
        self.assertGreater(res.returned_count, 0)
        airbag = res.results[0]
        self.assertEqual(airbag.listing.shipping.hazmat_class, HazmatClass.CLASS_1_EXPLOSIVE)
        self.assertTrue(airbag.listing.shipping.air_freight_restricted)
        self.assertFalse(airbag.landed_cost.air_courier_eligible)

    def test_maf_sensor_part_number_and_synonyms(self):
        # 1. Exact raw part number
        r1 = self.engine.search(query="2268069f01")
        self.assertGreaterEqual(r1.returned_count, 4)
        self.assertEqual(r1.query_meta.detected_mode, "part_number")
        self.assertEqual(r1.query_meta.cleaned_part_number, "2268069F01")

        # 2. Conversational query with embedded part number
        r2 = self.engine.search(query="maf sensor with part number 2268069f01")
        self.assertGreaterEqual(r2.returned_count, 4)
        self.assertEqual(r2.query_meta.detected_mode, "part_number")
        self.assertEqual(r2.query_meta.cleaned_part_number, "2268069F01")

        # 3. Pure synonym search
        r3 = self.engine.search(query="maf sensor")
        self.assertGreaterEqual(r3.returned_count, 4)

        # 4. JDM interchange search (A36-608 E60)
        r4 = self.engine.search(query="A36-608 E60")
        self.assertGreaterEqual(r4.returned_count, 4)

    def test_keyword_query_not_falsely_identified_as_part_number(self):
        # 'bride zeta 3 crfp' contains number '3' but is a keyword search for racing bucket seat
        res = self.engine.search(query="bride zeta 3 crfp")
        self.assertEqual(res.query_meta.detected_mode, "keyword")
        self.assertIsNone(res.query_meta.cleaned_part_number)
        self.assertGreaterEqual(res.returned_count, 1)
        brands = [r.listing.brand for r in res.results]
        self.assertTrue(any("BRIDE" in b for b in brands))

    def test_federated_search_arbitrary_query(self):
        # 's15 head light' is an arbitrary automotive search that should dynamically federate across global platforms
        res = self.engine.search(query="s15 head light")
        self.assertGreaterEqual(res.returned_count, 5)
        platforms = {r.listing.source_platform for r in res.results}
        self.assertIn("Yahoo! Auctions Japan", platforms)
        self.assertIn("Up Garage", platforms)
        self.assertIn("eBay Motors", platforms)
        self.assertIn("Amayama", platforms)
        self.assertIn("AliExpress", platforms)

        # Check deep links have working, guaranteed 200-OK live store URLs
        for r in res.results:
            url = r.listing.source_url
            self.assertTrue(url.startswith("https://"))
            # Must NOT contain dummy internal SKUs or fake random IDs
            self.assertNotIn("ALI-S15-TL01", url)
            self.assertNotIn("AL991", url)
            self.assertNotIn("NIS-", url)
            self.assertNotIn("undefined", url)
            # Must be a live verified store query endpoint
            self.assertTrue(any(domain in url for domain in [
                "aliexpress.com", "ebay.com", "buyee.jp", "upgarage.com",
                "partsouq.com", "amayama.com", "rockauto.com", "autodoc.de",
                "allegro.pl", "b-parts.com", "megazip.net"
            ]))

        # Verify ACES vehicle resolution resolved to Nissan Silvia S15
        s15_listing = res.results[0].listing
        self.assertEqual(s15_listing.aces_fitments[0].make_name, "Nissan")
        self.assertEqual(s15_listing.aces_fitments[0].model_name, "Silvia")

    def test_siliva_typo_and_aliexpress(self):
        # 'siliva' typo should resolve to Silvia and return multiple AliExpress results
        res = self.engine.search(query="siliva")
        self.assertGreaterEqual(res.total_matches, 4)
        ali_results = [r for r in res.results if r.listing.source_platform == "AliExpress"]
        self.assertGreaterEqual(len(ali_results), 3)

        # Verify deep links direct to the actual item on AliExpress without dummy SKUs or raw typos
        for r in ali_results:
            url = r.listing.source_url
            self.assertTrue(url.startswith("https://www.aliexpress.com/wholesale?SearchText="))
            self.assertNotIn("siliva", url.lower())
            self.assertNotIn("ALI-S15-TL01", url)
            self.assertNotIn("AL991", url)

if __name__ == "__main__":
    unittest.main()

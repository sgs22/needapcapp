from django.test import TestCase
from .sources.currys.client import CurrysScraper
from .sources.laptopsdirect.client import LaptopsDirectScraper


# class TestCurrysScraper(TestCase):
#     def setUp(self) -> None:
#         self.scraper = CurrysScraper()

#     def test_query_products(self):
#         products = self.scraper.query_product_segment()
#         self.assertEquals(len(products) > 0, True)

#     def test_soup_session_valid(self):
#         session = self.scraper.get_session()
#         self.assertEquals(session.status_code, 200)


class TestLaptopsDirectScraper(TestCase):
    def setUp(self) -> None:
        self.scraper = LaptopsDirectScraper()

    def test_session_valid(self):
        session = self.scraper.get_session(self.scraper.base_url)
        self.assertEquals(session.status_code, 200)

    def test_query_product_page_type(self):
        products = self.scraper.query_product_page(1)
        self.assertIsInstance(products, list)

    def test_process_product_page_type(self):
        product_schemas = self.scraper.process_product_page()
        for product in product_schemas:
            self.scraper.create_product(product)
        self.assertIsInstance(product_schemas, list)

    def test_product_data(self):
        pass

    def tearDown(self) -> None:
        # delete all products that were created
        pass

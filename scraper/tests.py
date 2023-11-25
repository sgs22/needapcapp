from django.test import TestCase
from .models import CurrysScraper, LaptopsDirectScraper


class TestCurrysScraper(TestCase):
    def setUp(self) -> None:
        self.scraper = CurrysScraper()

    def test_query_products(self):
        products = self.scraper.query_product_segment()
        print(products)
        self.assertEquals(len(products) > 0, True)

    def test_soup_session_valid(self):
        session = self.scraper.get_session(self.scraper.base_url)
        self.assertEquals(session.status_code, 200)


class TestLaptopsDirectScraper(TestCase):
    def setUp(self) -> None:
        self.scraper = LaptopsDirectScraper()

    def test_session_valid(self):
        session = self.scraper.get_session(self.scraper.base_url)
        self.assertEquals(session.status_code, 200)

    def test_query_laptop_segment(self):
        products = self.scraper.query_laptop_segment()
        self.assertEquals(len(products) > 0, True)

    def test_product_data(self):
        # check can get session (valid connection)
        # get all products and urls return [0]
        # for the porduct test getting all details from product url
        # save that data as a new product

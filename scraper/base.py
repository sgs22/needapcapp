from bs4 import BeautifulSoup
import requests


class ProductScraper:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

    def search_products(self, search_query, endpoint: str):
        search_query = search_query.replace(' ', '+')
        url = f"{self.base_url}{endpoint}"

        soup = self.get_soup_session(url)
        products = []

        for product in soup.find_all('article', class_='product'):
            name = product.find('strong', class_='productTitle').text.strip()
            price = product.find('strong', class_='current-price').text.strip()
            products.append({'name': name, 'price': price})

        return products

    def query_product_segment(self, url: str):
        soup = self.get_soup_session(url)
        products = []

        for product in soup.find_all("div", class_="product-tile  "):
            name = product.find('h2', class_='pdp-grid-product-name')
            link = product.find('a', class_='link text-truncate pdpLink')
            href = link['href']
            products.append({'name': name, 'url': href})
        return products

    def get_product_details_from_list(self, products: list):
        for item in products:
            response = self.get_soup_session(item.get('url'))
            response.find_all()

    def get_soup_session(self, url: str) -> BeautifulSoup:
        session = self.session.get(url)
        soup = BeautifulSoup(session.content, 'html.parser')
        return soup

    def get_session(self, url: str):
        session = self.session.get(url)
        return session

    def paginate(self, per_page: int, total: int):
        pages = []
        for i in range(0, total, per_page):
            pages.append(i)
        return pages

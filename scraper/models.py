from django.db import models

import requests
from bs4 import BeautifulSoup


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    product_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(max_length=5000)
    additional_info = models.JSONField(blank=True, null=True)
    # image = models.ImageField(upload_to='products', blank=True, null=True)
    image_urls = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name

    @classmethod
    def new(cls, *args, **kwargs):
        return cls.objects.create(*args, **kwargs)

    @classmethod
    def create_from_product_data(cls, product_data: dict):
        if not cls.valid_product_data(product_data):
            return None
        create_product = cls.objects.create(
            name=product_data.get('name'), price=product_data.get('price', 0),
            product_code=product_data.get('product_code', ''),
            description=product_data.get('description', ''),
            additional_info=product_data.get('additional_info', {}),
            image_urls=product_data.get('image_urls', {})
        )
        if create_product:
            return create_product
        return None

    @classmethod
    def valid_product_data(cls, product_data: dict) -> bool:
        valid = True
        required_fields = ['name', 'price']
        for k, v in product_data:
            if not k in required_fields:
                valid = False
        return valid

    @classmethod
    def get_model_fields(cls) -> list:
        fields = cls._meta.fields
        field_names = [field.name for field in fields]
        return field_names


class CurrysScraper:
    def __init__(self):
        self.base_url = 'https://www.currys.co.uk'
        self.session = requests.Session()
        self.session.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        }

    def search_products(self, search_query):
        search_query = search_query.replace(' ', '+')
        url = f"{self.base_url}/gbuk/search-keywords/xx_xx_xx_xx_xx/{search_query}/xx-criteria.html"

        response = self.session.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        products = []

        for product in soup.find_all('article', class_='product'):
            name = product.find('strong', class_='productTitle').text.strip()
            price = product.find('strong', class_='current-price').text.strip()

            products.append({'name': name, 'price': price})

        return products

    def query_product_segment(self):
        url = "https://www.currys.co.uk/computing/laptops/laptops?start=0&sz=5&viewtype=listView"
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


class LaptopsDirectScraper(ProductScraper):
    def __init__(self):
        super().__init__('https://www.laptopsdirect.co.uk')

    def query_laptop_segment(self) -> list:
        url = 'https://www.laptopsdirect.co.uk/ct/laptops-and-netbooks/laptops?pageNumber=1'
        # pages = self.paginate(48, 954)
        page_blocks = self.paginate(48, 50)
        page = 1
        products = []
        for page in page_blocks:
            print(f'processing product range: {page_blocks}')
            url = f'https://www.laptopsdirect.co.uk/ct/laptops-and-netbooks/laptops?pageNumber={page}'
            soup = self.get_soup_session(url)
            product_list = soup.find_all(class_='OfferBox')
            for product in product_list:
                name = product.find('a', class_='offerboxtitle').text.strip()
                link = product.find('a', class_='offerboxtitle')['href']
                products.append(
                    {'product_name': name, 'product_url': f'{self.base_url}{link}'})
            page += 1
        print(len(products))
        print(products)
        return products

    def get_product_details(self, product_url: str):
        soup = self.get_soup_session(product_url)
        name = soup.find('span', class_='title')
        price = soup.find('span', class_='VersionOfferPrice')
        price = price.find('img')['alt']  # type: ignore
        product_code = soup.find(
            'span', class_='sku text-grey margin-right-15')
        description = soup.find_all('div', class_='ProductDescription')
        additional_info = soup.find('div', class_='specData')
        image_urls = soup.find('a', class_='fancyboxThumb')
        if image_urls:
            image_urls = image_urls['href']  # type: ignore
        product_data = {'name': name, 'price': price,
                        'product_code': product_code,
                        'description': description,
                        'additional_info': {'info': additional_info},
                        'image_urls': [image_urls]
                        }
        print('product_data', product_data)
        return product_data

    def create_product(self, product_data: dict):
        create_product = Product.create_from_product_data(product_data)
        if create_product:
            return True
        return False

    def process(self):
        products = self.query_laptop_segment()
        if products:
            for product in products:
                if product.get('product_url'):
                    product_data = self.get_product_details(
                        product.get('product_url'))
                    if product_data:
                        success = self.create_product(product_data)
                        print('successfully created') if success else print(
                            'fail creating product')
        return True

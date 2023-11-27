from scraper.base import ProductScraper
from scraper.models import Product


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

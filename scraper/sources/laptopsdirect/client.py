from scraper.base import ProductScraper
from scraper.models import Product


class LaptopsDirectScraper(ProductScraper):
    def __init__(self):
        super().__init__('https://www.laptopsdirect.co.uk')

    def query_laptop_segment(self) -> list:
        url = f'{self.base_url}/ct/laptops-and-netbooks/laptops?pageNumber=1'
        page_blocks = self.paginate(48, 50)
        page = 1
        products = []
        for page in page_blocks:
            url = f'{self.base_url}/ct/laptops-and-netbooks/laptops?pageNumber={page}'
            soup = self.get_soup_session(url)
            product_list = soup.find_all(class_='OfferBox')
            for product in product_list:
                name = product.find('a', class_='offerboxtitle').text.strip()
                link = product.find('a', class_='offerboxtitle')['href']
                products.append(
                    {'product_name': name, 'product_url': f'{self.base_url}{link}'})
            page += 1
        return products

    def get_product_details(self, product_url: str) -> dict:
        soup = self.get_soup_session(product_url)
        name = soup.find('span', class_='title').text  # type: ignore
        price = soup.find('span', class_='VersionOfferPrice')
        price_img = price.find('img') if price else None
        if price_img:
            price = price_img['alt'].replace('£', '')  # type: ignore
        product_code = soup.find(
            'span', class_='sku text-grey margin-right-15').text  # type: ignore
        product_code = product_code.replace('SKU: ', '')
        image_urls = soup.find('a', class_='fancyboxThumb')
        if image_urls:
            image_urls = image_urls['href']  # type: ignore
            image_urls = f'{self.base_url}{image_urls}'  # type: ignore
        description = soup.find('div', class_='ProductDescription')
        specs = soup.find('div', id='specs')
        additional_info = self.format_specification(specs)
        product_data = {
            'name': name,
            'price': price,
            'product_code': product_code,
            'description': description,
            'additional_info': additional_info,
            'image_urls': [image_urls],
            'retailer': 'Laptops Direct',
            'retailer_sku_id': f'LD-{product_code[:22]}',
        }
        return product_data

    def query_product_page(self, page: int) -> list[dict]:
        url = f'{self.base_url}/ct/laptops-and-netbooks/laptops?pageNumber={page}'
        soup = self.get_soup_session(url)
        product_list = soup.find_all(class_='OfferBox')
        products = []
        for product in product_list:
            name = product.find('a', class_='offerboxtitle').text.strip()
            link = product.find('a', class_='offerboxtitle')['href']
            products.append(
                {'product_name': name, 'product_url': f'{self.base_url}{link}'})
        return products

    def create_product(self, product_data: dict):
        create_product = Product.create_from_product_data(product_data)
        if create_product:
            print(create_product.retailer_sku_id)
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

    def process_product_page(self) -> list[dict]:
        product_schemas = []
        products = self.query_product_page(1)
        for product in products:
            url = product.get('product_url')
            if url:
                product_data = self.get_product_details(url)
                if product_data:
                    product_schemas.append(product_data)
        return product_schemas

    @staticmethod
    def format_specification(specification) -> list:
        additional_info_data = []
        table_body = specification.find('tbody')
        table_row = [tr.find_all('td') for tr in table_body.find_all('tr')]
        for data in table_row:
            key = data[0].text.strip()
            value = data[1].text.strip() if len(data) > 1 else ''
            additional_info_data.append({key: value})
        return additional_info_data

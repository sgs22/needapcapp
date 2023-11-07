import requests
from bs4 import BeautifulSoup

class BSWebScraper:
    def __init__(self, base_url: str) -> None:
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'}

    def query_products_with_class(self, url_path: str, class_name: str):
        response = self.session.get(f'{self.base_url}{url_path}')
        soup = BeautifulSoup(response.content, 'html.parser')
        items = []
        count = 0
        for item in soup.find_all(class_=class_name):
            count += 1
            item_name = item.find('a', class_='offerboxtitle').text.strip()
            product_url = item.find('a', class_='offerboxtitle')['href']
            item_price = item.find('span', class_='offerprice').text.strip()
            formatted_price = item_price.replace('£', '')
            items.append({'name': item_name, 'price': float(formatted_price), 'url': product_url})

        

class LaptopsDirect(BSWebScraper):
    def __init__(self):
        super().__init__('https://www.laptopsdirect.co.uk/')

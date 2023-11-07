from django.db import models

import requests
from bs4 import BeautifulSoup


class Product(models.Model):
    name = models.CharField()
    price = models.FloatField()
    product_code = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    additional_info = models.JSONField(blank=True, null=True)
    image = models.ImageField(upload_to='products', blank=True, null=True)
    image_urls = models.JSONField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return self.name
    
    
class CurrysScraper:
    def __init__(self):
        self.base_url = 'https://www.currys.co.uk'
        self.session = requests.Session()
        self.session.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

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
    
    def get_product_details(self, product_code: str):
        url = f'https://www.currys.co.uk/search?q={product_code}'

        response = self.session.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')
        print(soup)
        product = {}
        product_name = soup.find('h1', class_='product-name').text.strip()
        product_price = soup.find('span', class_='value').text.strip()
        product.append({'name': product_name, 'price': product_price})
        print(product)


# if __name__ == "__main__":
#     scraper = CurrysScraper()
#     scraper.get_product_details('359445')

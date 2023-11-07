from django.http import HttpResponse
from django.shortcuts import render
from scraper.sources.laptopsdirect.client import LaptopsDirect

def test_scraper_view(request):
    LaptopsDirect().query_products_with_class('ct/laptops-and-netbooks/laptops?itemsPerPage=48', 'OfferBox')
    return HttpResponse('Hello, World!')

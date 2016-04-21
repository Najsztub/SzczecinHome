# -*- coding: utf-8 -*-
import scrapy


class SzczecinSpider(scrapy.Spider):
    name = "szczecin"
    allowed_domains = ["http://otodom.pl/sprzedaz/mieszkanie/szczecin/"]
    start_urls = (
        'http://www.http://otodom.pl/sprzedaz/mieszkanie/szczecin/?search[dist]=0/',
    )

    def parse(self, response):
        pass

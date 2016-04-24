# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SzczecinSpider(CrawlSpider):
    name = "szczecin"
    allowed_domains = ["otodom.pl"]
    start_urls = (
        'http://otodom.pl/sprzedaz/mieszkanie/szczecin/?search[dist]=0',
    )
    rules = (
        Rule(LinkExtractor(allow='\.html$', ), follow=True, callback='parse_page'),
        Rule(LinkExtractor(allow='sprzedaz/mieszkanie/szczecin/\?search%5Bdescription%5D=1&search%5Bdist%5D=0&page=[0-9]+'), follow=True,
        ),
        Rule(LinkExtractor(deny=('dom-'))),
        Rule(LinkExtractor(deny=('dzialka'))),
        Rule(LinkExtractor(deny=('garaz'))),
        Rule(LinkExtractor(deny=('hala'))),
        Rule(LinkExtractor(deny=('uzytkowy'))),
        Rule(LinkExtractor(deny=('wynajem'))),
    )

    def parse_page(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

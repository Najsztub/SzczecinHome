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
        Rule(LinkExtractor(allow=('page=[0-9]+'),
             restrict_xpaths=('//ul[@class="pager"]',)),
             follow=True,
        ),
        Rule(LinkExtractor(allow=('\.html' ),
                           restrict_xpaths=('//div[@class="col-md-content"]',),
                           deny=('dom-','dzialka','garaz','hala', 'uzytkowy', 'wynajem')), callback='parse_page'),
        
    )

    def parse_page(self, response):
        self.logger.info('Hi, this is an item page! %s', response.url)
        '''filename = response.url.split("/")[-1]
        with open(filename, 'wb') as f:
            f.write(response.body)'''

'''Rule(LinkExtractor(deny=('dom-'))),
Rule(LinkExtractor(deny=('dzialka'))),
Rule(LinkExtractor(deny=('garaz'))),
Rule(LinkExtractor(deny=('hala'))),
Rule(LinkExtractor(deny=('uzytkowy'))),
Rule(LinkExtractor(deny=('wynajem'))),
'''
#Rule(LinkExtractor(allow='\.html$', ), follow=True, callback='parse_page')

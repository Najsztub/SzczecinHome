# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class SzczecinSpider(CrawlSpider):
    scraped = 0
    name = "szczecin"
    allowed_domains = ["otodom.pl"]
    start_urls = (
        'http://otodom.pl/sprzedaz/mieszkanie/szczecin/?search[dist]=0',
    )
    rules = (
        # Follow pages
        Rule(LinkExtractor(allow=('page=[0-9]+'),
             restrict_xpaths=('//ul[@class="pager"]',)),
             follow=True,
        ),
        # Extract only adds
        Rule(LinkExtractor(allow=('\.html' ),
                           restrict_xpaths=('//div[@class="col-md-content"]',),
                           deny=('dom-','dzialka','garaz','hala', 'uzytkowy',
                                 'wynajem')),
             callback='parse_page',
        ),
        
    )

    def parse_page(self, response):
        scraped += 1
        if scraped % 100 == 0:
            self.logger.info('scraped %d sites', scraped)
        
        # Create item
        item = HomespiderItem()
        
        # Extract dwelling details
        main_data = response.xpath(
            '//ul[@class="main-list"]/li/span/strong/text()'
        ).extract()

        item['url'] = response.url
        item['price'] = main_data[0]
        item['pow'] = main_data[1]
        item['rooms'] = main_data[2]
        item['floor'] = main_data[3]
        
        # Extract dwelling address
        address = response.xpath('//address/p/a/text()').extract()
            
        item['location'] = ', '.join(address)
        item['town'] = address[1]
        item['sellType'] = address[0]
        
        # Add short title
        item['description'] = response.xpath(
            '//header[@class="col-md-offer-content"]/h1/text()'
        ).extract()
        
        # Add house description paragraphs 
        opis = response.xpath(
            '//div[@class="col-md-offer-content"]/p/text()'
        ).extract()

        item['details'] = ''.join(opis)
        
        # Return the filled item
        return item

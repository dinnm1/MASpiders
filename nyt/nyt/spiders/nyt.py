# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from grpc._channel import _start_unary_request
from scrapy.spiders import CrawlSpider, Rule
from nyt.items import NewsItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re

class TestSpider(CrawlSpider):

    def __init__(self, year=None, *args, **kwargs):
        self.year = year
        self.start_urls = ['http://spiderbites.nytimes.com/' + year + '/']  # The starting page for the crawls
        self.rules = (Rule(LxmlLinkExtractor(
        # allow=(self.year)),
        # allow=(r"nytimes.com/"+re.escape(self.year))),
        # allow=(r"nytimes.com/" + re.escape(self.start_urls))),
        #allow=("1995")),
        #allow=(year)),
        allow=('nytimes.com/'+year)),
        follow=True,
        callback='parse_item'),)

        super(TestSpider, self).__init__(*args, **kwargs)




    name = "nyt" #This name will help while running the crawler itself
    allowed_domains = ["nytimes.com"] #which domains are accessible for this crawler
    #start_urls = ['http://spiderbites.nytimes.com/1997/'] #initial URLs that are to be accessed first


    custom_settings = {
        'LOG_FILE': "./nyt.log",
        'LOG_ENABLED': True,
        'LOG_STDOUT': True,
        'LOG_LEVEL': 'DEBUG',  # DEBUG, INFO
        'FEED_URI': r"./%(year)s.csv",
        'FEED_FORMAT': 'csv',
        'AUTOTHROTTLE_ENABLED': False,
    }


    def parse_item(self, response):

        #if 'articles_'+ self.year not in response.url:
        if 'articles_' + self.year not in response.url:
            item = NewsItem()

            item['title'] = response.xpath('//*[@itemprop="headline" or @class="headline"]/text()').extract_first()
            item['author'] = response.xpath('//*[@class="byline-author" or @class="author creator"]/text()').extract_first()
            item['article'] = response.xpath('//*[@class="story-body-text story-content" or @class="css-18sbwfn"]/text()').extract()
            item['dop'] = response.xpath('//*[@itemprop="dateModified" or @class="css-pnci9ceqgapgq0"]/text()').extract_first()
            item['section'] = response.xpath('//*[@id="kicker"]/span/a/text()').extract_first()
            item['url'] = response.url

            yield item
# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from scrapy.spiders import CrawlSpider, Rule
from nyt.items import NewsItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor

class TestSpider(CrawlSpider):

    def __init__(self, uni=None, *args, **kwargs):
        self.year = str(year)
        super(TestSpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://spiderbites.nytimes.com/' + year + '/']  # The starting page for the crawls

    name = "nyt" #This name will help while running the crawler itself
    allowed_domains = ["nytimes.com"] #which domains are accessible for this crawler

    start_urls = ['http://spiderbites.nytimes.com/1997/'] #initial URLs that are to be accessed first

    custom_settings = {
        # 'LOG_FILE': r"I:\COURSES\EAD\AITEIT3\BITY3\IN700001 Project\NLP\david\bu.log",
        'LOG_FILE': "./data/gen.log",
        'LOG_ENABLED': True,
        'LOG_STDOUT': True,
        'LOG_LEVEL': 'INFO',  # DEBUG, INFO
        'DEPTH_LIMIT': 3,
        # 'FEED_URI': r'file:///I:/COURSES/EAD/AITEIT3/BITY3/IN700001 Project/NLP/david/%(name)sDepthLimit%(depth_limit)s.csv',
        # 'FEED_URI': "file:///C:/Users/drozado/data/gen.csv",
        'FEED_URI': r"./data/%(self.year)s.csv",
        'FEED_FORMAT': 'csv',
        'AUTOTHROTTLE_ENABLED': False,
    }
    rules = (Rule(LxmlLinkExtractor(
            allow=(self.year)),
            follow=True,
            callback='parse_item'),)
		
    def parse_item(self, response):

        if 'articles_1997' not in response.url:
            item = NewsItem()

            item['title'] = response.xpath('//*[@itemprop="headline" or @class="headline"]/text()').extract_first()
            item['author'] = response.xpath('//*[@class="byline-author" or @class="author creator"]/text()').extract_first()
            item['article'] = response.xpath('//*[@class="story-body-text story-content" or @class="css-18sbwfn"]/text()').extract()
            item['dop'] = response.xpath('//*[@itemprop="dateModified" or @class="css-pnci9ceqgapgq0"]/text()').extract_first()
            item['section'] = response.xpath('//*[@id="kicker"]/span/a/text()').extract_first()
            item['url'] = response.url

            yield item
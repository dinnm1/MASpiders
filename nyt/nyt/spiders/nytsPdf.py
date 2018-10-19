# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
from scrapy.spiders import CrawlSpider, Rule
from nyt.items import NewsItem
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
import re
import os
import time
import scrapy
import pyocr
import PyPDF2

class TestSpider(CrawlSpider):

    def __init__(self, year=None, *args, **kwargs):

        self.year = year
        self.start_urls = ['http://spiderbites.nytimes.com/' + year + '/']  # The starting page for the crawls
        self.rules = (Rule(LxmlLinkExtractor(
                            allow=(['select.nytimes.com/gst/abstract.html',
                                    'query.nytimes.com/gst/abstract.html',
                                    'spiderbites.nytimes.com/'+year+'/articles_',
                                    ]), #valid from 1980 to 1970
                            ),

                            follow=True,
                            callback='parse_item'),
                      Rule(LxmlLinkExtractor(
                          allow=(['timesmachine.nytimes.com/timesmachine/' + year+'/\d+/\d+/\d+.html',
                                  #'timesmachine.nytimes.com/svc/timesmachine/v1/refer?pdf',
                                  #'timesmachine.nytimes.com/timesmachine/1969/\d+/\d+/\d+.pdf
                                  ]),  # valid from 1980 to 1970
                          # deny=(['/\?', '\?', '/classified/']), #valid from 1981 to 2018
                          deny_extensions=(),

                      ),
                          follow=True,
                          callback='parse_item_with_pdf'),
        )


        super(TestSpider, self).__init__(*args, **kwargs)

        tools = pyocr.get_available_tools()
        self.tool = tools[0]
        print("Will use tool '%s'" % (self.tool.get_name()))
        langs = self.tool.get_available_languages()
        self.lang = langs[0]
        print("Will use lang '%s'" % (self.lang))


    name = "nytsPdf" #This name will help while running the crawler itself
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

    def parse_item_with_pdf(self,response):

        item = NewsItem()

        # item['title'] = response.xpath('//*[@itemprop="headline" or @class="headline" or @class="balancedHeadline"]/text()').extract_first()
        item['title'] = response.xpath('//*[@class="index_article_title"]/text()').extract_first()
        item['author'] = response.xpath('//*[@id="byline_content"]/text()').extract_first()
        item['dop'] = response.xpath('//*[@id="publish_date_content"]/text()').extract_first()
        item['url'] = response.url
        pdfLink = response.url[:-4]+'pdf' #Strip HTML suffix
        print("OOOOOOOOOOOOOO:"+pdfLink)
        yield scrapy.Request(pdfLink, callback=self.parse_pdf, meta={'item': item},headers={'Cookie':'nyt-a=SDD8lVQuNFcytct6RCEpuW; vistory=a00; optimizelyEndUserId=oeu1528782239377r0.24770684785055264; __utmc=69104142; walley=GA1.2.963265854.1528782241; LPVID=JhZTlmYzczNTU3NGYwOGQ3; vi_www_hp=b20; PHPSESSID=2866910be63542797beb066189c50656; nyt_timesmachine_first_session=false; _cb_ls=1; _cb=CYcTKpDw_5wBD78OWz; LPSID-17743901=R6_N7m4FSI-pRO28tnMk0A; _ga=GA1.2.963265854.1528782241; aauHubDigi=true; NYT_W2=New%20YorkNYUS|ChicagoILUS|London--UK|Los%20AngelesCAUS|San%20FranciscoCAUS|Tokyo--JP; nyt-d=101.000000000NAI00000YAIWo0%2CPN5%2F004GKB0I6miJ07PH8b0gDJOz1w70W00N2nuK0A37ae0pApKk1%2F01450B4XiV0J1sK71%2F01450B4XiB0K1WS800PNDq1WSd9i1sV6CP0K6H8N070Wa81yS1CA0C7df4%40ffc567ea%2F5e387ff8; nyt-auth-method=username; _gcl_au=1.1.1335690985.1537330929; __utma=69104142.963265854.1528782241.1533697087.1537335225.9; __utmz=69104142.1537335225.9.2.utmcsr=nytimes.com|utmccn=(referral)|utmcmd=referral|utmcct=/2017/01/28/us/us-immigration-ban.html; _sp_id.75b0=9193461a7146c4d2.1528782246.38.1538624072.1538116536; walley_gid=GA1.2.178445080.1539565216; edu_cig_opt=%7B%22isEduUser%22%3Atrue%7D; b2b_cig_opt=%7B%22isCorpUser%22%3Afalse%7D; subDockView=true; ga_INT=GA1.2.963265854.1528782241; ga_INT_gid=GA1.2.310049192.1539840026; NYT-S=2oauKrtdVAKNYfZGRICljhdfl1BWP7DNCVXxqLyXOctpVpM8RNmkOjDcc90mqBaVcJWySSijqa.Nv9bn1VIjqlccSnzwtIA5P1l4GzcBN4FYQB/GKx4Q3nLH0FbZml7nzPpmrzlyEgM7iCoPgfv5KK5EpaBtC509dyyPbj02nW08ZkWaIdrzQViP3DpVNf9XGM7.S1SSvLIXk0; NYT-BCET=1539935547%7CehY%2BI1Ma7O0IvPYcrC4txGEt8cY%3D%7CY%3B_%7Cxnt37Jlc8lQKan%2FiHoFsvw5LrvrprXRTem95HbaM3iQ%3D; nyt-gdpr=0; _fbp=fb.1.1539914018458.546023465; _chartbeat2=.1536027105393.1539918992649.1000000000011101.B0qA6jHiUy2-x3tb7FNzuDZ6vdu.6; nyt-m=EA212C72D1A759947DE409902DF8BD4F&igf=i.0&iru=i.0&t=i.5&vp=i.0&rc=i.0&imu=i.1&e=i.1541030400&ira=i.0&v=i.0&prt=i.5&fv=i.0&g=i.0&igd=i.0&imv=i.0&gf=l.10.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1&iga=i.0&pr=l.4.223.0.0.0&ird=i.0&vr=l.4.103.0.0.0&ft=i.0&gl=l.2.-1.-1&n=i.2&iir=i.1&igu=i.1&l=l.15.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1.-1&rl=l.1.-1&ica=i.0&kid=i.1&cav=i.103&iub=i.0&iue=i.1&er=i.1538627324&ier=i.0&ifv=i.0&gb=l.3.0.0.1539927127; xyz_cr_623_et_122==NaN&cr=623&et=122'})

    def parse_pdf(self,response):
        try:
            scrape_count = int(self.crawler.stats.get_value('item_scraped_count'))
            if scrape_count % 20000 == 0:
                print("Entering sleep after " + str(scrape_count) + " scraped items")
                time.sleep(1000)
                print("Exiting sleep after " + str(scrape_count) + " scraped items")
        except:
            pass
        print("Heyyyyyyyyyyyyyyyyyyyyy:" + response.url)
        reader = PyPDF2.PdfFileReader(response.body)
        text = u"aaaa"
        item = response.meta['item']
        """
        stream = StringIO.StringIO(response.body)

        if reader.getDocumentInfo().title:
                # Title is optional, may be None
                text += reader.getDocumentInfo().title
        """
        item['article'] = text
        yield item

    def parse_item(self, response):
        pass

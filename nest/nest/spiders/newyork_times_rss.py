import scrapy
import urllib2
import re
from datetime import datetime
from scrapy.spiders import XMLFeedSpider
from scrapy.selector import Selector
import sys
from nest.news_parser import ArticleExtractor


class NewyorkTimesRssSpider(XMLFeedSpider):

    name = "newyork_times_rss"
    allowed_domains = ["nytimes.com"]
    download_delay = 2

    start_urls = (
        'http://rss.nytimes.com/services/xml/rss/nyt/Arts.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/InternationalHome.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/World.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/US.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/NYRegion.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Business.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/EnergyEnvironment.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/\
            InternationalBusiness.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/SmallBusiness.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/Economy.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/MediaandAdvertising.xml',
        'http://rss.nytimes.com/services/xml/rss/nyt/YourMoney.xml')

    itertag = 'item'

    def parse_node(self, response, node):
        # Clean up namespace to allow for tags to be accessed
 
        node.remove_namespaces()
        #titles = node.xpath('//title/text()').extract()
        #title= titles[2]
        #description = node.xpath('//*[name()="media:description"]/text()').extract()
        #description = node.xpath('//description/text()').extract()
        links = node.xpath('//link[@rel="standout"]/@href').extract()
        pub_date = node.xpath('//pubDate/text()').extract()[0]
        small_img = node.xpath('//*[name()="media:content"]/@url').extract()
        
        #TODO Convert date

        # Fetch actual article
        if len(links) > 0:

            url = links[0]

            # Cookie workaround for NY Times. NY times a ...
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(url)
            raw_html = response.read()

            # Goose cannot extract clean text from html of NY Times
            selector = Selector(text=raw_html)
            article_selectors = selector.xpath('//*[contains(@class, "story-body-text")]/text()')
            cleaned_text = '\n'.join(article_selectors.extract())

            article_ex = ArticleExtractor(url,response,raw_html)
            article_item = article_ex.get_article_item()

            # Override since Goose was not able to extract correctly
            article_item['text_content'] = cleaned_text
            article_item['date_published'] = pub_date
            article_item['source'] = 'nytimes'
            return article_item


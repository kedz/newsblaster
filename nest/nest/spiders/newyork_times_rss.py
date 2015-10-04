import scrapy
import urllib2
import re
from datetime import datetime
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import XMLFeedSpider
from nest.items import ArticleItem
from scrapy.selector import Selector
import sys
from goose import Goose
import cookielib

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
    iterator = 'xml'

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
        #Convert date
    

        # Fetch actual article
        if len(links) > 0:
            #request = scrapy.http.Request(links[0],meta={'dont_merge_cookies': True},callback=self.parse_article)
            #request.meta['pub_date'] = pub_date
            #request.meta['small_img'] = small_img
            #yield request

            url = links[0]

            # Cookie workaround for NY Times. NY times a ...
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
            response = opener.open(url)
            raw_html = response.read()

            # Goose cannot extract clean text from html of NY Times
            selector = Selector(text=raw_html)
            article_selectors = selector.xpath('//*[contains(@class, "story-body-text")]/text()')
            cleaned_text = '\n'.join(article_selectors.extract())

            extractor = Goose({'enable_image_fetching' : True,})
            extractor_contents = extractor.extract(raw_html=raw_html)
            description = extractor_contents.meta_description
            keywords = extractor_contents.meta_keywords
            authors = extractor_contents.authors
            images = None
            article_image =  extractor_contents.top_image
            if article_image is not None:
                images = article_image.src


            # Initialize Items
            article_item = ArticleItem()
        
            # Fill in Article Information
            article_item['source_link'] = response.url
            article_item['time_of_crawl'] = int(datetime.strptime(response.headers['Date'],"%a, %d %b %Y %H:%M:%S %Z").strftime("%s"))*1000
            #article_item['html_content'] = html
            article_item['text_content'] = cleaned_text
            article_item['source_type'] = 'news'
            article_item['title'] = extractor_contents.title
            article_item['date_published'] = pub_date
            article_item['authors'] = authors
            article_item['topics'] = keywords
            article_item['images_url'] = images


            # Check if article was parsed, if not write to error file
            #TODO replace this code with logging
            if "title" not in article_item.keys():
                errorFile = open("MissedArticles.txt", 'a')
                if len(response.request.meta['redirect_urls']) > 0:
                    errorFile.write(response.request.meta['redirect_urls'][0] +
                                "\r\n")
                else:
                    errorFile.write(response.url + "\r\n")
                errorFile.close()
            # print "Writing to file"
            print article_item
            return article_item


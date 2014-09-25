import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy import log
from scrapy.selector import XmlXPathSelector
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.contrib.spiders import XMLFeedSpider
from nest.items import ArticleItem, ArticleMetaInformation
from scrapy.selector import Selector

class NewyorkTimesRssSpider(XMLFeedSpider):
    name = "newyork_times_rss"
    allowed_domains = ["nytimes.com"]

    #TODO put list of all RSS feeds here
    start_urls = ('http://rss.nytimes.com/services/xml/rss/nyt/Arts.xml','http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml' 'http://rss.nytimes.com/services/xml/rss/nyt/InternationalHome.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/World.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Africa.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Americas.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/AsiaPacific.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Europe.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/MiddleEast.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Education.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/US.xml', 'http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml')
    itertag = 'item'

    def parse_node(self, response, node):
        # Clean up namespace to allow for tags to be accessed
        node.remove_namespaces()
        
        mylist = node.xpath('//link[@rel="standout"]/@href').extract()
        #print mylist
        #Extract all relevant meta information
        #Extract url from each item in the rss feed
        #Fetch article
        #Example
        #url = 'http://www.nytimes.com/2014/09/21/movies/a-survey-celebrates-georgias-rich-film-tradition.html?partner=rss&emc=rss'
        
        #Fetch actual article
        if len(mylist) > 0:
           yield scrapy.Request(mylist[0],callback=self.parse_article)
        #yield scrapy.Request(url,callback=self.parse_article)

    def parse_article(self,response):
        print '*************Parsing article'
        
        #Initialize Items
        article_item = ArticleItem()
        article_meta_information = ArticleMetaInformation()
        
        #Fill in Article Information
        article_item['source_link'] = response.url        
        article_item['time_of_crawl'] = response.headers['Date']       
        article_item['html_content'] = response.body      
        article_item['text_content'] = response.xpath('//p[re:test(@class, "story-body-text")]/text()').extract()
        article_item['source_type'] = 'news_article'
        
        article_title = response.xpath('//meta[@property=\"og:title\"]/@content').extract()
        if len(article_title) > 0:
           article_item['title'] = article_title[0]
        
        date_published = response.xpath('//meta[@property=\"article:published\"]/@content').extract()
        if len(date_published) > 0:
            article_meta_information['date_published'] = date_published[0]
        else:
            date_published = response.xpath('//meta[@property=\"article:published_time\"]/@content').extract()
            if len(date_published) > 0:
                article_meta_information['date_published'] = date_published[0]
        
        article_meta_information['location'] = 'USA'

        author = response.xpath('//meta[@name=\"author\"]/@content').extract()
        if len(author) > 0:
            article_meta_information['author'] = author[0]
        
        keywords = response.xpath('//meta[@name=\"keywords\"]/@content').extract()
        article_meta_information['topics'] = self.get_topics(keywords)
        
        language = response.xpath('//meta[@itemprop=\"inLanguage\"]/@content').extract()
        if len(language) > 0:
           article_meta_information['language'] = language[0][:2]
        else:
            article_meta_information['language'] = "en"
        
        main_image = response.xpath('//meta[@property=\"og:image\"]/@content').extract()
        if len(main_image) > 0:
           article_meta_information['images_url'] = main_image[0]
        
        article_item['meta_information'] = article_meta_information
        
        #prints meta information
        print article_item['meta_information']

    def get_topics(self,keywords):
    #data always present in 0 of array
        for keyword_list in keywords:
            return keyword_list.split(',')

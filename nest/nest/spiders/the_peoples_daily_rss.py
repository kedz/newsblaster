import scrapy
import re
from datetime import datetime
from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from nest.items import ArticleItem
from scrapy.selector import Selector
from nest.news_parser import ArticleExtractor

class PeopleDailySpiderRSS(XMLFeedSpider):
    name = "the_peoples_daily_rss"
    download_delay = 2
    # allowed_domains = ["english.people.com.cn",
    # "english.peopledaily.com.cn"]

    start_urls = ('http://english.peopledaily.com.cn/rss/World.xml',)
    itertag = 'item'

    def parse_node(self, response, node):
        # Clean up namespace to allow for tags to be accessed
        links = node.xpath('//item//link/text()').extract()


        #TODO custom parsing might be required to extract larger # of articles.

        if len(links) > 0:
            url = links[0].replace("\n", "").strip()
            article_ex = ArticleExtractor(url,response)
            article_item = article_ex.get_article_item()
            article_item['source'] = 'the_peoples_daily'
            # Drop html for this crawler. 
            article_item['html_content'] = None
            return article_item



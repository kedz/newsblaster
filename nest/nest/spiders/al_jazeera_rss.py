import scrapy
import re
from datetime import datetime
from scrapy import log
from scrapy.contrib.spiders import XMLFeedSpider
from nest.items import ArticleItem
from scrapy.selector import Selector
from nest.news_parser import ArticleExtractor


class al_jazeera_rss(XMLFeedSpider):
    name = "al_jazeera_rss"
    allowed_domains = ["america.aljazeera.com"]

    download_delay = 2

    # NOTE: Any more rss links ?
    start_urls = ("http://america.aljazeera.com/content/ajam/articles.rss",)
    itertag = 'item'

    def parse_node(self, response, node):

        # Clean up namespace to allow for tags to be accessed
        node.remove_namespaces()
        links = node.xpath('//item//link/text()').extract()

        # Fetch actual article
        if len(links) > 0:
            url = links[0]
            article_ex = ArticleExtractor(url,response)
            article_item = article_ex.get_article_item()
            article_item['source'] = 'aljazeera'
            return article_item

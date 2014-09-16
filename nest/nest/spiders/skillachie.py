import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from pprint import pprint
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

class SkillachieSpider(CrawlSpider):

	name = "skillachie"
	allowed_domains = ["skillachie.com"]

	start_urls = (
			'http://www.skillachie.com/',
		     )		
	#http://skillachie.com/2014/07/25/mysql-cluster-101/

	#Follow only these specific links
	blog_link_format = re.compile('http://skillachie.com/\d+/\d+/\d+')

	#Rules to handle following urls
	rules = (Rule(LxmlLinkExtractor(allow=(blog_link_format), allow_domains=('skillachie.com', )),callback='parse_follow',follow=True), )

	def parse_follow(self, response):

		#TODO save html and send to RabbitMQ here
		#TODO complete pipeline and items
		#print(response.body)
		pass

		#TODO Create custom link extractor for RSS


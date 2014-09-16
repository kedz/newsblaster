import scrapy
import re
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy import log
from pprint import pprint
from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor

#TODO implement throttle

class PeopleDailySpider(CrawlSpider):


	name = "the_peoples_daily"
	allowed_domains = ["english.people.com.cn"]

	start_urls = (
			'http://english.people.com.cn/',
		     )		

	#URL Patterns For English Articles http://english.people.com.cn
	#http://english.people.com.cn/n/2014/0912/c90882-8782115.html
	#http://english.people.com.cn/n/2014/0912/c98649-8781550.html
	#http://english.people.com.cn/n/2014/0912/c98649-8781657.html

	#Follow only these specific links
	article_link_format = re.compile('http://english.people.com.cn/n/\d+/\d+')

	#Rules to handle following urls
	rules = (Rule(LxmlLinkExtractor(allow=(article_link_format), allow_domains=('english.people.com.cn', )),callback='parse_follow',follow=True), )

	def parse_follow(self, response):

		#TODO save html and send to RabbitMQ here
		#TODO complete pipeline and items
		#print(response.body)
		pass


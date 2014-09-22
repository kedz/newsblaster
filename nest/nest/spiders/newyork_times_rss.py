import scrapy
from scrapy import log
from scrapy.selector import XmlXPathSelector
from scrapy.contrib.spiders import XMLFeedSpider

class NewyorkTimesRssSpider(XMLFeedSpider):
		name = "newyork_times_rss"
		allowed_domains = ["nytimes.com"]

		#TODO put list of all RSS feeds here
		start_urls = ('http://rss.nytimes.com/services/xml/rss/nyt/Arts.xml',)
		itertag = 'item'

		def parse_node(self, response, node):
			
			# Clean up namespace to allow for tags to be accessed 
			node.remove_namespaces()
			
			print node.xpath('//link[@rel="standout"]/@href').extract()
			#print node.xpath('title').extract()
			#Extract all relevant meta information
			#Extract url from each item in the rss feed
			#Fetch article
			#Example
			url = 'http://www.nytimes.com/2014/09/21/movies/a-survey-celebrates-georgias-rich-film-tradition.html?partner=rss&emc=rss'
			
			#Fetch actual article
			yield scrapy.Request(url,callback=self.parse_article)

		def parse_article(self,response):
			print '*************Parsing article'
			print response.body

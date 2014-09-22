# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
	title = Field()
	source_type = Field()
	source_link = Field()
	time_of_crawl = Field()
	html_content = Field()
	text_content = Field()
	meta_information = Field() # ArticleMetaInformation Item


class ArticleMetaInformation(Item):
	location = Field()
	topics = Field() #Array of topics
	date_published = Field()
	author = Field()
	language = Field()
	images_url = Field() #Links to images in article. Optional for now

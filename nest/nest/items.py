# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class ArticleItem(Item):
    title = Field()
    clustered = Field()
    source = Field()
    source_type = Field()
    source_link = Field()
    time_of_crawl = Field()
    html_content = Field()
    text_content = Field()
    date_published = Field()
    authors = Field() #Array of authors
    topics = Field() #Array of topics
    images_url = Field() #Links to images in article. Optional for now

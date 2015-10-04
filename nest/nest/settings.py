# -*- coding: utf-8 -*-

# Scrapy settings for nest project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'nest'

SPIDER_MODULES = ['nest.spiders']
NEWSPIDER_MODULE = 'nest.spiders'
#CONCURRENT_REQUESTS=1
LOG_LEVEL = 'DEBUG'
COOKIES_DEBUG = True
COOKIES_ENABLED = True

DOWNLOADER_MIDDLEWARES = {
    'scrapy.downloadermiddlewares.cookies.CookiesMiddleware': 700,
}

ITEM_PIPELINES = {
	'nest.pipelines.ArticleEnrichmentPipeLine': 1,
	'nest.pipelines.ArticleSummarizationPipeline': 2,
	'nest.pipelines.SendToDataStorePipeline': 3,
								 }

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'nest (+cs.columbia.com)'

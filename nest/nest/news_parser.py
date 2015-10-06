import  urllib2
from goose import Goose
from nest.items import ArticleItem
from datetime import datetime


class ArticleExtractor(object):

    def __init__(self,url,response,raw_html=None):
        self.url = url
        self.raw_html = raw_html
        self.response = response

    def get_article_item(self):

        extractor = Goose({'enable_image_fetching' : True,'use_meta_language': False, 'target_language':'en'})
        extractor_contents = None
        html_content = None

        if self.raw_html:
            extractor_contents = extractor.extract(raw_html=self.raw_html)
            html_content = self.raw_html
        else:
            extractor_contents = extractor.extract(url=self.url)
            html_content = extractor_contents.raw_html

        description = extractor_contents.meta_description
        keywords = extractor_contents.meta_keywords
        authors = extractor_contents.authors
        cleaned_text = extractor_contents.cleaned_text
     
        images = None
        article_image =  extractor_contents.top_image
        if article_image is not None:
            images = article_image.src

        # Initialize Items
        article_item = ArticleItem()

        # Fill in Article Information
        article_item['clustered'] = False
        article_item['source_link'] = self.url
        article_item['time_of_crawl'] = int(datetime.strptime(self.response.headers['Date'],"%a, %d %b %Y %H:%M:%S %Z").strftime("%s"))*1000
        article_item['html_content'] = html_content
        article_item['text_content'] = cleaned_text
        article_item['source_type'] = 'news'
        article_item['title'] = extractor_contents.title
        article_item['date_published'] = None #Set from Spider
        article_item['authors'] = authors
        article_item['topics'] = keywords
        article_item['images_url'] = images

        return article_item

    def check_if_attrs_empty(self,article_item):
        empty_attrs = []
        for attr in article_items.keys():
            if article_items[attr] is None:
                empty.append(attr)
        return empty_attrs

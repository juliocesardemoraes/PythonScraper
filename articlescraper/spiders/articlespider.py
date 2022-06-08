import re
import os
import scrapy
from pymongo import UpdateOne
from articlescraper.database import Database

class Article():
    """
    Object that witholds an bbc article content

    Parameters:
        title (str): Article title
        link (str): Article that redirects to article page
        category (str): Article Category(Ex: Europe, USA, Culture)

    Returns:
        An Article Class Instance
    """
    def __init__(self, title, link, category) -> None:
        self.title = title
        self.link = link
        self.category = category

    def __getitem__(self, key):
        return getattr(self, str(key))
    def __setitem__(self, key, value):
        return setattr(self, str(key), value)

    def get_list(self):
        """
        Method for fetching the instance properties and values as a dict
        so it can be read and inserted into the database

        Parameters:
            self

        Returns:
            Returns the instance class properties formatted as a json
        """
        return {"title":self.title, "link": self.link, "category": self.category}

class ArticleSpider(scrapy.Spider):
    """
    Class used for scraping web for news articles, in this case bbc one

    Parameters
        scrapy.Spider (class): Responsible for crawling the website
    """
    name = 'article'
    start_urls = ['http://www.bbc.com/']
    allowed_domains = ['www.bbc.com']


    def parse(self, response):
        mongo = Database("bbc_" + os.getenv('DEPLOY_ENVIROMENT'))

        index = 0

        article_object = []

        for article in response.css('div.media__content'):
            article_to_format = article.css('a.media__link::text').get()
            article_link = article.css('a.media__link::attr(href)').get()


            if index<5 :
                article_object.append(Article("","",""))

                if not re.search("https://", article_link):
                    article_object[index].link = ("https://www.bbc.com" + article_link)
                else:
                    article_object[index].link = article_link

                article_object[index].title = article_to_format.strip()
                theme = article.css('a.media__tag::text').get()
                article_object[index].category = theme

            index = index + 1

        operations = []

        for operation in article_object:
            operations.append(UpdateOne({ "title": operation.title},{"$set": operation.get_list()},upsert=True))

        mongo.database_instance.bulk_write(operations)

        return{
            "code": 200,
        }

"""
from textblob import Blobber
from textblob.taggers import NLTKTagger
from textblob.sentiments import NaiveBayesAnalyzer
        # NPL TO IMPLEMENT
        # tb = Blobber(analyzer=NaiveBayesAnalyzer())
        # nkl = Blobber(pos_tagger=NLTKTagger())

        for article in article_title_list:
            print("ARTICLE", article)
            blob = tb(article)
            blob2 = nkl(article)
            print("TEXTO", blob)
            print("BLAB", blob.sentiment)
            print("TEXTO2", blob2)
            print("BLAB2", blob2.sentiment)
"""
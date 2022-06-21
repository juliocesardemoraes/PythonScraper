import re
import os
import datetime
import scrapy
from articlescraper.database import Database

class Article():
    """
    Object that witholds an article structure

    Parameters:
        category (str): Article Category(Ex: Europe, USA, Culture).
        content (Array(str)): Article actual content.
        date: Article Release Date.
        image_link (str): Article image link to render.
        link (str): Article that redirects to article page.
        title (str): Article title.

    Returns:
        An Article Class Instance
    """
    def __init__(self, category, content, date, image_link, link, title) -> None:
        self.category = category
        self.content = content
        self.date = date
        self.image_link = image_link
        self.link = link
        self.title = title


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
        return {"title":self.title,
                "link": self.link,
                "category": self.category,
                "image_link": self.image_link,
                "content": self.content,
                "date": self.date
                }

class BBCSpider(scrapy.Spider):
    """
    Class used for scraping web for news articles,
    in this case we're using the bbc news website

    Parameters
        scrapy.Spider (class): Responsible for crawling the website

    Returns:
        code 200 when it's successful
    """
    name = 'article'
    start_urls = ['http://www.bbc.com/']
    allowed_domains = ['www.bbc.com']


    def parse(self, response):

        index = 0
        article_object = []

        for article in response.css('div.media__content'):
            article_to_format = article.css('a.media__link::text').get()
            article_link = article.css('a.media__link::attr(href)').get()

            # Checking index to only scrape the main articles
            if index<5 :
                article_object.append(Article("","","","",[],""))

                if not re.search("https://", article_link):
                    article_object[index].link = ("https://www.bbc.com" + article_link)
                else:
                    article_object[index].link = article_link

                article_object[index].title = article_to_format.strip()

                theme = article.css('a.media__tag::text').get()
                article_object[index].category = theme

                image = response.css('div.responsive-image')
                image_src = image[index].css('img::attr(src)').get()

                article_object[index].image_link = image_src

                article_time_fetch = datetime.date.today().strftime("%Y-%m-%d")

                article_object[index].date = article_time_fetch

            index = index + 1

        for article in article_object:
            yield scrapy.Request(article.link, callback=self.article_crawler, meta={'object': article})

        return article_object

    def article_crawler(self,response):
        """
        Method that enters each article page and fetches the content
        and also inserts the object into the database

        Parameters:
            self
            response (Dict): An status code regarding the crawling

        Returns:
            No Return
        """
        mongo = Database("bbc_" + os.getenv('DEPLOY_ENVIROMENT'))
        article_object = response.meta['object']

        for article in response.css('article'):
            content = article.css('p::text').extract()
            article_object.content = content

        mongo.database_instance.replace_one({ "title": article_object.title},
        article_object.get_list(), upsert=True)

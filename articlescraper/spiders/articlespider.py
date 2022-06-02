import scrapy
import re
from textblob import TextBlob
from articlescraper.db import Database




class ArticleSpider(scrapy.Spider):
    name = 'article'
    start_urls = ['http://www.bbc.com/']
    allowed_domains = ['www.bbc.com']


    def parse(self, response):

        db = Database().initialize_database()

        article_title_list = []
        article_link_list = []

        for article in response.css('h3.media__title'):
            articleToFormat = article.css('a.media__link::text').get()
            articleLink = article.css('a.media__link::attr(href)').get()

            if not (re.search("https://", articleLink)):
                article_link_list.append("https://www.bbc.com" + articleLink)
            else: 
                article_link_list.append(articleLink)

            article_title_list.append(articleToFormat.strip())

        print(article_title_list)
        print(article_link_list)


        for article in article_title_list:
            blob = TextBlob(article)
            print("TEXTO", blob)
            print("BLAB", blob.sentiment.polarity)



import re
import scrapy
from articlescraper.db import Database
from textblob.sentiments import NaiveBayesAnalyzer
from textblob import Blobber
from textblob.taggers import NLTKTagger


class ArticleSpider(scrapy.Spider):
    """
    Main class to scrape web for articles
    :param scrapy.Spider class: Responsible for crawling the website
    """
    name = 'article'
    start_urls = ['http://www.bbc.com/']
    allowed_domains = ['www.bbc.com']


    def parse(self, response):
        db = Database()

        article_title_list = []
        article_link_list = []
        article_theme_list = []

        index = 0

        for article in response.css('div.media__content'):
            article_to_format = article.css('a.media__link::text').get()
            article_link = article.css('a.media__link::attr(href)').get()

            if index<5 :
                if not re.search("https://", article_link):
                    article_link_list.append("https://www.bbc.com" + article_link)
                else:
                    article_link_list.append(article_link)
                article_title_list.append(article_to_format.strip())

                theme = article.css('a.media__tag::text').get()
                article_theme_list.append(theme)

            index = index + 1

        db.insert_one_object({"article_title": article_title_list, "article_link": article_link_list,
         "article_theme": article_theme_list })


        #print(article_title_list)
        #print(article_link_list)

        tb = Blobber(analyzer=NaiveBayesAnalyzer())
        nkl = Blobber(pos_tagger=NLTKTagger())


"""
        for article in article_title_list:
            print("ARTICLE", article)
            blob = tb(article)
            blob2 = nkl(article)
            print("TEXTO", blob)
            print("BLAB", blob.sentiment)
            print("TEXTO2", blob2)
            print("BLAB2", blob2.sentiment)
"""
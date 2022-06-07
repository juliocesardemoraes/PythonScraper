from pymongo import MongoClient
from dotenv import load_dotenv
import os;

load_dotenv()

class Database():
    """
    Class to instantiate a database connection
    params: none
    returns: Database Instance
    """
    def __init__(self):
        print("UUU", os.getenv('MONGO_URI'))
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.database_instance = self.client.webscrapping.bbc

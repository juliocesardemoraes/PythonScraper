from pymongo import MongoClient
from dotenv import load_dotenv
import os;

load_dotenv()

class Database:
    """
    Class to instantiate a database connection

    param: collection_database string: Collection To be used in the database
    returns: Database Instance
    """
    def __init__(self, collection_database):
        self.collection = collection_database
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.database_instance = getattr(self.client.webscrapping, self.collection)

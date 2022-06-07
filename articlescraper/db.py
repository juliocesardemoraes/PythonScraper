from pymongo import MongoClient
from dotenv import load_dotenv
import os;

load_dotenv()

class Database():
    def __init__(self):
        self.client = MongoClient(os.getenv('MONGO_URI'))
        self.db = self.client.webscrapping.bbc
    

    def insert_one_object(self, object_to_insert):
        """
        Function to insert one object
        :param object_to_insert object: Object to insert into mongo
        """
        self.db.insert_one(object_to_insert)


if __name__ == "__main__":
    db= Database()
    db.initialize_database()

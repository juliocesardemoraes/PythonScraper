from pymongo import MongoClient
from dotenv import load_dotenv
import os;

load_dotenv()

class Database():
    def initialize_database(self):
        client = MongoClient(os.getenv('MONGO_URI'))

        for dbe in client.list_databases():
            print('DB', dbe)

        db = client.webscrapping.bbc
        # db.insert_one({"title": "Teste", "name": "Aqui"})
        return client
        

if __name__ == "__main__":
    db= Database()
    db.initialize_database()

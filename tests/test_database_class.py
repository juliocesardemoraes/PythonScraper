from articlescraper.database import Database

def test_insert_into_database():
    """
    Test to check if database is inserting, and
    testing if it's inserted
    """
    mongo = Database("testing_database_insert")
    object_to_test = {"unique_test":"test"}
    mongo.database_instance.insert_one(object_to_test)
    teste = mongo.database_instance.find_one(object_to_test)
    mongo.database_instance.drop()
    assert teste == object_to_test


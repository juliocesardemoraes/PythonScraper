import pytest

def test_insert_into_database():
    """
    Test to check if database is inserting, and
    testing if it's inserted
    """
    pytest.mongo.database_instance.insert_one(pytest.object_to_test)
    inserted_object = pytest.mongo.database_instance.find_one(pytest.object_to_test)
    assert inserted_object == pytest.object_to_test

def test_read_from_collection():
    """
    Test to check if database is reading properly

    Parameters: none

    Returns: none
    """
    read_object = pytest.mongo.database_instance.find_one(pytest.object_to_test)
    assert read_object == pytest.object_to_test

def test_update_from_collection():
    """
    Test to check if database is updating properly

    Parameters: none

    Returns: none
    """
    object_to_update = {"operation":"update"}

    pytest.mongo.database_instance.update_one(pytest.object_to_test,{ "$set": object_to_update})

    update_test = pytest.mongo.database_instance.find_one(object_to_update)

    assert update_test['operation'] != pytest.object_to_test['operation']
    assert update_test['operation'] == object_to_update['operation']

def test_delete_from_collection():
    """
    Test to check if database is deleting properly

    Parameters: none

    Returns: none
    """
    pytest.mongo.database_instance.delete_one(pytest.object_to_test)
    deleted_object = pytest.mongo.database_instance.find_one(pytest.object_to_test)
    assert deleted_object is None

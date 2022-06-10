import pytest
from articlescraper.database import Database

def pytest_configure():
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every plugin and initial conftest
    file after command line options have been parsed.
    """
    pytest.mongo = Database("testing_database_insert")
    pytest.object_to_test = {"operation":"main"}

def pytest_sessionstart():
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

def pytest_sessionfinish():
    """
    Called after whole test run finished, right before
    returning the exit status to the system.
    """
    pytest.mongo.database_instance.drop()

def pytest_unconfigure():
    """
    Called before test process is exited.
    """
    pytest.mongo.client.close()

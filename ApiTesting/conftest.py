import pytest
import configparser

"""
	The aim of these fixtures are so that values from the config.ini files can be stored.
	In order for the test functions to recognize these variables.
	An alternative implementation is the usage global variables or pytest_configure()
"""
config = configparser.ConfigParser()
config.read('config.ini')

@pytest.fixture()
def project_id():
	#Initialize project_id for the session
	project_id = config['keys']['project_id']
	return project_id

@pytest.fixture()
def project_api_key():
	#Initialize project_api_key for the session
	project_api_key = config['keys']['project_api_key']
	return project_api_key
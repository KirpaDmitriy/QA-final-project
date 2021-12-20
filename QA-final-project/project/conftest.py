import pytest
import requests

from AppClient import Application
from DBClient import DataBase

@pytest.fixture
def session():
    credentials = {
        'username': 'abobaaaaaaaa',
        'password': 'T5LydYtmtv7EDEC',
        'submit': 'Login'
    }
    
    answer = requests.post("http://127.0.0.1:8080/login", data=credentials, allow_redirects=False)
    
    session = {
        'session': answer.cookies.get('session')
    }
    
    return session


@pytest.fixture
def app():
    return Application("http://127.0.0.1", 8080,
                       "api/add_user",
                       "api/del_user",
                       "api/block_user",
		       "api/accept_user",
                       "status")


@pytest.fixture
def db():
    return DataBase('127.0.0.1', 3306, 'root', '1234', 'MYSQL_DB')

from faker import Faker
from selenium import webdriver

fake = Faker()


class BaseTest:
    def generate_user(self, name='', password='', email=''):
        new_user = {
            'username': ''.join(fake.name().split()) if len(name) == 0 else name,
            'password': fake.password() if len(password) == 0 else password,
            'email': fake.email() if len(email) == 0 else email
        }
        return new_user
    
    
    def create_user(self, session, app, db, name='', password='', email=''):
        new_user = self.generate_user(name, password, email)
        app.add_user(new_user, session)
        user_added = db.user_in_db(new_user)
        assert user_added, "Problem adding user"
        return new_user


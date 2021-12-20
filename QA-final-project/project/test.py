from faker import Faker
import allure
from selenium import webdriver

from Base import BaseTest

fake = Faker()


class TestApplicationApi(BaseTest):
    @allure.story("Check if the app started")
    def test_started(self, app):
        '''Проверяет, запущено ли приложение'''
        app_answer = app.start()
        started = (app_answer.json()['status'] == 'ok')
        assert started, "Failed starting the app"
        assert app_answer.status_code == 200
    
    
    @allure.story("Check adding new user")
    def test_add_new_user(self, session, app, db):
        '''Проверяет добавление нового пользователя. В итоге пользователь должен попасть в базу, приложение - вернуть нужный код'''
        new_user = self.generate_user()
        app_answer = app.add_user(new_user, session)
        found_in_db = db.user_in_db(new_user)
        assert found_in_db, "User was not added in database"
        assert app_answer.status_code == 201, "Wrong http status code"
    
    
    @allure.story("Adding same user twice")
    def test_add_same_user(self, session, app, db):
        '''Проверяет добавление пользователя дважды. Приложение должно сообщить об отсутствии изменений'''
        anyuser_from_db = db.get_first_user_creds()
        name, password, email = anyuser_from_db
        same_user = self.generate_user(name, password, email)
        app_answer = app.add_user(same_user, session)
        assert app_answer.status_code == 304, "Wrong status code"
    
    
    @allure.story("Adding almost same user twice")
    def test_add_same_name(self, session, app, db):
        '''Проверяет добавление пользователя пользователя с существующим логином. Приложение должно сообщить о том, что такая сущность уже существует, либо добавить пользователя'''
        anyuser_from_db = db.get_first_user_creds()
        name, password, email = anyuser_from_db
        almost_same_user = self.generate_user(name, password, fake.email())
        app_answer = app.add_user(almost_same_user, session)
        found_in_db = db.user_in_db(almost_same_user)
        if found_in_db:
            assert app_answer.status_code in [200, 201], "Wrong status code"
        else:
            assert app_answer.status_code == 304, "Wrong status code"
    
    
    @allure.story("Adding almost same user twice")
    def test_add_same_email(self, session, app, db):
        '''Проверяет добавление пользователя пользователя с существующей почтой. Приложение должно сообщить о том, что такая сущность уже существует, либо добавить пользователя'''
        anyuser_from_db = db.get_first_user_creds()
        name, password, email = anyuser_from_db
        almost_same_user = self.generate_user(''.join(fake.name().split()), password, email)
        app_answer = app.add_user(almost_same_user, session)
        found_in_db = db.user_in_db(almost_same_user)
        if found_in_db:
            assert app_answer.status_code in [200, 201], "Wrong status code"
        else:
            assert app_answer.status_code == 304, "Wrong status code"
    
    
    @allure.story("Deleting user")
    def test_delete_user(self, session, app, db):
        '''Удаление пользователя. В случае успеха он пропадает из БД'''
        new_user = self.create_user(session, app, db)
        app_answer = app.delete_user(new_user['username'], session)
        user_deleted_from_db = not db.user_in_db(new_user)
        assert user_deleted_from_db, "User was not removed from database"
        assert app_answer.status_code == 204, "Wrong status code"
    
    
    @allure.story("Deleting user who was not registered")
    def test_delete_nonexistent_user(self, session, app, db):
        '''Удаление пользователя, которого в БД нет. Приложение должно сообщить о том, что такой сущности нет'''
        app_answer = app.delete_user(fake.name(), session)
        assert app_answer.status_code == 404, "Wrong status code"
    
    
    @allure.story("Block unblocked user")
    def test_block_user(self, session, app, db):
        '''Блокировка должна пройти успешно, данные попасть в БД'''
        user_to_block = self.create_user(session, app, db)
        app_answer = app.block_user(user_to_block['username'], session)
        user_blocked = db.user_blocked(user_to_block['username'])
        assert user_blocked, "User was not blocked in database"
        assert app_answer.status_code == 200, "Wrong status code"
    
    
    @allure.story("Block blocked user")
    def test_block_fail(self, session, app, db):
        '''Блокировка не должна ничего поменять, а приложение должно сообщить об этом'''
        user_to_block = self.create_user(session, app, db)
        app.block_user(user_to_block['username'], session)
        app_answer = app.block_user(user_to_block['username'], session)
        user_blocked = db.user_blocked(user_to_block['username'])
        assert user_blocked, "User was unblocked in database"
        assert app_answer.status_code == 304, "Wrong status code"
    
    
    @allure.story("Block nonexistent user")
    def test_block_nobody(self, session, app, db):
        '''Блокировка несуществующего пользователя должна завершится сообщением об отстутсвии сущности'''
        app_answer = app.block_user(fake.name(), session)
        assert app_answer.status_code == 404, "Wrong status code"
    
    
    @allure.story("Unblock blocked user")
    def test_unblock_user(self, session, app, db):
        '''Разблокировка аналогично блокировке должна изменить данные в БД'''
        user_to_unblock = self.create_user(session, app, db)
        app.block_user(user_to_unblock['username'], session)
        app_answer = app.unblock_user(user_to_unblock['username'], session)
        user_unblocked = not db.user_blocked(user_to_unblock['username'])
        assert user_unblocked, "User was not unblocked in database"
        assert app_answer.status_code == 200, "Wrong status code"
    
    
    @allure.story("Unblock unblocked user")
    def test_unblock_fail(self, session, app, db):
        '''Разблокировка разблокированного пользователя никаких изменений вносить не должна, завершается сообщением об отсутствии изменений'''
        user_to_unblock = self.create_user(session, app, db)
        app_answer = app.unblock_user(user_to_unblock['username'], session)
        user_unblocked = not db.user_blocked(user_to_unblock['username'])
        assert user_unblocked, "User was blocked in database"
        assert app_answer.status_code == 304, "Wrong status code"
    
    
    @allure.story("Unblock nonexistent user")
    def test_unblock_nobody(self, session, app, db):
        '''Разблокировать несуществующего пользователя нельзя, должно быть отправлено сообщение о том, что такой сущности нет'''
        app_answer = app.unblock_user(fake.name(), session)
        assert app_answer.status_code == 404, "Wrong status code"
    
    
    @allure.story("Unblock having no rights")
    def test_unauthorized_block(self, session, app, db):
        '''Заблокировать пользователя без регистрации нельзя, должно быть отправлено сообщение об отстутствии прав'''
        user_to_block = self.create_user(session, app, db)
        app_answer = app.block_user(user_to_block['username'], {})
        user_not_blocked = not db.user_blocked(user_to_block['username'])
        assert user_not_blocked, "User was blocked in database"
        assert app_answer.status_code == 401, "Wrong status code"



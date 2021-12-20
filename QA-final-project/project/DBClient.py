import pymysql


class DataBase:
    cursor = None
    table = "test_users"
    def __init__(self, host, port, user, password, db):
        connection = pymysql.connect(host=host, port=port, user=user, password=password, db=db, autocommit=True)
        self.cursor = connection.cursor()
    
    def get_all_users_creds(self):
        self.cursor.execute(f'SELECT username, password, email FROM {self.table}')
        users = self.cursor.fetchall()
        return users
    
    def get_first_user_creds(self):
        self.cursor.execute(f'SELECT username, password, email FROM {self.table}')
        firstuser = self.cursor.fetchone()
        return firstuser
    
    def user_in_db(self, search_user):
        ''' users = self.get_all_users_creds()
        found = False
        for user in users:
            if user[0] == search_user['username'] and user[1] == search_user['password'] and user[2] == search_user['email']:
                found = True
                break'''
        username, password, email = search_user.values()
        self.cursor.execute('SELECT * FROM ' + self.table + ' WHERE username="' + username + '" AND password="' + password + '" AND email="' + email + '"')
        return len(self.cursor.fetchall()) != 0
    
    def user_blocked(self, username):
        self.cursor.execute('SELECT access FROM ' + self.table + ' WHERE username="' + username + '"')
        user = self.cursor.fetchone()
        return user[0] == 0

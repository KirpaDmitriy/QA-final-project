from http.client import HTTPConnection
import requests

HTTPConnection._http_vsn_str = "HTTP/1.1"


class Application:
    data = None
    
    def __init__(self, host, port, add_user, delete_user, block_user, unblock_user, status):
        self.data = {
             'host': host,
             'port': port,
             'url': ':'.join([host, str(port)]),
             'add_user': add_user,
             'del_user': delete_user,
             'block_user': block_user,
             'unblock_user': unblock_user,
             'status': status
        }
    
    def start(self):
        start = requests.get('/'.join([self.data['url'], self.data['status']]))
        return start
    
    def add_user(self, user, session):
        answer = requests.post('/'.join([self.data['url'], self.data['add_user']]), json=user, cookies=session)
        return answer
    
    def delete_user(self, username, session):
        answer = requests.get('/'.join([self.data['url'], self.data['del_user'], username]), cookies=session)
        return answer
    
    def block_user(self, username, session):
        answer = requests.get('/'.join([self.data['url'], self.data['block_user'], username]), cookies=session)
        return answer
    
    
    def unblock_user(self, username, session):
        answer = requests.get('/'.join([self.data['url'], self.data['unblock_user'], username]), cookies=session)
        return answer

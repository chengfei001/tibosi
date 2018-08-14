from requests import request, post
from json import loads,dumps
import logging
import sys


logging.basicConfig(level=logging.DEBUG)
users = {'18519197371': 'f8d5b32657d1f4b8f2c5aeb5b5606bce'}
class userLogin:
    def __init__(self,username):



        self.user = username
        # md5加密后的密码
        self.password = ''
        if users.get(self.user):
            self.password = users[username]
        else:
            logging.info('用户名不在抓取列表')
            sys.exit()


        self.guid = ''
        self.userID = ''
        self.appENama = ''
        self.appID = ''
        self.url_logoin = 'http://gfapinew.ksbao.com/api/user/userlogin'

        self.headers = {
            'Host':'gfapinew.ksbao.com',
            'User-Agent':'userAgent:Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:58.0) Gecko/20100101 Firefox/58.0',
            'Accept': '*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer':'http://wide.ksbao.com/html/start.html?ac=889',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'http://wide.ksbao.com'
        }

    def login(self):
        logging.info('login ....')

        data = {"username": self.user,
                "password": self.password,
                "clientType": "web_iPhone",
                "clientver": "wide.ksbao.com"}
        response = post(url=self.url_logoin, data=data)

        result = loads(response.text)
        # logging.info(result)
        if result['msg'] == '登陆成功.':
            self.guid = result['data']['guid']
            self.userID = result['data']['userID']
            self.appEName = result['data']['appEName']
            self.appID = result['data']['appID']
        else:
            logging.info(result['msg'] + response.text)
            sys.exit()

        logging.info(result['msg']+response.text)

    def run(self):
        self.login()

if __name__ == '__main__':
    user = userLogin('18519197371')
    user.run()


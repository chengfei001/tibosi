from requests import request, post
from json import loads,dumps
import logging


logging.basicConfig(level=logging.DEBUG)


class userLogin:
    def __init__(self):
        # 用户名
        self.usr = '15010670639'
        # md5加密后的密码
        self.password = '17a5d062129897b78c9a1f01f66f5bbe'
        self.guid = ''
        self.userID = ''
        self.appENama = ''
        self.url_logoin = 'http://gfapi.ksbao.com/api/user/userlogin'

        self.headers = {
            'Host':'gfapi.ksbao.com',
            'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': '*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer':'http://xxypc.tibosi.com/Old/practicing.html',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'http://xxypc.tibosi.com'
        }

    def login(self):
        logging.info('login ....')

        data = {"username": self.usr,
                "password": self.password}
        response = post(url=self.url_logoin, data=data)

        result = loads(response.text)
        # logging.info(result)
        if result['msg'] == '登陆成功.':
            self.guid = result['data']['guid']
            self.userID = result['data']['userID']
            self.appEName = result['data']['appEName']

        logging.info(result['msg']+response.text)

    def run(self):
        self.login()

if __name__ == '__main__':
    user  = userLogin()
    user.run()


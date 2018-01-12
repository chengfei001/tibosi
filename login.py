from requests import request, post
from json import loads,dumps
import logging
import sys


logging.basicConfig(level=logging.DEBUG)

users = {'15010670639': '17a5d062129897b78c9a1f01f66f5bbe',
        '13811378722': 'e10adc3949ba59abbe56e057f20f883e',
        '13671031359': 'e10adc3949ba59abbe56e057f20f883e',
        '18824329661': 'e10adc3949ba59abbe56e057f20f883e',
        '15210928290': 'e10adc3949ba59abbe56e057f20f883e',
        '18531246153': 'e10adc3949ba59abbe56e057f20f883e',
        '13811317037': 'e10adc3949ba59abbe56e057f20f883e'}
class userLogin:
    def __init__(self,username):

        # 18531246153
        # self.user = '18531246153'
        # self.password = 'e10adc3949ba59abbe56e057f20f883e'

        # 15210928290
        # self.user = '15210928290'
        # self.password = 'e10adc3949ba59abbe56e057f20f883e'

        # 18824329661 password：123456
        # self.user = '18824329661'
        # self.password = 'e10adc3949ba59abbe56e057f20f883e'

        #卓家进 手机 13671031359密码123456
        # self.user = '13671031359'
        # self.password = 'e10adc3949ba59abbe56e057f20f883e'

        # # 用户名 曹惠子
        # #4个学科，账号13811378722密码123456
        # #通用版-儿外科，通用版-急诊科，通用版-精神科，通用版-麻醉科

        # self.user = '13811378722'
        # # md5加密后的密码
        # self.password = 'e10adc3949ba59abbe56e057f20f883e'
        #
        # # 用户名  内科 儿科 妇科
        # self.user = '15010670639'
        # # md5加密后的密码
        # self.password = '17a5d062129897b78c9a1f01f66f5bbe'


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
        self.url_logoin = 'http://gfapi.ksbao.com/api/user/userlogin'

        self.headers = {
            'Host':'gfapi.ksbao.com',
            'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': '*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer':'http://xxypc.tibosi.com/Old/practicing.html',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'http://wide.ksbao.com/html/softMenu1.html'
        }

    def login(self):
        logging.info('login ....')

        data = {"username": self.user,
                "password": self.password}
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
    user = userLogin('13671031359')
    user.run()


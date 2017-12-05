from requests import request, post
from json import loads
import logging
logging.basicConfig(level=logging.DEBUG)


class loginTest:
    def __init__(self):
        #用户名
        self.usr = '18687157918'
        #md5加密后的密码
        self.password = '25d55ad283aa400af464c76d713c07ad'
        self.sid = ''
        self.userID =''
        self.url_logoin = 'http://114.55.128.51:7051/user/login'
        self.url_verifyCode = 'http://114.55.128.51:7051/user/register/getVerifyCode'
        self.guidCode = ''
        self.url_appone = 'http://114.55.128.51:7051/appManage/appOne'
        self.url_appTwo = 'http://114.55.128.51:7051/appManage/appTwo'
        self.url_appThree = 'http://114.55.128.51:7051/appManage/appThree'
        self.url_chapterApi = 'http://114.55.128.51:7051/appManage/chapterApi'
        self.url_examList = 'http://114.55.128.51:7051/exam/examList'

        self.headers = {
            'Host':'114.55.128.51:7051',
            'User-Agent':'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:57.0) Gecko/20100101 Firefox/57.0',
            'Accept': '*/*',
            'Accept-Language':'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Referer':'http://xxypc.tibosi.com/Old/practicing.html',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'http://xxypc.tibosi.com'
        }




    def login(self):
        logging.info('login ....')

        data = {"usr":self.usr,
                "pwd":self.password}
        response = post(url=self.url_logoin, data=data)

        result = loads(response.text)
        logging.info(result)
        if result['data']['code'] == 1:
            self.sid = result['data']['sid']
            self.userID = result['data']['userID']

            logging.info(self.sid)
            logging.info(self.userID)

            verifyCode_data = {"sid":self.userID,
                               "userID":self.userID}
            response = request(method='get', url=self.url_verifyCode, data = verifyCode_data)
            self.guidCode = loads(response.text)['guidCode']

            logging.info(response.text)
            logging.info(self.guidCode)



            #获取学科分类
            appon_data = {"userID": self.userID,
                          "sid": self.sid}
            response = post(url=self.url_appone, headers=self.headers, data=appon_data)
            logging.info(response.text)


            #学科级别分类
            appon_data = {"userID": self.userID,
                          "sid": self.sid,
                          'AppClassID': loads(response.text)['data'][0]['AppClassID']}
            response = post(url=self.url_appTwo, headers=self.headers, data=appon_data)
            logging.info(response.text)


            #最小分类
            appon_data = {"userID": self.userID,
                          "sid": self.sid,
                          'AppClassID': loads(response.text)['data'][0]['AppClassID']}
            response = post(url=self.url_appThree, headers=self.headers, data=appon_data)
            logging.info(response.text)


            #学科最小分类下的习题分类
            appon_data = {"userID": self.userID,
                          "sid": self.sid,
                          'AppEName': loads(response.text)['data'][0]['AppEName']}
            response = post(url=self.url_chapterApi, headers=self.headers, data=appon_data)
            logging.info(response.text)


            logging.info('````````````````'+loads(response.text)['data'][0]['Child'][0]['Child'][0]['AppID'])
            logging.info('````````````````' + loads(response.text)['data'][0]['Child'][0]['Child'][0]['ExamCptID'])
            # #具体考题
            # 强化练习     response.text)['data'][0]
            #     |
            #     ————强化练习    esponse.text)['data'][0]['Child'][0]
            #             |
            #             ————麻醉相关解剖生理基础（多选题） response.text)['data'][0]['Child'][0]['Child'][0]
            appon_data = {"userID": self.userID,
                          "sid": self.sid,
                          "AppID": loads(response.text)['data'][0]['Child'][0]['Child'][0]['AppID'],
                          "ExamCptID": loads(response.text)['data'][0]['Child'][0]['Child'][0]['ExamCptID']}
            logging.info(appon_data)
            response = post(url=self.url_examList, headers=self.headers, data=appon_data)
            logging.info(response.text)

    def run(self):
        self.login()


if __name__ == '__main__':

    login = loginTest()
    login.run()



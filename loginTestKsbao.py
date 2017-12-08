from requests import request, post
from json import loads
import logging
logging.basicConfig(level=logging.DEBUG)


class loginTest:
    def __init__(self):
        #用户名
        self.usr = '15010670639'
        #md5加密后的密码
        self.password = '17a5d062129897b78c9a1f01f66f5bbe'
        self.guid = ''
        self.userID = ''
        self.appENama = ''
        self.url_logoin = 'http://gfapi.ksbao.com/api/user/userlogin'
        self.url_verifyCode = 'http://gfapi.ksbao.com/api/app/appVersionInfo?appENames=ZYYS_JSQKYX&appVer=0&agentCode=889&clientver=wide.ksbao.com'
        self.url_vipinfo = 'http://gfapi.ksbao.com/api/user/vipinfo?appEName=ZYYS_JSQKYX&guid=DEmXrR5TXeBgpJgzT1NN1RHLtEaYjwby3234143&appVn=1&clientver=wide.ksbao.com'
        self.url_chapterTestEx ='http://gfapi.ksbao.com/api/exam/getChapterTestEx'
        self.guidCode = ''
        # self.url_appone = 'http://114.55.128.51:7051/appManage/appOne'
        # self.url_appTwo = 'http://114.55.128.51:7051/appManage/appTwo'
        # self.url_appThree = 'http://114.55.128.51:7051/appManage/appThree'
        # self.url_chapterApi = 'http://114.55.128.51:7051/appManage/chapterApi'
        # self.url_examList = 'http://114.55.128.51:7051/exam/examList'

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

        data = {"username":self.usr,
                "password":self.password}
        response = post(url=self.url_logoin, data=data)

        result = loads(response.text)
        logging.info(result)
        if result['msg'] == '登陆成功.':
            self.guid = result['data']['guid']
            self.userID = result['data']['userID']
            self.appENama = result['data']['appEName']

            TestEx_data = {"appID":1334,
                           "cptID":1,
                           "queryHistory":1,
                           "queryTestInfo":1,
                           "queryKnowledge":1,
                           "guid":self.guid,
                           "agentCode":888,
                           "clientver":"wide.ksbao.com"}
            response = post(url=self.url_chapterTestEx, headers=self.headers, data=TestEx_data)
            logging.info(response.text)

            # verifyCode_data = {"sid":self.userID,
            #                    "userID":self.userID}
            # response = request(method='get', url=self.url_verifyCode, data = verifyCode_data)
            # self.guidCode = loads(response.text)['guidCode']
            #
            # logging.info(response.text)
            # logging.info(self.guidCode)



            #获取学科分类
            # appon_data = {"userID": self.userID,
            #               "sid": self.sid}
            # response = post(url=self.url_appone, headers=self.headers, data=appon_data)
            # logging.info(response.text)


            # #学科级别分类
            # appon_data = {"userID": self.userID,
            #               "sid": self.sid,
            #               'AppClassID': loads(response.text)['data'][0]['AppClassID']}
            # response = post(url=self.url_appTwo, headers=self.headers, data=appon_data)
            # logging.info(response.text)
            # # appon_data = {"userID": self.userID,
            # #               "sid": self.sid,
            # #               'AppClassID': 1754}
            # # response = post(url=self.url_appTwo, headers=self.headers, data=appon_data)
            # # logging.info(response.text)
            #
            #
            # #最小分类
            # appon_data = {"userID": self.userID,
            #               "sid": self.sid,
            #               'AppClassID': loads(response.text)['data'][0]['AppClassID']}
            # response = post(url=self.url_appThree, headers=self.headers, data=appon_data)
            # logging.info(response.text)
            #     # appon_data = {"userID": self.userID,
            #     #               "sid": self.sid,
            #     #               'AppClassID': 6116}
            #     # response = post(url=self.url_appThree, headers=self.headers, data=appon_data)
            #     # logging.info(response.text)
            #
            #
            # #学科最小分类下的习题分类
            # appon_data = {"userID": self.userID,
            #               "sid": self.sid,
            #               'AppEName': loads(response.text)['data'][0]['AppEName']}
            # response = post(url=self.url_chapterApi, headers=self.headers, data=appon_data)
            # logging.info(response.text)
            #
            #

            #
            # # #具体考题
            # # 强化练习     response.text)['data'][0]
            # #     |
            # #     ————强化练习    esponse.text)['data'][0]['Child'][0]
            # #             |
            # #             ————麻醉相关解剖生理基础（多选题） response.text)['data'][0]['Child'][0]['Child'][0]
            # appon_data = {"userID": self.userID,
            #               "sid": self.sid,
            #               "AppID": loads(response.text)['data'][0]['Child'][0]['Child'][0]['AppID'],
            #               "ExamCptID": loads(response.text)['data'][0]['Child'][0]['Child'][0]['ExamCptID']}
            # logging.info(appon_data)
            # response = post(url=self.url_examList, headers=self.headers, data=appon_data)
            # logging.info(response.text)
            #
            # # appon_data = {"userID": self.userID,
            # #               "sid": self.sid,
            # #               "AppID": 'b2215065-bc4b-11e6-b1a9-00163e0157d1',
            # #               "ExamCptID": '53e33011-991b-4285-bcc7-8b9482579610'}
            # # logging.info(appon_data)
            # # response = post(url=self.url_examList, headers=self.headers, data=appon_data)
            # # logging.info(response.text)

    def run(self):
        self.login()


if __name__ == '__main__':

    login = loginTest()
    login.run()



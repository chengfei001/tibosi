from requests import request, post
from json import loads,dumps
import logging
from  pymongo import  MongoClient
import time
import datetime

logging.basicConfig(level=logging.DEBUG)
client = MongoClient('localhost',27017)
db = client.ksbao
ksbao_test = db.ksbao_test9
# ksbao_testInfo = db.ksbao_testInfo




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
        #获取agent信息 886
        #获取菜单  appEName从数据看直接获取
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?appEName=ZYYS_NK&clientver=wide.ksbao.com'
        self.url_chapterTestEx ='http://gfapi.ksbao.com/api/exam/getChapterTestEx'
        self.url_soft_menu = 'http://gfapi.ksbao.com/api/softMenu/getNew?agentCode=889&clientver=wide.ksbao.com'
        self.guidCode = ''
        self.appID = '751'
        self.cptID = ''
        self.agentCode = 886
        self.login_appID = ''
        self.login_appEName = ''



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
        #登录
        logging.info('login ....')


        data = {"username":self.usr,
                "password":self.password}
        response = post(url=self.url_logoin, data=data)

        result = loads(response.text)
        # logging.info(result)
        if result['msg'] == '登陆成功.':
            self.guid = result['data']['guid']
            self.userID = result['data']['userID']
            self.appENama = result['data']['appEName']

            #科目
            response = request(method='get', url=self.url_soft_menu, headers=self.headers)

            context = loads(response.text)
            logging.info(context['data'])


            # logging.info(loads(response.text))
            # logging.info(self.guidCode)

            # response = request(method='get', url=self.chapterMenuX, headers=self.headers)
            #
            # menuInfo = loads(response.text)
            # menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            # logging.info(menuInfo['data']['ChapterMenuJson'])
            # for menu_level2 in menuInfo2['Childs']:
            #     # INFO: root:1
            #     # INFO: root:2
            #     # INFO: root:3
            #     # INFO: root:4
            #     # INFO: root:5
            #     # INFO: root:6
            #     # INFO: root:7
            #     # INFO: root:8
            #     # INFO: root:10
            #     # INFO: root:11
            #     # INFO: root:13
            #     # INFO: root:14
            #     # INFO: root:16
            #     logging.info(loads(menu_level2))
            #     for menu_level3 in menu_level2['Childs']:
            #
            #             for  testEx_item in menuInfo2['Childs'][0]['Childs'][0]['Childs']:
            #                 arr_testEx_items = []
            #                 #考题
            #
            #                 TestEx_data = {"appID":self.appID,
            #                                "cptID":testEx_item['ID'],
            #                                "queryHistory":1,
            #                                "queryTestInfo":1,
            #                                "queryKnowledge":1,
            #                                "guid":self.guid,
            #                                "agentCode":self.agentCode,
            #                                "clientver":"wide.ksbao.com"}
            #                 logging.info(TestEx_data)
            #                 response = post(url=self.url_chapterTestEx, headers=self.headers, data=TestEx_data)
            #
            #                 testEx_info = loads(response.text)
            #
            #                 # logging.info(testEx_info)
            #
            #                 for testEx_items in testEx_info['data']['test']['StyleItems']:
            #                     for testEx_item in testEx_items['TestItems']:
            #                         arr_testEx_items.append(testEx_item)
            #                         # logging.info(testEx_item)
            #                 ksbao_test.insert_many(arr_testEx_items)
            #             logging.warning("休息2分钟继续抓......")
            #             time.sleep(120)
    def delete_code(self):
        logging.info("临时代码存放处")
        # for testEx_item in testEx_info['data']['test']['StyleItems'][0]['TestItems']:
        # testEx_items.append(testEx_info['data']['test']['StyleItems'][0]['TestItems'][0])
        #     logging.info(testEx_item)


        # logging.info(menuInfo)
        # logging.info(menuInfo['data'])
        # logging.info(menuInfo['data']['ChapterMenuJson'])
        # 章节练习下列表
        # logging.info(loads(menuInfo['data']['ChapterMenuJson']))
        # 最小分类 习题集 or 公共科目 的下级
        # logging.info(menuInfo2['Childs'][0])
        # 试卷列表
        # logging.info(menuInfo2['Childs'][0]['Childs'][0])

        #
        # #考题ID
        # logging.info(menuInfo2['Childs'][0]['Childs'][0]['Childs'][0])

        # testEx_items = []

        # for  testEx_item in menuInfo2['Childs'][0]['Childs'][0]['Childs']:
        #     #考题
        #     TestEx_data = {"appID":self.appID,
        #                    "cptID":testEx_item['ID'],
        #                    "queryHistory":1,
        #                    "queryTestInfo":1,
        #                    "queryKnowledge":1,
        #                    "guid":self.guid,
        #                    "agentCode":self.agentCode,
        #                    "clientver":"wide.ksbao.com"}
        #     response = post(url=self.url_chapterTestEx, headers=self.headers, data=TestEx_data)
        #     testEx_info = loads(response.text)
        #     for testEx_item in testEx_info['data']['test']['StyleItems'][0]['TestItems']:
        #     testEx_items.append(testEx_info['data']['test']['StyleItems'][0]['TestItems'][0])
        #
        # ksbao_test.insert_many(testEx_items)


        # logging.info(testEx_info)
        # logging.info(testEx_info['data']['test']['StyleItems'][0]['TestItems'][0])

        # ksbao_test = loads(testEx_info['data']['test']['StyleItems'][0]['TestItems'][0])
        # for testEx_item in testEx_info['data']['test']['StyleItems'][0]['TestItems']:
        # testEx_items.append(testEx_info['data']['test']['StyleItems'][0]['TestItems'][0])
        #     logging.info(testEx_item)
        #
        # logging.info(testEx_item['Title'])



        # verifyCode_data = {"sid":self.userID,
        #                    "userID":self.userID}
        # response = request(method='get', url=self.url_verifyCode, data = verifyCode_data)
        # self.guidCode = loads(response.text)['guidCode']
        #
        # logging.info(response.text)
        # logging.info(self.guidCode)



        # 获取学科分类
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
    start = time.time()

    login = loginTest()
    login.run()
    # long running
    # do something other
    end = time.time()
    print(end - start)



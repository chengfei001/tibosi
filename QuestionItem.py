from requests import request, post
from pymongo import MongoClient
from json import loads, dumps
import logging

from login import userLogin
import CryptoDesUtil

logging.basicConfig(level = logging.DEBUG)

#mongoDB
client = MongoClient(host='localhost', port=27017)
db = client.kaoshibaodian_base
db_questionItem = client.QuestionItem
db_questionAnswer = client.QuestionAnswer
db_PoolItem = db.PoolItem

#要抓取的科室
appENames = {'ZYYS_NK'}

class QuestionItem:
    def __init__(self):
        self.appID = '751'
        self.agentCode = 886
        # self.guid = ''
        self.url_chapterTestEx = 'http://gfapi.ksbao.com/api/exam/getChapterTestEx'
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.user = userLogin()
        self.user.run()

    def getQuestionItem(self):
        logging.info('strat')
        for appEName in appENames:
            response = request(method='get', url=self.chapterMenuX % (appEName), headers=self.user.headers)
            menuInfo = loads(response.text)
            menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            for testEx_item in menuInfo2['Childs'][0]['Childs'][0]['Childs']:
                arr_testEx_items = []
                # 考题

                TestEx_data = {"appID": self.appID,
                               "cptID": testEx_item['ID'],
                               "queryHistory": 1,
                               "queryTestInfo": 1,
                               "queryKnowledge": 1,
                               "guid": self.user.guid,
                               "agentCode": self.agentCode,
                               "clientver": "wide.ksbao.com"}
                logging.info(TestEx_data)
                response = post(url=self.url_chapterTestEx, headers=self.user.headers, data=TestEx_data)

                testEx_info = loads(response.text)

                # logging.info(response.text)
                #获取TestInfo信息，答题人数、答对人数、收藏人数、讨论人数、解析人数、等信息，以字典的方式保存，供后面程序合并保存
                testInfo ={}
                for testInfo_items in testEx_info['data']['testInfo']:
                    testInfo[testInfo_items['AllTestID']] = testInfo_items['Statistics']['Test']

                for testEx_items in testEx_info['data']['test']['StyleItems']:
                    for testEx_item in testEx_items['TestItems']:

                        # arr_testEx_items.append(testEx_item)
                        #ATEST处理方式
                        if testEx_item == 'ATEST':
                            testEx_item['Title'] = CryptoDesUtil.DESUtil.decrypt(testEx_item['Title'])
                            logging.info(dumps(dict(testEx_item, **testInfo[testEx_item['AllTestID']])))
                        elif testEx_item == 'BTEST':
                            a='1'
                        elif testEx_item == 'A3TEST':
                            a = '1'
                # ksbao_test.insert_many(arr_testEx_items)
            logging.warning("休息2分钟继续抓......")

    def run(self):
        self.getQuestionItem()


if __name__ == '__main__':
    questionItem = QuestionItem()
    questionItem.run()
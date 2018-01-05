from requests import request, post
from pymongo import MongoClient
from json import loads, dumps
import time
import logging

from login import userLogin
import CryptoDesUtil

logging.basicConfig(level = logging.INFO)

#mongoDB
client = MongoClient(host='localhost', port=27017)
db = client.kaoshibaodian_base
# db2 = client.kaoshibaodian_base1
db_questionItem = db.QuestionItem
db_questionAnswer = db.QuestionAnswer
db_PoolItem = db.PoolItem

#要抓取的科室
appENames = {'ZYYS_NK'}

class QuestionItem:
    def __init__(self):
        #确认课程抓取时AppID需要从数据库中获取
        self.appID = '751'
        self.agentCode = 886
        # self.guid = ''
        self.url_chapterTestEx = 'http://gfapi.ksbao.com/api/exam/getChapterTestEx'
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.user = userLogin()
        self.user.run()

    def getQuestionItem(self):
        logging.info('strat')
        desUtil = CryptoDesUtil.DESUtil()
        for appEName in appENames:
            response = request(method='get', url=self.chapterMenuX % (appEName), headers=self.user.headers)
            menuInfo = loads(response.text)
            menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            for menu_level2 in menuInfo2['Childs']:
                # 一级菜单名称
                srcName = menu_level2['Name']
                # logging.info(loads(menu_level2))
                for menu_level3 in menu_level2['Childs']:
                    sbjName = menu_level3['Name']
                    for testEx_item in menuInfo2['Childs'][0]['Childs'][0]['Childs']:
                        # 二级菜单名称
                        # 试卷名称
                        cptName = testEx_item['Name']
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
                        # logging.info(TestEx_data)
                        response = post(url=self.url_chapterTestEx, headers=self.user.headers, data=TestEx_data)

                        testEx_info = loads(response.text)

                        # logging.info(response.text)
                        #获取TestInfo信息，答题人数、答对人数、收藏人数、讨论人数、解析人数、等信息，以字典的方式保存，供后面程序合并保存
                        testInfo ={}
                        for testInfo_items in testEx_info['data']['testInfo']:
                            if testInfo_items['ChildTableID'] == -1 :
                                testInfo[testInfo_items['AllTestID']] = testInfo_items['Statistics']['Test']
                            else:
                                testInfo[str(testInfo_items['AllTestID'])+'-'+str(testInfo_items['ChildTableID'])] = testInfo_items['Statistics']['Test']
                                logging.info(str(testInfo_items['AllTestID'])+'-'+str(testInfo_items['ChildTableID']))
                            # logging.debug("testInfo")


                        for testEx_items in testEx_info['data']['test']['StyleItems']:
                            # logging.debug("test_items")
                            test_ex_StyleID = testEx_items['StyleID']
                            test_ex_Style = testEx_items['Style']
                            test_ex_Explain = testEx_items['Explain']
                            test_ex_Score = testEx_items['Score']
                            test_ex_Type = testEx_items['Type']
                            test_ex_SubType = testEx_items['SubType']
                            for testEx_item in testEx_items['TestItems']:

                                # logging.debug("test_Item")
                                # logging.debug(testEx_item)
                                # 公共数据部分


                                testEx_item['StyleID'] = testEx_items['StyleID']
                                testEx_item['Style'] = testEx_items['Style']
                                testEx_item['Explain'] = testEx_items['Explain']
                                testEx_item['Score'] = testEx_items['Score']
                                testEx_item['Type'] = testEx_items['Type']
                                testEx_item['SubType'] = testEx_items['SubType']
                                # 一级菜单名称
                                testEx_item['srcName'] = srcName
                                # 二级菜单名称
                                testEx_item['sbjName'] = sbjName
                                # 试卷名称
                                testEx_item['CptName'] = cptName
                                # testEx_item['AppID'] = self.appID
                                '''
                                TestInfo
                                '''
                                # if testEx_item.get('AllTestID'):
                                #     testInfoStatistics = testInfo[testEx_item['AllTestID']]
                                #     testEx_item['AppID'] = testInfoStatistics['AppID']
                                #     testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                #     testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                #     testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                #     testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                #     testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                #     testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                #     testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']

                                #ATEST处理方式

                                if testEx_items['Type'] == 'ATEST':
                                    logging.debug("==========ATEST==========")
                                    if testEx_item.get('AllTestID'):
                                        testInfoStatistics = testInfo[testEx_item['AllTestID']]
                                        testEx_item['AppID'] = testInfoStatistics['AppID']
                                        testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                        testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                        testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                        testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                        testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                        testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                        testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']
                                    testEx_item['Title'] = desUtil.decrypt(ciphertext=testEx_item['Title'])
                                    db_questionItem.insert(testEx_item)
                                    logging.info(testEx_item)
                                # BTEST题 增加BTestID、BTestItems、FrontTitle
                                elif testEx_items['Type'] == 'BTEST':

                                    logging.debug("==========BTEST==========")
                                    # FrontTitle必须放在循环外面，否足MongoDB会报_ID重复的错误
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    bTest_items = testEx_item['BTestItems']
                                    for bTest_item in testEx_item['BTestItems']:
                                        if testEx_item.get('AllTestID'):
                                            logging.info(bTest_item)
                                            testInfoStatistics = testInfo[str(testEx_item['AllTestID']) + '-' + str(bTest_item['BTestItemID'])]
                                            testEx_item['AppID'] = testInfoStatistics['AppID']
                                            testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                            testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                            testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                            testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                            testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                            testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                            testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']

                                        testEx_item['BTestItemID'] = bTest_item['BTestItemID']
                                        testEx_item['Explain'] = bTest_item['Explain']
                                        testEx_item['TestPoint'] = bTest_item['TestPoint']
                                        testEx_item['Answer'] = bTest_item['Answer']
                                        testEx_item['Title'] = desUtil.decrypt(ciphertext=bTest_item['Title'])
                                        db_questionItem.insert(testEx_item.copy())
                                        logging.info(testEx_item)


                                # A3TEST题 增加A3TestID、A3TestItems、FrontTitle
                                elif testEx_items['Type'] == 'A3TEST':
                                    logging.debug("==========A3TEST==========")
                                    # FrontTitle必须放在循环外面，否足MongoDB会报_ID重复的错误
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    for a3Test_item in testEx_item['A3TestItems']:
                                        if testEx_item.get('AllTestID'):
                                            testInfoStatistics = testInfo[str(testEx_item['AllTestID']) + '-' + str(a3Test_item['A3TestItemID'])]
                                            testEx_item['AppID'] = testInfoStatistics['AppID']
                                            testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                            testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                            testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                            testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                            testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                            testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                            testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']

                                        testEx_item['A3TestItemID'] = a3Test_item['A3TestItemID']
                                        testEx_item['Explain'] = a3Test_item['Explain']
                                        testEx_item['TestPoint'] = a3Test_item['TestPoint']
                                        testEx_item['Answer'] = a3Test_item['Answer']
                                        testEx_item['SelectedItems'] = a3Test_item['SelectedItems']
                                        testEx_item['Title'] = desUtil.decrypt(ciphertext=a3Test_item['Title'])

                                        db_questionItem.insert(testEx_item.copy())
                                        logging.info(testEx_item)
                                    # logging.info("==============A3TEST===========")
                                # logging.info(testEx_item)

                        logging.warning("休息2分钟继续抓......")
                        time.sleep(75)

    def run(self):
        self.getQuestionItem()


if __name__ == '__main__':
    questionItem = QuestionItem()
    questionItem.run()
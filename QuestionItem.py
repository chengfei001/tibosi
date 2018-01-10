from requests import request, post
from pymongo import MongoClient
from json import loads, dumps
import time
import logging
import random
import time

from login import userLogin
import CryptoDesUtil

logging.basicConfig(level=logging.INFO)

# mongoDB
client = MongoClient(host='localhost', port=27017)
db = client.kaoshibaodian_base
# db2 = client.kaoshibaodian_base1
db_questionItem = db.QuestionItem
db_questionAnswer = db.QuestionAnswer
db_PoolItem = db.PoolItem

# 曹惠子账号 13811378722 ，通用版-麻醉科，通用版-精神科，通用版-儿外科，通用版-急诊科
# appENames = '["ZYYS_MZK","ZYYS_JSK","ZYYS_EWK","ZYYS_JZK"]'
appENames = '["ZYYS_MZK","ZYYS_JZK","ZYYS_JSK"]'


# # 要抓取的科室 何燕账号 1506
# # appENames = {'ZYYS_WK'}#{'ZYYS_NK', 'ZYYS_WK', 'ZYYS_EK', 'ZYYS_FCK'}
# appENames = '["ZYYS_NK", "ZYYS_WK", "ZYYS_EK", "ZYYS_FCK"]'

class QuestionItem:
    def __init__(self):
        # 确认课程抓取时AppID需要从数据库中获取

        self.agentCode = 886
        # self.guid = ''
        self.url_chapterTestEx = 'http://gfapi.ksbao.com/api/exam/getChapterTestEx'
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.appVersion = 'http://gfapi.ksbao.com/api/app/appVersionInfo?appENames=%s&guid=%s&agentCode=889&clientver=wide.ksbao.com'
        self.user = userLogin()
        self.user.run()
        # self.appID = self.user.appID
        self.sleepSec = 65

    def getQuestionItem(self):
        # logging.info(self.appID)
        start = time.time()
        logging.info('strat')
        desUtil = CryptoDesUtil.DESUtil()
        num = 0
        num2 = 0
        allType = {}
        logging.info(appENames)
        response = request(method='get', url=self.appVersion % (appENames, self.user.guid), headers=self.user.headers)
        apps = loads(response.text)['data']
        for app in apps:
            logging.error('-----------------' + str(app['AppID']) + ':' + app['AppEName'] + '---------------')
            response = request(method='get', url=self.chapterMenuX % (app['AppEName']), headers=self.user.headers)
            menuInfo = loads(response.text)
            # logging.info(menuInfo)
            menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            for menu_level2 in menuInfo2['Childs']:
                # 一级菜单名称
                srcName = menu_level2['Name']
                # logging.info('----------'+dumps(menu_level2))
                for menu_level3 in menu_level2['Childs']:
                    sbjName = menu_level3['Name']
                    for testEx_item in menu_level3['Childs']:
                        # 二级菜单名称
                        # 试卷名称
                        cptName = testEx_item['Name']
                        logging.info('@@@@@@@@@@@@@@@@@' + str(testEx_item['ID']) + '.' + cptName + '@@@@@@@@@@@@@@@@@')
                        # arr_testEx_items = []
                        # 考题
                        TestEx_data = {"appID": app['AppID'],
                                       "cptID": testEx_item['ID'],
                                       "queryHistory": 1,
                                       "queryTestInfo": 1,
                                       "queryKnowledge": 1,
                                       "guid": self.user.guid,
                                       "agentCode": self.agentCode,
                                       "clientver": "wide.ksbao.com"}
                        response = post(url=self.url_chapterTestEx, headers=self.user.headers, data=TestEx_data)
                        logging.info(response.text)
                        testEx_info = loads(response.text)
                        logging.info(testEx_item)
                        # 获取TestInfo信息，答题人数、答对人数、收藏人数、讨论人数、解析人数、等信息，以字典的方式保存，供后面程序合并保存
                        testInfo = {}
                        for testInfo_items in testEx_info['data']['testInfo']:
                            if testInfo_items['ChildTableID'] == -1:
                                testInfo[testInfo_items['AllTestID']] = testInfo_items['Statistics']['Test']
                            else:
                                testInfo[str(testInfo_items['AllTestID']) + '-' + str(testInfo_items['ChildTableID'])] = testInfo_items['Statistics']['Test']
                            num2 = num2 + 1

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

                                # appEName
                                testEx_item['appEName'] = app['AppEName']
                                # 图片路径
                                testEx_item['pic_path'] = 'http://t.api.ksbao.com/tk_img/ImgDir_%s/' % (app['AppEName'])
                                testEx_item['AppID'] = app['AppID']
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

                                allType[testEx_items['Type']] = 'test'
                                logging.debug("==========" + testEx_items['Type'] + "==========")
                                # ATEST处理方式
                                if testEx_items['Type'] == 'ATEST' or testEx_items['Type'] == 'XTEST':
                                    # logging.debug("=========="+testEx_items['Type']+"==========")
                                    if testEx_item.get('AllTestID'):
                                        if testInfo[testEx_item['AllTestID']] is not None:
                                            testInfoStatistics = testInfo[testEx_item['AllTestID']]
                                            testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                            testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                            testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                            testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                            testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                            testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                            testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']
                                        else:
                                            testEx_item['ChildTableID'] = -1
                                            testEx_item['UserCount'] = 0
                                            testEx_item['RightCount'] = 0
                                            testEx_item['FavCount'] = 0
                                            testEx_item['DiscussionCount'] = 0
                                            testEx_item['ExplainCount'] = 0
                                            testEx_item['ConcernCount'] = 0

                                    testEx_item['Title'] = desUtil.decrypt(ciphertext=testEx_item['Title'])
                                    db_questionItem.insert(testEx_item)
                                    logging.info(testEx_item)
                                    num = num + 1
                                # BTEST题 增加BTestID、BTestItems、FrontTitle
                                elif testEx_items['Type'] == 'BTEST':

                                    # logging.debug("==========BTEST==========")
                                    # FrontTitle必须放在循环外面，否足MongoDB会报_ID重复的错误
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    bTest_items = testEx_item['BTestItems']
                                    for bTest_item in testEx_item['BTestItems']:
                                        if testEx_item.get('AllTestID'):
                                            if testInfo[str(testEx_item['AllTestID']) + '-' + str(bTest_item['BTestItemID'])] is not None:
                                                testInfoStatistics = testInfo[str(testEx_item['AllTestID']) + '-' + str(bTest_item['BTestItemID'])]
                                                testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                                testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                                testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                                testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                                testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                                testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                                testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']
                                            else:
                                                testEx_item['ChildTableID'] = -1
                                                testEx_item['UserCount'] = 0
                                                testEx_item['RightCount'] = 0
                                                testEx_item['FavCount'] = 0
                                                testEx_item['DiscussionCount'] = 0
                                                testEx_item['ExplainCount'] = 0
                                                testEx_item['ConcernCount'] = 0

                                        testEx_item['BTestItemID'] = bTest_item['BTestItemID']
                                        testEx_item['Explain'] = bTest_item['Explain']
                                        testEx_item['TestPoint'] = bTest_item['TestPoint']
                                        testEx_item['Answer'] = bTest_item['Answer']
                                        testEx_item['Title'] = desUtil.decrypt(ciphertext=bTest_item['Title'])
                                        db_questionItem.insert(testEx_item.copy())
                                        logging.info(testEx_item)
                                        num = num + 1


                                # A3TEST题 增加A3TestID、A3TestItems、FrontTitle
                                elif testEx_items['Type'] == 'A3TEST':
                                    # logging.debug("==========A3TEST==========")
                                    # FrontTitle必须放在循环外面，否足MongoDB会报_ID重复的错误
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    for a3Test_item in testEx_item['A3TestItems']:
                                        if testEx_item.get('AllTestID'):
                                            if testInfo[str(testEx_item['AllTestID']) + '-' + str(a3Test_item['A3TestItemID'])] is not None:
                                                testInfoStatistics = testInfo[str(testEx_item['AllTestID']) + '-' + str(a3Test_item['A3TestItemID'])]
                                                testEx_item['ChildTableID'] = testInfoStatistics['ChildTableID']
                                                testEx_item['UserCount'] = testInfoStatistics['UserCount']
                                                testEx_item['RightCount'] = testInfoStatistics['RightCount']
                                                testEx_item['FavCount'] = testInfoStatistics['FavCount']
                                                testEx_item['DiscussionCount'] = testInfoStatistics['DiscussionCount']
                                                testEx_item['ExplainCount'] = testInfoStatistics['ExplainCount']
                                                testEx_item['ConcernCount'] = testInfoStatistics['ConcernCount']
                                            else:
                                                testEx_item['ChildTableID'] = -1
                                                testEx_item['UserCount'] = 0
                                                testEx_item['RightCount'] = 0
                                                testEx_item['FavCount'] = 0
                                                testEx_item['DiscussionCount'] = 0
                                                testEx_item['ExplainCount'] = 0
                                                testEx_item['ConcernCount'] = 0

                                        testEx_item['A3TestItemID'] = a3Test_item['A3TestItemID']
                                        testEx_item['Explain'] = a3Test_item['Explain']
                                        testEx_item['TestPoint'] = a3Test_item['TestPoint']
                                        testEx_item['Answer'] = a3Test_item['Answer']
                                        testEx_item['SelectedItems'] = a3Test_item['SelectedItems']
                                        testEx_item['Title'] = desUtil.decrypt(ciphertext=a3Test_item['Title'])

                                        db_questionItem.insert(testEx_item.copy())
                                        logging.info(testEx_item)
                                        num = num + 1
                        # 休眠时间
                        self.sleepSec = random.randint(15, 55)

                        logging.warning("休息" + str(self.sleepSec) + "秒继续抓......")
                        logging.info('num:' + str(num))
                        logging.info('num2:' + str(num2))
                        logging.info(allType)
                        time.sleep(self.sleepSec)

        end = time.time()
        print((end - start) / 60)

    def run(self):
        self.getQuestionItem()


if __name__ == '__main__':
    questionItem = QuestionItem()
    questionItem.run()

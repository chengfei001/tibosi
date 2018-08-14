from requests import request, post
from pymongo import MongoClient
from json import loads, dumps
import time
import logging
import random
import time

from login_2018 import userLogin
import CryptoDesUtil


#主抓去进程
logging.basicConfig(level=logging.INFO, filemode='ChapterTestEx.log', format='%(asctime)s - %(levelname)s - %(message)s')

# mongoDB
client = MongoClient(host='localhost', port=27017)
db = client.kaoshibaodian_base_new_2018
db_questionItem = db.QuestionItem
apps = [{'user': '18519197371', 'apps': '[\"YSDQKH_GGWSYS\"]'}
        ]

userList = {'18519197371'}



# 主抓去进程
class QuestionItem:
    def __init__(self):
        # 确认课程抓取时AppID需要从数据库中获取

        self.agentCode = 886
        # self.guid = ''
        self.url_chapterTestEx = 'http://gfapinew.ksbao.com/api/exam/getChapterTestEx'
        self.chapterMenuX = 'http://gfbjapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.appVersion = 'http://gfapinew.ksbao.com/api/app/appVersionInfo?appENames=%s&guid=%s&clientver=wide.ksbao.com'
        # self.user = userLogin()
        # self.user.run()

    def getQuestionItem(self):

        start = time.time()
        # logging.info(self.appID)
        desUtil = CryptoDesUtil.DESUtil()
        num = 0
        num2 = 0
        allType = {}
        logging.info(self.appENames)
        logging.info(self.user.guid)
        logging.info(self.appVersion % (self.appENames, self.user.guid))
        response = request(method='get', url=self.appVersion % (self.appENames, self.user.guid), headers=self.user.headers)
        logging.info(response.text)

        apps = loads(response.text)['data']
        for app in apps:
            # 为了应对2018版，程序变更，现在同一个科室可能会有两个科室，一个vip一个非vip，可能2019年还会出现更多的科室
            if app['isVip'] == 0:
                continue

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
                        # logging.info('@@@@@@@@@@@@@@@@@' + str(testEx_item['ID']) + '.' + cptName + '@@@@@@@@@@@@@@@@@')
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


                        # logging.info(response.text)
                        testEx_info = loads(response.text)
                        # 保存json文件，备查
                        json = open('/Users/chengfei/ksbd_json/' + '_' + app['AppName'] + '_' + app['AppCName'] + app['AppEName'] + '_' + str(app['AppID']) + '_' + str(testEx_item['ID']) + '.json','w')
                        json.write(response.text)
                        json.close()
                        # logging.info(testEx_item)
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
                            test_ex_num = 0
                            for testEx_item in testEx_items['TestItems']:

                                # 公共数据部分
                                testEx_item['StyleID'] = testEx_items['StyleID']
                                testEx_item['Style'] = testEx_items['Style']
                                # testEx_item['Explain'] = testEx_items['Explain']
                                testEx_item['Score'] = testEx_items['Score']
                                testEx_item['Type'] = testEx_items['Type']
                                testEx_item['SubType'] = testEx_items['SubType']
                                testEx_item['province'] = 'JS'
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
                                allType[testEx_items['Type']] = 'test'
                                # ATEST处理方式
                                if testEx_items['Type'] == 'ATEST' or testEx_items['Type'] == 'XTEST':
                                    test_ex_num = test_ex_num + 1
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
                                    # logging.info(testEx_item)
                                    num = num + 1
                                # BTEST题 增加BTestID、BTestItems、FrontTitle
                                elif testEx_items['Type'] == 'BTEST':

                                    # logging.debug("==========BTEST==========")
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    # 增加父ID
                                    testEx_item['Title'] = desUtil.decrypt(ciphertext=testEx_item['Title'])
                                    testEx_item['father_id'] = 0
                                    father_id = str(db_questionItem.insert(testEx_item.copy()))
                                    # bTest_items = testEx_item['BTestItems']

                                    for bTest_item in testEx_item['BTestItems']:
                                        test_ex_num = test_ex_num + 1
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
                                        # 增加父ID
                                        testEx_item['father_id'] = father_id
                                        db_questionItem.insert(testEx_item.copy())
                                        num = num + 1

                                # A3TEST题 增加A3TestID、A3TestItems、FrontTitle
                                elif testEx_items['Type'] == 'A3TEST':
                                    # logging.debug("==========A3TEST==========")
                                    testEx_item['FrontTitle'] = desUtil.decrypt(ciphertext=testEx_item['FrontTitle'])
                                    # 增加父ID
                                    testEx_item['father_id'] = 0
                                    father_id = str(db_questionItem.insert(testEx_item.copy()))
                                    for a3Test_item in testEx_item['A3TestItems']:
                                        test_ex_num = test_ex_num + 1
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
                                        # 增加父ID
                                        testEx_item['father_id'] = father_id
                                        db_questionItem.insert(testEx_item.copy())
                                        # logging.info(testEx_item)
                                        num = num + 1
                                elif testEx_items['Type'] == 'PDTEST' or testEx_items['Type'] == 'TKTEST' or testEx_items['Type'] == 'JDTEST':
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
                                    # 保存判断，简答和填空题
                                    db_questionItem.insert(testEx_item.copy())


                                else:
                                    logging.info('@@@@@@@@@@@@@@@@@'+ '.' + cptName + '-'+ sbjName +'-'+ srcName+'-'+ cptName +'='+str(test_ex_num)+'-'+testEx_items['Type']+'@@@@@@@@@@@@@@@@@')
                        # 休眠时间
                        self.sleepSec = random.randint(5, 13)

                        # logging.warning("休息" + str(self.sleepSec) + "秒继续抓......")
                        time.sleep(self.sleepSec)

            logging.info('num:' + str(num))
            logging.info('num2:' + str(num2))
            logging.info(allType)


        end = time.time()
        print((end - start) / 60)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    def run(self):
        # 循环账号抓取
        for user in apps:
            # 根据账号列表判断是否需要抓取
            if user['user']in userList:
                self.user = userLogin(user['user'])
                self.user.run()
                self.appENames= user['apps']
                self.getQuestionItem()


if __name__ == '__main__':
    questionItem = QuestionItem()
    questionItem.run()

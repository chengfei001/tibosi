from requests import request, post
from json import loads,dumps
from re import findall
import logging
from  pymongo import  MongoClient

from login import userLogin

logging.basicConfig(level=logging.DEBUG)

#mongoDB
client = MongoClient('localhost',27017)
db = client.kaoshibaodian_base
db_PoolItem = db.PoolItem
db_SpecialtyDept = db.SpecialtyDept

'''
各个省份学科科室关系
'''
class SpecialtyDept:
    def __init__(self):
        # 获取菜单  appEName从数据看直接获取
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.user  =userLogin()
        self.user.run()
        # self.AppID = ''
        # self.Province = ''
        # self.SpecialtyName = ''
    def getSpecialtyDept(self):
        #循环省市 目前指定「通用版」，通用版通，北京、江苏、湖北等一级
        for poolItem in db_PoolItem.find({'Province':'通用版'}):
            # AppID = poolItem['AppID']
            Province = poolItem['Province']
            SpecialtyName = poolItem['SpecialtyName']
            logging.info(SpecialtyName)
            # 通过AppEName获取菜单
            response = request(method='get', url=self.chapterMenuX % (poolItem['AppEName']), headers = self.user.headers)
            menuInfo = loads(response.text)
            menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            # 循环菜单 习题集，公共科目层级
            for menu_level2 in menuInfo2['Childs']:
                #循环科室（章节之后一层）
                for menu_level3 in menu_level2['Childs']:
                    specialtyDept = {}
                    specialtyDept['SpecialtyName'] = SpecialtyName
                    specialtyDept['deptName'] = menu_level3['Name']
                    specialtyDept['Province'] = Province
                    # #保存到MongoDB中，注销
                    # db_SpecialtyDept.insert(specialtyDept)
    def run(self):
        self.getSpecialtyDept()






if __name__ == "__main__":
    specialtyDept = SpecialtyDept()
    specialtyDept.run()


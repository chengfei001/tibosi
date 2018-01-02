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



class SpecialtyDept:
    def __init__(self):
        # 获取菜单  appEName从数据看直接获取
        self.chapterMenuX = 'http://gfapi.ksbao.com/api/chapterMenu/getChapterMenuX?clientver=wide.ksbao.com&appEName=%s'
        self.user  =userLogin()
        self.user.run()
        self.AppID = ''
        self.Province = ''
        self.SpecialtyName = ''
    def getSpecialtyDept(self):
        for poolItem in db_PoolItem.find({'Province':'通用版'}):
            self.AppID = poolItem['AppID']
            self.Province = poolItem['Province']
            self.SpecialtyName = poolItem['SpecialtyName']
            response = request(method='get', url=self.chapterMenuX % (poolItem['AppEName']), headers = self.user.headers)
            menuInfo = loads(response.text)
            menuInfo2 = loads(menuInfo['data']['ChapterMenuJson'])
            for menu_level2 in menuInfo2['Childs']:
                # INFO: root:1
                # INFO: root:2
                # INFO: root:3
                # INFO: root:4
                # INFO: root:5
                # INFO: root:6
                # INFO: root:7
                # INFO: root:8
                # INFO: root:10
                # INFO: root:11
                # INFO: root:13
                # INFO: root:14
                # INFO: root:16
                logging.info(menu_level2)
                for menu_level3 in menu_level2['Childs']:
                    logging.info(menu_level3)


                    logging.warning("休息2分钟继续抓......")
    def run(self):
        self.getSpecialtyDept()






if __name__ == "__main__":
    specialtyDept = SpecialtyDept()
    specialtyDept.run()


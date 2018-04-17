from requests import request, post
from json import loads,dumps
from re import findall
import logging
from  pymongo import  MongoClient

from login import userLogin

logging.basicConfig(level=logging.DEBUG)

client = MongoClient('localhost',27017)
db = client.kaoshibaodian_base_new

db_PoolItem = db.PoolItem
db_PoolItemTags = db.PoolItemTags

# 关键字，标签
class PoolItem:
    def __init__(self):
        self.url_pooItem = 'http://gfapi.ksbao.com/api/softMenu/getNew?agentCode=889&clientver=wide.ksbao.com'
        self.user = userLogin('13811378722')
        self.user.run()
        # self.user  =userLogin()
        self.user.run()

    def getPoolItem(self):
        array_poolItems = []
        response = request(method='get', url=self.url_pooItem, headers=self.user.headers)
        poolItem_info = loads(response.text)
        logging.info(poolItem_info)
        logging.info(poolItem_info['data'])
        logging.info(loads(poolItem_info['data'])['Childs'])
        if poolItem_info['msg'] == '查询软件目录成功':
            for items in loads(poolItem_info['data'])['Childs']:
                #住院医师规培结业考核zhuyuanyishi(只需要获取)
                if items['AppEName'] == 'zhuyuanyishi':
                    for items_province in items['Childs']:
                        province = items_province['Name']
                        for items_province_sub in items_province['Childs']:
                            array_poolItem = items_province_sub
                            if findall('\((.*?)\)', items_province_sub['Name']) :
                                items_province_sub['SpecialtyName'] = findall('\((.*?)\)', items_province_sub['Name'])[0]

                            items_province_sub['Province'] = province
                            items_province_sub['AppENamesNum'] = len(items_province_sub['AppENames'])
                            if items_province_sub.get('tags'):
                                if items_province_sub['tags'].split('#'):
                                    for tag in items_province_sub['tags'].split('#'):
                                        d_tag = {'TagName': tag,'app_id':items_province_sub['AppID']}
                                        #暂时注释插入数据库动作
                                        db_PoolItemTags.insert(d_tag)
                            # 单条数据插入，暂时注销，避免插入错误
                            # db_PoolItem.insert(items_province_sub)

    ''' 批量插入，目前数量979，批量插入操作失败                            
                                array_poolItems.append(items_province_sub)
                            db_PoolItem.insert_many(array_poolItems)
    '''


    def run(self):
        self.getPoolItem()

if __name__ == "__main__":
    poolItem = PoolItem()
    poolItem.run()


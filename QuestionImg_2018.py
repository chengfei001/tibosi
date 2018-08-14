from pymongo import MongoClient
from json import loads,dumps
from requests import get
import os

import re

import logging

logging.basicConfig(level=logging.INFO)

client = MongoClient(host={'localhost'}, port=27017)
db = client.kaoshibaodian_base_new_2018
db_question_item = db.QuestionItem



class QuestionImg:
    def __init__(self):
        self.file_path = '/Users/chengfei/YSDQKH_GGWSYS/'
        self.pic_type = 'jpg'
        self.pic_type2 = 'gif'
    def get_question_img(self):
        questin_items = db_question_item.find({'$or': [{'Title': re.compile(self.pic_type)},
                                                       {'FrontTitle': re.compile(self.pic_type)},
                                                       {'SelectedItems.Content': re.compile(self.pic_type)},
                                                       {'Title': re.compile(self.pic_type2)},
                                                       {'FrontTitle': re.compile(self.pic_type2)},
                                                       {'SelectedItems.Content': re.compile(self.pic_type2)}],
                                               'appEName': {'$in': ["ZYYS_ZJZYEBYHK","ZYYS_ZJZYKFK"]}
                                               },
                                              no_cursor_timeout=True)
        # questin_items = db_question_item.find({'$or':[{'Title':re.compile(self.pic_type)},
        #                                               {'FrontTitle':re.compile(self.pic_type)},
        #                                               {'SelectedItems.Content':re.compile(self.pic_type)},
        #                                               {'Title':re.compile(self.pic_type2)},
        #                                               {'FrontTitle':re.compile(self.pic_type2)},
        #                                               {'SelectedItems.Content':re.compile(self.pic_type2)}],
        #                                        'appEName': {'$in': ['ZYYS_YNWK', 'ZYYS_ZJNK']}
        #                                        },
        #                                       no_cursor_timeout=True)
        for question in questin_items:

            pic_path = question['pic_path']
            app_ename = question['appEName']
            # 获取题干中的图片，返回数组
            imgs = re.findall('\[(.*?)\]',question['Title'])
            self.get_img(imgs = imgs, pic_path= pic_path,app_ename = app_ename)
            #检查FrontTitle字段是否存在，存在的话获取FrontTitle中的图片，返回数组
            if question.get('FrontTitle'):
                imgs = re.findall('\[(.*?)\]', question['FrontTitle'])
                self.get_img(imgs=imgs, pic_path=pic_path, app_ename=app_ename)
            # 检查SelectedItems.title字段是否存在，存在的话获取SelectedItems.title中的图片，返回数组
            if question.get('SelectedItems'):
                for selected in question['SelectedItems']:
                    imgs = re.findall('\[(.*?)\]', selected['Content'])
                    self.get_img(imgs=imgs, pic_path=pic_path, app_ename=app_ename)
        questin_items.close()

    def get_img(self,imgs,pic_path,app_ename):
        #存储路径 目录+ppEName
        path = self.file_path+app_ename
        isExists = os.path.exists(path)
        logging.info(isExists)
        if not isExists:
            logging.info(path)
            os.makedirs(path)

        for img in imgs:
            response = get(url=pic_path+img)
            pic = open(path + '/' + img, 'wb')
            pic.write(response.content)
            pic.close()
            logging.info(pic_path+img)

    def run(self):
        self.get_question_img()





if __name__ == '__main__':
    question_img = QuestionImg()
    question_img.run()
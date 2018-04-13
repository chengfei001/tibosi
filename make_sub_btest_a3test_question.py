from pymongo import MongoClient
from pymongo import ASCENDING
import logging


logging.basicConfig(level=logging.INFO)

client = MongoClient(host={'localhost'}, port=27017)
db = client.kaoshibaodian_base

db_question_item = db.QuestionItem


# 生成子题
class Question:

    def make_main_record(self):
        # 获取appEname
        for appEName in db_question_item.distinct('appEName', {'Type': {'$in': ['BTEST', 'A3TEST']}},no_cursor_timeout=True):
            #获取要A3TEST & BTEST
            master_id = '';
            master_all_testid = 0
            for question_item in db_question_item.find({'$and': [{'Type': {'$in': ['BTEST', 'A3TEST']}},{'father_id':{'$exists': False}}, {'appEName': appEName}]}).sort('AllTestID,ChildTableID'):
                # 如果是A3TEST,将ChildTableID和A3TestID相等的表作为主记录，添加father_id 为0，其他相同AllTestID
                if question_item['Type'] == 'BTEST':
                    if question_item['BTestItemID'] == question_item['BTestID'] and question_item.get('father_id') is None:
                        master_id = str(question_item['_id'])
                        master_all_testid = question_item['AllTestID']
                        question_item_sub = question_item.copy()
                        # 删除主键_id,以便插入新纪录
                        del question_item_sub['_id']
                        # 讲主记录的_id作为father_id
                        question_item_sub['father_id'] = master_id
                        # logging.info(question_item_sub)
                        # 插入一条新的子记录
                        db_question_item.insert(question_item_sub)

                        # 新增主记录的father_id 为'0'，0代表 自己
                        question_item['father_id'] = '0'
                        # logging.info(question_item)
                        db_question_item.save(question_item)
                    else:
                        if question_item.get('father_id') is None:
                            # logging.info(str(question_item['AllTestID'])+ '  ddd' + str(master_all_testid))
                            if question_item['AllTestID'] == master_all_testid:
                                question_item['father_id'] = master_id
                                db_question_item.save(question_item)
                                # logging.info("BTEST sub")
                                # logging.info(question_item)
                            else:
                                logging.info("有问题了 BTEST: "+str(question_item['_id']))
                elif question_item['Type'] == 'A3TEST':
                    if question_item['A3TestItemID'] == question_item['A3TestID'] and question_item.get('father_id') is None:
                        master_id = str(question_item['_id'])
                        master_all_testid = question_item['AllTestID']
                        question_item_sub = question_item.copy()
                        # 删除主键_id,以便插入新纪录
                        del question_item_sub['_id']
                        # 讲主记录的_id作为father_id
                        question_item_sub['father_id'] = master_id
                        # logging.info(question_item_sub)
                        # 插入一条新的子记录
                        db_question_item.insert(question_item_sub)
                        # 新增主记录的father_id 为'0'，0代表 自己
                        question_item['father_id'] = '0'
                        # logging.info(question_item)
                        db_question_item.save(question_item)
                    else:
                        if question_item.get('father_id') is None:
                            if question_item['AllTestID'] == master_all_testid:
                                question_item['father_id'] = master_id
                                db_question_item.save(question_item)
                            else:
                                logging.info("有问题了 A3TEST: "+str(question_item['_id']))

        # db_question_item.close()


    def run(self):
        self.make_main_record()

if __name__ == '__main__':
    question = Question()
    question.run()
    # for btest in db_question_item.find({'TYPE': 'BTEST'}):

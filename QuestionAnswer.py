from pymongo import MongoClient
# from json import loads,dumps
import logging
import  types

logging.basicConfig(level = logging.INFO)


client = MongoClient(host={'localhost'}, port=27017)
db = client.kaoshibaodian_base_new

db_questionAnswer = db.QuestionAnswer
db_questionItem = db.QuestionItem

class QuestionAnswer:
    def __init__(self):
        # self.appENames = ["ZYYS_KQHMWK"]
        #self.appENames = ["ZYYS_KQHMWK","ZYYS_FSK","ZYYS_ZYT","ZYYS_ZYEBYHK","ZYYS_KFYX","ZYYS_PFK","ZYYS_QKYX","ZYYS_SJNK","ZYYS_YK","ZYYS_YXYX","ZYYS_GK","ZYYS_HYXK","ZYYS_EK","ZYYS_FCK","ZYYS_NK","ZYYS_WK","ZYYS_EWK","ZYYS_JSK","ZYYS_JZK","ZYYS_MZK","ZYYS_EBYHK","ZYYS_EXJYK","ZYYS_LCBLK","ZYYS_CSYXK","ZYYS_MNWK","ZYYS_XXWK","ZYYS_ZXWK","ZYYS_FSZLK","ZYYS_KQBLK","ZYYS_KQNK","ZYYS_KQQK","ZYYS_KQXFK","ZYYS_KQZJK","ZYYS_TNK","ZYYS_YFYXK","ZYYS_ZJK","ZYYS_ZYEK","ZYYS_ZYFK","ZYYS_ZYGSK","ZYYS_ZYKFK","ZYYS_ZYNK","ZYYS_ZYQK","ZYYS_ZYWK","ZYYS_ZYYK","ZYYS_JSNKYJD"]
        # self.appENames = ["ZYYS_MZK","ZYYS_JSK","ZYYS_EWK","ZYYS_JZK","ZYYS_YNWK","ZYYS_ZJNK","ZYYS_EBYHK", "ZYYS_LCBLK", "ZYYS_EXJYK", "ZYYS_CSYXK","ZYYS_NK", "ZYYS_WK","ZYYS_EK", "ZYYS_FCK","ZYYS_KQHMWK","ZYYS_ZYEBYHK","ZYYS_FSK","ZYYS_ZYT","ZYYS_PFK","ZYYS_QKYX","ZYYS_SJNK","ZYYS_KFYX","ZYYS_GK","ZYYS_YK","ZYYS_YXYX","ZYYS_HYXK","ZYYS_FSZLK","ZYYS_YFYXK","ZYYS_KQQK","ZYYS_KQNK","ZYYS_KQXFK","ZYYS_KQZJK","ZYYS_KQBLK","ZYYS_ZYEK","ZYYS_ZYFK","ZYYS_ZYGSK","ZYYS_ZYKFK","ZYYS_ZYNK","ZYYS_ZYQK","ZYYS_ZYWK","ZYYS_ZYYK","ZYYS_TNK","ZYYS_ZJK","ZYYS_ZXWK", "ZYYS_XXWK", "ZYYS_MNWK","ZYYS_ZJZYEK", "ZYYS_ZJZYFK"]
        # self.appENames = ["ZYYS_ZJZYYK", "ZYYS_ZJZYGSK", "ZYYS_ZJFCK", "ZYYS_ZJZYEBYHK", "ZYYS_ZJZYQK", "ZYYS_ZJZYWK", "ZYYS_ZJZYEK", "ZYYS_ZJZYFK"
        self.appENames = ["ZYYS_ZJFCK","ZYYS_ZJZYEBYHK","ZYYS_ZJZYEK","ZYYS_ZJZYFK"]

    def get_question_answer(self):

        logging.info(self.appENames)
        for question_item in db_questionItem.find({'appEName':{'$in': self.appENames}}):
            # logging.info(question_item)
            question_answer ={}
            question_answer['questionID'] = str(question_item['_id'])

            # 单独处理 「判断、问答、填空」三种类型题 单独处理 TKTEST', 'PDTEST', 'JDTEST'
            if question_item['Type'] == 'TKTEST' or question_item['Type'] == 'PDTEST' or question_item['Type'] == 'JDTEST':
                if question_item.get('Answer') is not None:
                    if isinstance(question_item['Answer'], list):
                        for answer_item in question_item['Answer']:
                            question_answer['Content'] = answer_item
                            db_questionAnswer.insert(question_answer.copy())
                    else:
                        question_answer['Content'] = question_item['Answer']
                        db_questionAnswer.insert(question_answer.copy())
            # ATEST BTEST A3
            elif question_item['Type'] == 'XTEST':
                if question_item.get('SelectedItems') is not None:
                    for answer_item  in question_item['SelectedItems']:
                        if answer_item.get('HasImg'):
                            answer_item['HasImg'] = answer_item['HasImg']
                        else:
                            answer_item['HasImg'] = 0

                        question_answer['ItemName'] = answer_item['ItemName']
                        question_answer['Content'] = answer_item['Content']
                        i = 0
                        while i < len(question_item['Answer']):
                            if answer_item['ItemName'] == question_item['Answer'][i]:
                                IsRight = 1
                                break
                            else:
                                IsRight = 0
                            i += 1
                        question_answer['IsRight'] = IsRight
                        db_questionAnswer.insert(question_answer.copy())
            else:
                if question_item.get('SelectedItems') is not None:
                    for answer_item  in question_item['SelectedItems']:
                        if answer_item.get('HasImg'):
                            answer_item['HasImg'] = answer_item['HasImg']
                        else:
                            answer_item['HasImg'] = 0

                        question_answer['ItemName'] = answer_item['ItemName']
                        question_answer['Content'] = answer_item['Content']
                        i = 0
                        while i < len(question_item['Answer']):
                            if answer_item['ItemName'] == question_item['Answer'][i]:
                                IsRight = 1
                                break
                            else:
                                IsRight = 0
                            i += 1
                        question_answer['IsRight'] = IsRight
                        db_questionAnswer.insert(question_answer.copy())

        # 单独处理 「判断、问答、填空」三种类型题
        # for question_item in db_questionItem.find({'Type': {'$in': ['TKTEST', 'PDTEST', 'JDTEST']}}):
        #     question_answer = {}
        #     question_answer['questionID'] = str(question_item['_id'])
        #     if question_item.get('Answer') is not None:
        #         for answer_item in question_item['Answer']:
        #             question_answer['Content'] = answer_item
        #             # logging.info(question_answer)
        #             db_questionAnswer.insert(question_answer.copy())



    def run(self):
        self.get_question_answer()



if __name__ == '__main__':
    questionitem = QuestionAnswer()
    questionitem.run()

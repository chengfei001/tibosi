from pymongo import MongoClient
# from json import loads,dumps
import logging
import  types

logging.basicConfig(level = logging.INFO)


client = MongoClient(host={'localhost'}, port=27017)
db = client.kaoshibaodian_base_new_2018

db_questionAnswer = db.QuestionAnswer
db_questionItem = db.QuestionItem

class QuestionAnswer:
    def __init__(self):

        self.appENames = ["YSDQKH_GGWSYS"]

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

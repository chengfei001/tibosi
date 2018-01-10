from pymongo import MongoClient
from json import loads,dumps
import logging

logging.basicConfig(level = logging.INFO)


clent = MongoClient(host={'localhost'}, port=27017)
db = clent.kaoshibaodian_base

db_questionAnswer = db.QuestionAnswer
db_questionItem = db.QuestionItem

class QuestionAnswer:
    def __init__(self):
        # self.appENames = "['ZYYS_EK']"
        self.appENames = ["ZYYS_MZK","ZYYS_JSK","ZYYS_EWK","ZYYS_JZK","ZYYS_NK", "ZYYS_WK", "ZYYS_EK", "ZYYS_FCK"]

    def get_question_answer(self):
        logging.info(self.appENames)
        for question_item in db_questionItem.find({'appEName':{'$in': self.appENames}}):
            # logging.info(question_item)
            question_answer ={}
            question_answer['questionID'] = str(question_item['_id'])
            for answer_item  in question_item['SelectedItems']:
                if answer_item.get('HasImg'):
                    answer_item['HasImg'] = answer_item['HasImg']
                else:
                    answer_item['HasImg'] = 0

                question_answer['ItemName'] = answer_item['ItemName']
                question_answer['Content'] = answer_item['Content']
                if answer_item['ItemName'] == question_item['Answer']:
                    IsRight = 1
                else:
                    IsRight = 0
                question_answer['IsRight'] = IsRight
                db_questionAnswer.insert(question_answer.copy())
    def run(self):
        self.get_question_answer()



if __name__ == '__main__':
    questionitem = QuestionAnswer()
    questionitem.run()

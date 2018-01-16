from pymongo import MongoClient
import logging


logging.basicConfig(level=logging.INFO, filemode='ChapterTestEx.log', format='%(asctime)s - %(levelname)s - %(message)s')

# mongoDB
client = MongoClient(host='localhost', port=27017)
db = client.kaoshibaodian_base

db_questionItem = db.QuestionItem



if __name__ == '__main__':
    n =0
    testInfo = {}
    for question2 in db_questionItem.distinct('Title', {'appEName': {'$in': ['ZYYS_JSNKYJD']}}):
        # logging.info(question2)
        testInfo[question2] = 'title'

    logging.info('江苏数据装载完成')
    for question in db_questionItem.distinct('Title',{'appEName':{'$in':['ZYYS_NK']}}):
        if testInfo.get(question) is not None:
            n = n +1
            logging.info(question)
        # for question2 in db_questionItem.distinct('Title', {'appEName': {'$in': ['ZYYS_JSNKYJD']}}):
        #     if question == question2:
        #         n = n +1

    logging.info(str(n))
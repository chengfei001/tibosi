from pymongo import MongoClient
import logging
logging.basicConfig(level=logging.INFO)

client = MongoClient(host={'localhost'},port=27017)

db =client.kaoshibaodian_base

if __name__ == '__main__':
    appENames = '['
    logging.info("strat")
    for appEName in db.QuestionItem.distinct('appEName'):
        appENames = appENames+'\"'+appEName + '\",'

    appENames = appENames +  ']'
    logging.info(appENames)
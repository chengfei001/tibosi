from pymongo import MongoClient
import logging

logging.basicConfig(level=logging.INFO)

client = MongoClient(host='localhost', port=27017)

db = client.kaoshibaodian_base

if __name__ == '__main__':
    dict_test = {'name': 'chengfei', 'age': 39, 'sex': 'male'}
    return_id = db.savereturn.insert(dict_test)
    logging.info("aa"+str(return_id) + str(isinstance(return_id,object))+str(type(return_id)))

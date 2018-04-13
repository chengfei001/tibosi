from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
import re
from pymongo import MongoClient


client = MongoClient(host={'localhost'},port=27017)
db = client.kaoshibaodian_base
"""
des cbc解密密算法
针对考试宝典标题解密

"""

class DESUtil:
    def __init__(self):
        self.iv = "5QTtRO3v"
        self.key = "5QTtRO3v"
    def decrypt(self,ciphertext):
        cipherX = DES.new(self.key, DES.MODE_CBC, self.iv)
        orginalText = cipherX.decrypt(a2b_hex(ciphertext))
        text = orginalText.decode("utf-8")
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)
        text = re.sub('[\01\02\03\04\05\06\07\08]$', '', text)

        #
        return text
if __name__ == '__main__':
    # des = DESUtil()
    # abc  = des.decrypt('107ec9bbeb95f2433a9a2e907dc4d68a6e7b457fe914e345fc0dec81da60fe99b78cc2c0d78c67c9489b96d2437d13dc1df057138a0ae64f5fe94990e812404e48b6a4fdb531d69a2dad21218dfe8720626c7278fc124a38d520525772e60aa8514bcbb8cf40fef50392200f0107bc97a8b2214807bec710fb9edc6ae1dbf8d39e1ae4c8a7fd63b99c23e4fdba2b3d958359201e682ee63f03c9bc514e88eddd4e752725ea5826350262875fb4bfab07d0721dce9110b5b3')
    des = DESUtil()
    abc = des.decrypt('7fcbefbf5734f784b8cbcafb45a2d5f165a406ac8511cb13fa578af178d6678ea8d7b5cddc81cd653d3f6f588d3d781e14143c017c0db07ab3a035092f7d628bc5aa03f5e7dfca4f88982a96a5090dbf0f4ec44e8957035251a817b506a94256c2748dbb886bf193b02a5e1a5c0203544ab842f1a7f1d4f50a4b952689b13c4d')
    # desUtil = DESUtil()
    # for question_item in db.QuestionItem.find({'Type': {'$in': ['JDTEST', 'TKTEST', 'PDTEST']}}):
    #     question_item['Title'] =desUtil.decrypt(question_item['Title'])
    #     print(question_item['Title'])
    #     db.QuestionItem.save(question_item)

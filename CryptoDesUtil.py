from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
import re


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
        return re.sub('[\01\02\03\04\05\06\07\08]', '', orginalText.decode("utf-8"))
if __name__ == '__main__':
    des = DESUtil()
    abc  = des.decrypt('107ec9bbeb95f2433a9a2e907dc4d68a6e7b457fe914e345fc0dec81da60fe99b78cc2c0d78c67c9489b96d2437d13dc1df057138a0ae64f5fe94990e812404e48b6a4fdb531d69a2dad21218dfe8720626c7278fc124a38d520525772e60aa8514bcbb8cf40fef50392200f0107bc97a8b2214807bec710fb9edc6ae1dbf8d39e1ae4c8a7fd63b99c23e4fdba2b3d958359201e682ee63f03c9bc514e88eddd4e752725ea5826350262875fb4bfab07d0721dce9110b5b3')
    print(abc+"bddqb")

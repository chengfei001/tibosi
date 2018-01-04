from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
# import base64


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
        return  orginalText.decode("utf-8")
# coding: utf8
import sys
# from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex

import base64


"""
des cbc加密算法
padding : PKCS5
"""

class DESUtil:

    # __BLOCK_SIZE_8 = BLOCK_SIZE_8 = DES.block_size
    # __IV = "\0\0\0\0\0\0\0\0" # __IV = chr(0)*8

    # @staticmethod
    # def encryt(str, key):
    #     cipher = DES.new(key, DES.MODE_CBC, DESUtil.__IV)
    #     x = DESUtil.__BLOCK_SIZE_8 - (len(str) % DESUtil.__BLOCK_SIZE_8)
    #     if x != 0:
    #         str = str + chr(x)*x
    #     msg = cipher.encrypt(str)
    #     # msg = base64.urlsafe_b64encode(msg).replace('=', '')
    #     msg = base64.b64encode(msg)
    #     return msg

    @staticmethod
    def decrypt(enStr, key):
        # var decrypted = CryptoJS.DES.decrypt({ciphertext: CryptoJS.enc.Hex.parse(message)}, keyHex,{iv: ivHex, mode: CryptoJS.mode.CBC, padding: CryptoJS.pad.Pkcs7});
        # cipher = DES.new(key, DES.MODE_CBC,DESUtil.__IV)
        # # enStr += (len(enStr) % 4)*"="
        # # decryptByts = base64.urlsafe_b64decode(enStr)
        # decryptByts = base64.b64decode(enStr)
        # msg = cipher.decrypt(decryptByts)
        # paddingLen = ord(msg[len(msg)-1])
        # return msg[0:-paddingLen]
        # iv = '\0\0\0\0\0\0\0\0'
        # des = DES.new('12345678',DES.MODE_CBC)
        # # des.IV = iv
        # print(des.decrypt('abcdabcd'))

        # DES.key_size = 64
        # des = DES.new('35515474524f3376514d61596e50616a51716334643765614636424e53326447', DES.MODE_CBC,'12345678')
        #
        # text = 'abcdefgh'
        # cipher_text = des.encrypt(text)
        #
        # print(des.decrypt(cipher_text))
        return  '200'

if __name__ == "__main__":
    # key = "35515474524f3376514d61596e50616a51716334643765614636424e53326447"
    message = "90c907746fca3d269afeb7a5a2e5e871807864be683969263bbaf92a23ad025afb5f80ee4aa6c43bbe2e3a35bd4af029bff9f78e06b335853e9e26d9d0842708f44e8f69f75b2b89716b3ce262858b14"
    key = "5QTtRO3v"
    iv = "5QTtRO3v"
    cipherX = DES.new(key, DES.MODE_CBC, iv)
    y = cipherX.decrypt(a2b_hex(message))

    print(y.decode("utf-8"))

    # res = DESUtil.encryt("21975c41eef511ffad1d4b0fcc7e328edf7a714841a0ecf8ef4ed5b68beaba130b9176b8ce54fee725163b3d8dda4273e0858597f66203ce", key)
    # print(res)
    # print(DESUtil.decrypt('21975c41eef511ffad1d4b0fcc7e328edf7a714841a0ecf8ef4ed5b68beaba130b9176b8ce54fee725163b3d8dda4273e0858597f66203ce', key))
    # print(DES.block_size)
    # DESUtil.decrypt('a','a')


# if __name__ == '__main__':
#     pc = prpcrypt('35515474524f3376514d61596e50616a51716334643765614636424e53326447')  # 初始化密钥
#     # e = pc.encrypt("00000")
#     d = pc.decrypt('21975c41eef511ffad1d4b0fcc7e328edf7a714841a0ecf8ef4ed5b68beaba130b9176b8ce54fee725163b3d8dda4273e0858597f66203ce')
#     # logging.info(e)
#     logging.info(d)
#     # e = pc.encrypt("00000000000000000000000000")
#     # d = pc.decrypt(e)
#     # logging.info(e, d)
# coding: utf8
import sys
# from binascii import b2a_hex, a2b_hex

from Crypto.Cipher import DES
from binascii import b2a_hex, a2b_hex
import base64


"""
des cbc解密密算法

"""

class DESUtil:


    def decrypt(enStr, key,iv):
        cipherX = DES.new(key, DES.MODE_CBC, iv)
        orginalText = cipherX.decrypt(a2b_hex(message))
        return  orginalText.decode("utf-8")

if __name__ == "__main__":
    # key = "35515474524f3376514d61596e50616a51716334643765614636424e53326447"
    message = "90c907746fca3d269afeb7a5a2e5e871807864be683969263bbaf92a23ad025afb5f80ee4aa6c43bbe2e3a35bd4af029bff9f78e06b335853e9e26d9d0842708f44e8f69f75b2b89716b3ce262858b14"
    key = "5QTtRO3v"
    iv = "5QTtRO3v"
    title = DESUtil.decrypt(message,key=key,iv=iv)
    print(title)



#!/usr/bin/env python
# coding: utf-8
# encrypt mode: AES256 CBC

import base64
from Crypto.Cipher import AES
import time
from keys import AES_key, AES_iv


# Encryption key and iv
key = AES_key
iv = AES_iv


class EncryptJSON(object):

    def __init__(self, key=key, iv=iv):
        self.key = key
        self.iv = iv
        self.cipher = AES.new(self.key, AES.MODE_CBC, self.iv)

    def Encrypt(self, mystr):
        self.enstr = self._pad(mystr) 
        self.enret = base64.b64encode(self.cipher.encrypt(self.enstr))
        return self.enret

    def _pad(self, s):
        BS = AES.block_size
        s = s.encode("utf-8")
        self.encrypt_str = s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode("utf-8")
        return self.encrypt_str

    def Decrypt(self, encryptedData):
        self.encryptedData = base64.b64decode(encryptedData)
        ret = self._unpad(self.cipher.decrypt(self.encryptedData))
        self.destr = ret.decode(encoding="utf-8")
        return self.destr

    def _unpad(self, s):
        return s[:-ord(s[len(s)-1:])]
    


if __name__ == '__main__':
    encryptedData = '6xoh9pXuZbCHG8ZgitT6N5PQ1Z+ylNQQ1tzRFYJILEc='
    mystr = '{"hosts":["456","52"]}'
    print(EncryptJSON().Encrypt(mystr))
    print(EncryptJSON().Decrypt(encryptedData))
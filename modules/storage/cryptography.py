# -*- coding: utf-8 -*-
# Copyright 2015 Alex Woroschilow (alex.woroschilow@gmail.com)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
import base64 
import logging
from Crypto.Cipher import AES
from Crypto import Random        

import math


class CryptoAES(object):
    
    block = 16

    def __init__(self, password=None):
        self.password = password.encode('utf-8')

    def encrypt(self, string=None):
        if string is None or not len(string):
            string = ' '
        
        try:
            string = string.encode('utf-8')
            string = string.ljust(self.block * math.ceil(len(string) / self.block))

            iv = Random.new().read(AES.block_size)        
            cipher = AES.new(self.password, AES.MODE_CBC, iv)  # never use ECB in strong systems obviously
            content_binary = cipher.encrypt(string)
            content_bytes = base64.b64encode(iv + content_binary)
            return content_bytes.decode("utf-8")
        except(ValueError)  as ex:
            logger = logging.getLogger('CryptoAES')
            logger.exception(ex, string)
            return string
    
    def decrypt(self, string=None):
        if string is None or not len(string):
            return None
        try:
            content_binary = base64.b64decode(string)
            iv = content_binary[:AES.block_size]
            cipher = AES.new(self.password, AES.MODE_CBC, iv)            
            content_bytes = cipher.decrypt(content_binary[AES.block_size:])
            return content_bytes.decode('utf-8')
        except(ValueError)  as ex:
            logger = logging.getLogger('CryptoAES')
            logger.exception(ex)
            return string


if __name__ == "__main__":
    test = CryptoAES('testtesttesttesttesttesttesttest')
    encoded = test.encrypt('asdfasdfasdf asdf asdf asdf asdf asdf asdf asdf')
    decoded = test.decrypt(encoded)
    print(decoded)


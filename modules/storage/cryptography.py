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
import os
import inject
import base64 
import logging
from Crypto.Cipher import AES
from Crypto import Random        

import math


class CryptoFile(object):
    length = 80

    def __init__(self, path=None):
        self.path = path

    def __write(self, content):
        with open(self.path, 'w+') as stream:
            stream.write(content)
            stream.close()
        return True
    
    def __read(self):
        if os.path.isfile(self.path):
            with open(self.path, 'r') as stream:
                return stream.read()
        return None

    @inject.params(logger='logger')
    def __header_raw(self, logger):
        if not os.path.isfile(self.path):
            return os.path.basename(self.path)
        try:
            content = self.__read()
            if content is None or not len(content):
                return os.path.basename(self.path)

            lines = content.split("\n")
            if lines is None or not len(lines):
                return os.path.basename(self.path)
            
            start = lines.index("===HEADER BEGIN===")
            stop = lines.index("===HEADER END===")
            
            return "".join(lines[start + 1:stop])
        except(ValueError)  as ex:
            logger.debug(ex)
        return os.path.basename(self.path)

    @inject.params(logger='logger')
    def __content_raw(self, logger):
        try:
            content = self.__read()
            if content is None:
                return ""

            lines = content.split("\n")
            if lines is None or not len(lines):
                return ""
            
            start = lines.index("===CONTENT BEGIN===")
            stop = lines.index("===CONTENT END===")
            
            return "".join(lines[start + 1:stop])
        except(ValueError)  as ex:
            logger.debug(ex)
        return ""

    @property
    @inject.params(encryptor='encryptor', logger='logger')
    def name(self, encryptor, logger):
        if not os.path.isfile(self.path):
            return os.path.basename(self.path)
        try:
            content = self.__header_raw()
            if content is None or not len(content):
                return os.path.basename(self.path)
            return encryptor.decrypt(content)
        except(ValueError)  as ex:
            logger.debug(ex)
        return os.path.basename(self.path)

    @property
    @inject.params(encryptor='encryptor', logger='logger')
    def content(self, encryptor, logger):
        try:
            content = self.__content_raw()
            if content is None:
                return ""
            return encryptor.decrypt(content)
        except(ValueError)  as ex:
            logger.debug(ex)
        return ""

    @name.setter
    @inject.params(encryptor='encryptor')
    def name(self, value, encryptor=None):
        header_encrypted = encryptor.encrypt(value)
        header_chunks = [header_encrypted[i:i + self.length] for i in range(0, len(header_encrypted), self.length)]
        header = "===HEADER BEGIN===\n{}\n===HEADER END===\n".format("\n".join(header_chunks))
        
        content_encrypted = self.__content_raw()
        content_chunks = [content_encrypted[i:i + self.length] for i in range(0, len(content_encrypted), self.length)]
        content = "===CONTENT BEGIN===\n{}\n===CONTENT END===\n".format("\n".join(content_chunks))
         
        self.__write("{}{}".format(header, content))
        
    @content.setter
    @inject.params(encryptor='encryptor')
    def content(self, value, encryptor=None):
        header_encrypted = encryptor.encrypt(self.name)
        header_chunks = [header_encrypted[i:i + self.length] for i in range(0, len(header_encrypted), self.length)]
        header = "===HEADER BEGIN===\n{}\n===HEADER END===\n".format("\n".join(header_chunks))
        
        content_encrypted = encryptor.encrypt(value)
        content_chunks = [content_encrypted[i:i + self.length] for i in range(0, len(content_encrypted), self.length)]
        content = "===CONTENT BEGIN===\n{}\n===CONTENT END===\n".format("\n".join(content_chunks))
         
        self.__write("{}{}".format(header, content))

    def clone(self, source):
        source = CryptoFile(source)
        self.name = "{}(clone)".format(source.name)
        self.name.content = source.content


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
            return content_bytes.decode('utf-8').strip()
        except(ValueError)  as ex:
            logger = logging.getLogger('CryptoAES')
            logger.exception(ex)
            return string


if __name__ == "__main__":
    test = CryptoAES('testtesttesttesttesttesttesttest')
    encoded = test.encrypt('asdfasdfasdf asdf asdf asdf asdf asdf asdf asdf')
    decoded = test.decrypt(encoded)
    print(decoded)


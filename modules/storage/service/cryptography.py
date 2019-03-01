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
import secrets
import shutil

from Crypto.Cipher import AES
from Crypto import Random        

import math


def clone(path=None):
    if path is None: return None
    name_old = os.path.basename(path)
    name_new = secrets.token_hex(16)
    while os.path.exists(path.replace(name_old, name_new)):
        name_new = secrets.token_hex(16)
    destination = path.replace(name_old, name_new)
    if os.path.isdir(path): shutil.copytree(path, destination)
    if os.path.isfile(path): shutil.copyfile(path, destination)
    return destination


def rename(path=None, name=None):
    if path is None: return None
    if name is None: return None

    file = path    
    if os.path.isdir(path) and os.path.exists(path):
        file = '{}/.metadata'.format(path)
    try:
        crypto = CryptoFile(file)
        if os.path.isfile(path): crypto.setName(name)
        if os.path.isdir(path): crypto.setContent(name)
        return path
    except(ValueError)  as ex:
        logger = logging.getLogger('cryptography')
        logger.debug(ex, "{}, {}".format(path, name))
    return None


def mkdir(path=None, name=None):
    if path is None: return None
    if name is None: return None

    unique = secrets.token_hex(16)
    while os.path.exists("{}/{}".format(path, unique)):
        unique = secrets.token_hex(16)

    folder = "{}/{}".format(path, unique)
    if os.path.isdir(folder): return folder
    
    os.makedirs(folder)

    try:
        crypto = CryptoFile('{}/.metadata'.format(folder))
        crypto.setName('.metadata')
        crypto.setContent(name)
        return folder
    except(ValueError)  as ex:
        logger = logging.getLogger('cryptography')
        logger.debug(ex, "{}/{}".format(path, name))
    return None


def touch(path=None, name=None):
    if path is None: return None
    if name is None: return None
    
    file = "{}/{}".format(path, name)
    if os.path.isfile(file): return file

    unique = secrets.token_hex(16)
    while os.path.isfile("{}/{}".format(path, unique)):
        unique = secrets.token_hex(16)
        
    file = "{}/{}".format(path, unique)
    if os.path.isfile(file): return file

    try:
        crypto = CryptoFile(file)
        crypto.setName(name)
        
        return file
    except(ValueError)  as ex:
        logger = logging.getLogger('cryptography')
        logger.debug(ex, "{}/{}".format(path, name))
    return None


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
        if not os.path.exists(self.path): return None
        with open(self.path, 'r') as stream:
            result = stream.read()
            stream.close()
            return result

    def __header_raw(self):
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
            logger = logging.getLogger('cryptography')
            logger.debug(ex)
        return os.path.basename(self.path)

    def __content_raw(self):
        try:
            content = self.__read()

            if content is None: return ''

            lines = content.split("\n")
            if lines is None or not len(lines):
                return ""
            
            start = lines.index("===CONTENT BEGIN===")
            stop = lines.index("===CONTENT END===")
            
            return "".join(lines[start + 1:stop])
        except(ValueError)  as ex:
            logger = logging.getLogger('cryptography')
            logger.debug(ex)
        return ""

    @property
    @inject.params(encryptor='encryptor')
    def name(self, encryptor):
        if not os.path.isfile(self.path):
            return os.path.basename(self.path)
        try:
            content = self.__header_raw()
            if content is None or not len(content):
                return os.path.basename(self.path)
            return encryptor.decrypt(content)
        except(ValueError)  as ex:
            logger = logging.getLogger('cryptography')
            logger.debug(ex)
        return os.path.basename(self.path)

    def setName(self, value):
        self.name = value

    def setContent(self, value):
        self.content = value

    @property
    @inject.params(encryptor='encryptor')
    def content(self, encryptor):
        try:
            content = self.__content_raw()
            if content is None: return ''
            return encryptor.decrypt(content)
        except(ValueError)  as ex:
            logger = logging.getLogger('cryptography')
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


if __name__ == "__main__":
    test = CryptoAES('testtesttesttesttesttesttesttest')
    encoded = test.encrypt('asdfasdfasdf asdf asdf asdf asdf asdf asdf asdf')
    decoded = test.decrypt(encoded)
    print(decoded)


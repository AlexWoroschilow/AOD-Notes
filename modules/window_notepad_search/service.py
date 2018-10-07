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

from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import MultifieldParser

from whoosh import index


class Search(object):

    def __init__(self):
        pass

    def initialize(self, destination):
        self.ix = index.create_in(destination, Schema(
            title=TEXT(stored=True),
            path=ID(stored=True),
            content=TEXT(stored=True)
        ))
        return self
        
    def exists(self, destination):
        if os.path.exists(destination):
            return index.exists_in(destination)
        return False

    def previous(self, destination):
        if self.exists(destination):
            self.ix = index.open_dir(destination)
        return self

    def append(self, entity=None):
        self.writer = self.ix.writer()
        self.writer.add_document(title=entity.name, path=entity.path, content=entity.text)
        self.writer.commit()

    def update(self, entity=None):
        self.writer = self.ix.writer()
        self.writer.update_document(title=entity.name, path=entity.path, content=entity.text)
        self.writer.commit()

    def remove(self, entity=None):
        self.writer = self.ix.writer()
        with self.ix.searcher() as searcher:
            for number in searcher.document_numbers(path=entity.path):
                print(number)
                self.writer.delete_document(number)
        self.writer.commit()

    def request(self, string=None):
        with self.ix.searcher() as searcher:
            
            query = MultifieldParser([
                "title", "content"
            ], self.ix.schema).parse(string)
            
            for result in searcher.search(query):
                yield result

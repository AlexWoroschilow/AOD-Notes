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
from whoosh.qparser import QueryParser

from whoosh import index


class Search(object):

    @inject.params(config='config', storage='storage')
    def __init__(self, options, config, storage):

        destination = '%s/index' % os.path.dirname(options.config)
        
        if not os.path.exists(destination):
            os.mkdir(destination)
            
        if index.exists_in(destination):
            self.ix = index.open_dir(destination)
            return None 
        
        self.ix = index.create_in(destination, Schema(
            title=TEXT(stored=True),
            path=ID(stored=True),
            content=TEXT(stored=True)
        ))
        
        self.writer = self.ix.writer()
        destination = config.get('storage.location')
        for entity in storage.entities(destination):
            self.writer.add_document(title=entity.name, path=entity.path, content=entity.text)
        self.writer.commit()
        return None

    def add(self, entity=None):
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
            query = QueryParser('content', self.ix.schema).parse(string)
            for result in searcher.search(query):
                yield result

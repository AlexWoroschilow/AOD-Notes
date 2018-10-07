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

from whoosh.fields import *
from whoosh.qparser import QueryParser

from whoosh.index import create_in
from whoosh.index import open_dir


class Search(object):

    def __init__(self, options):
        
        index = '%s/index' % os.path.dirname(options.config)
        if os.path.exists(index):
            self.ix = open_dir(index)
            return
        
        os.mkdir(index)
        
        self.ix = create_in(index, Schema(
            title=TEXT(stored=True),
            path=ID(stored=True),
            content=TEXT(stored=True)
        ))

    def add(self, entity=None):
        self.writer = self.ix.writer()
        print(entity.path, entity.name)
        self.writer.add_document(title=entity.name, path=entity.path, content=entity.text)
        self.writer.commit()

    def remove(self, entity=None):
        self.writer.commit()

    def request(self, string=None):
        with self.ix.searcher() as searcher:
            query = QueryParser('content', self.ix.schema).parse(string)
            for result in searcher.search(query):
                yield result

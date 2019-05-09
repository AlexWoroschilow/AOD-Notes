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
import re

from html.parser import HTMLParser

from whoosh.fields import Schema, TEXT, ID
from whoosh import qparser
from whoosh import scoring
from whoosh import index


class MLStripper(HTMLParser):

    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs = True
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)

    def stripTags(self, html=None):
        if html is None: return None
        self.feed(html)
        return re.sub(' +', ' ', self.get_data())


class Search(object):

    parser = MLStripper()
    searchResult = None

    def __init__(self):
        pass
    
    def create(self, destination):
        if not os.path.exists(destination):
            os.mkdir(destination)
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

    def append(self, title, path, text):
        content = self.parser.stripTags(u"{}".format(text))
        if content is None or not len(content): return

        self.writer = self.ix.writer()
        self.writer.add_document(title=title, path=path, content=content)
        self.writer.commit()

    def update(self, title, path, text):
        content = self.parser.stripTags(u"{}".format(text))
        if content is None or not len(content):
            return self.remove(path) 

        self.writer = self.ix.writer()
        self.writer.update_document(title=title, path=path, content=content)
        self.writer.commit()

    def remove(self, path=None):
        with self.ix.searcher() as searcher:
            self.writer = self.ix.writer()
            for number in searcher.document_numbers(path=path):
                self.writer.delete_document(number)
            self.writer.commit()

    def search(self, string=None, fields=["title", "content"], minscore=0):
        with self.ix.searcher(weighting=scoring.BM25F) as searcher:
            query = qparser.MultifieldParser(fields, self.ix.schema)
            query.add_plugin(qparser.WhitespacePlugin())
            query.add_plugin(qparser.WildcardPlugin())
            pattern = query.parse(u"*{}*".format(string))
            for result in searcher.search(pattern, limit=None):
                if result.score > minscore: minscore = result.score
                if result.score < minscore: continue  
                yield result


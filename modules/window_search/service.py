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
from html.parser import HTMLParser

from whoosh.fields import Schema, TEXT, ID
from whoosh import qparser

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
        if html is None:
            return ''
        
        self.feed(html)
        return self.get_data()


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
        self.writer = self.ix.writer()
        content = self.parser.stripTags(text)
        self.writer.add_document(title=title, path=path, content=content)
        self.writer.commit()

    def update(self, title, path, text):
        self.writer = self.ix.writer()
        content = self.parser.stripTags(text)
        self.writer.update_document(title=title, path=path, content=content)
        self.writer.commit()

    def remove(self, path=None):
        self.writer = self.ix.writer()
        with self.ix.searcher() as searcher:
            for number in searcher.document_numbers(path=path):
                self.writer.delete_document(number)
        self.writer.commit()

    def search(self, string=None):
        with self.ix.searcher() as searcher:
            
            query = qparser.MultifieldParser([
                "title", "content"
            ], self.ix.schema)
            query.add_plugin(qparser.WildcardPlugin())            
            
            self.searchResult = searcher.search(query.parse(
                "*{}*".format(string)                
            ))
            
            for result in self.searchResult:
                yield result

    def keywords(self, string=None):
        if self.searchResult is None:
            self.search(string)
        
        keys = self.searchResult.key_terms("content", docs=5, numterms=10)
        return [keyword for keyword, score in keys]

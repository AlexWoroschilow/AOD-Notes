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

    def __init__(self, destination=None):
        self.destination = destination
        self.writer = None
        self.ix = None

        self.schema = Schema(
            title=TEXT(stored=True),
            content=TEXT(stored=True),
            path=ID(stored=True)
        )

        if not os.path.exists(self.destination):
            os.mkdir(self.destination)
        if not self.exists(self.destination):
            return self.create(self.destination)
        return self.previous(self.destination)

    def create(self, destination=None):
        if self.schema is None: return None
        if destination is None: return None
        self.ix = index.create_in(destination, self.schema)

    def exists(self, destination=None):
        if destination is None: return False
        if not os.path.exists(destination): return False
        return index.exists_in(destination)

    def previous(self, destination=None):
        if destination is None: return None
        if not self.exists(destination): return None
        self.ix = index.open_dir(destination)
        return None

    def append(self, title, path, text):
        content = self.parser.stripTags(text)
        if content is None or not len(content): return None
        self.writer = self.ix.writer()
        self.writer.add_document(title=title, path=path, content=content)
        self.writer.commit()

    def update(self, title, path, text):
        content = self.parser.stripTags(text)
        if content is None or not len(content): return None
        self.writer = self.ix.writer()
        self.writer.update_document(title=title, path=path, content=content)
        self.writer.commit()

    def remove(self, path=None):
        with self.ix.searcher() as searcher:
            self.writer = self.ix.writer()
            for number in searcher.document_numbers(path=path):
                self.writer.delete_document(number)
            self.writer.commit()

    def search(self, string=None):
        with self.ix.searcher() as searcher:
            query = qparser.MultifieldParser([
                "title", "content"
            ], self.ix.schema)
            query.add_plugin(qparser.WildcardPlugin())
            pattern = query.parse("*{}*".format(string))
            for result in searcher.search(pattern):
                yield result

    def clean(self):
        if self.destination is None: return None
        self.create(self.destination)
        return True

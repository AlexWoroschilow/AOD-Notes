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
import sqlite3

from datetime import datetime
from os.path import expanduser


class Entity(object):
    def __init__(self, index=None, date=None, name=None, text=None):
        """
        
        :param index: 
        :param date: 
        :param name: 
        :param text: 
        """
        self._index = index
        self._date = date
        self._name = name
        self._text = text

    @property
    def index(self):
        """
        
        :return: 
        """
        return self._index

    @property
    def date(self):
        """

        :return: 
        """
        return self._date

    @property
    def name(self):
        """

        :return: 
        """
        return self._name

    @property
    def text(self):
        """

        :return: 
        """
        return self._text


class Folder(Entity):
    def __init__(self, index=None, date=None, name=None, text=None):
        super(Folder, self).__init__(index, date, name, text)


class Note(Entity):
    def __init__(self, index=None, date=None, name=None, text=None):
        super(Note, self).__init__(index, date, name, text)


class SQLiteStorage(object):
    _connection = None

    def __init__(self, database=None):
        """
        
        :param database: 
        """
        database = database.replace('~', expanduser('~'))
        if not os.path.isfile(database):
            self.__init_database(database)
        if self._connection is None:
            self._connection = sqlite3.connect(database, check_same_thread=False)
            self._connection.text_factory = str

    def __init_database(self, database=None):
        """
        
        :param database: 
        :return: 
        """
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute("CREATE TABLE Folder (id INTEGER PRIMARY KEY, date TEXT, name TEXT, description TEXT)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_NAME ON Folder(name)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_DATE ON Folder(date)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_INDEX ON Folder(id)")

        self._connection.execute("CREATE TABLE Note (id INTEGER PRIMARY KEY, date TEXT, name TEXT, text TEXT)")
        self._connection.execute("CREATE INDEX IDX_NOTE_NAME ON Note(name)")
        self._connection.execute("CREATE INDEX IDX_NOTE_DATE ON Note(date)")
        self._connection.execute("CREATE INDEX IDX_NOTE_INDEX ON Note(id)")

    @property
    def folders(self):
        """
        
        :return: 
        """
        query = "SELECT * FROM Folder ORDER BY name ASC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, date, name, description = row
            yield Folder(str(index), str(date), str(name), str(description))

    @folders.setter
    def folders(self, collection):
        """
        
        :param collection: 
        :return: 
        """
        pass

    def addFolder(self, name=None, description=None):
        """

        :param word: 
        :param translation: 
        :return: 
        """
        time = datetime.now()
        fields = (time.strftime("%Y.%m.%d %H:%M:%S"), name, description)
        self._connection.execute("INSERT INTO Folder VALUES (NULL, ?, ?, ?)", fields)
        self._connection.commit()

    def updateFolder(self, index=None, name=None, description=None):
        """

        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        fields = (name, description, index)
        self._connection.execute("UPDATE Folder SET name=?, description=? WHERE id=?", fields)
        self._connection.commit()

    def removeFolder(self, index=None, name=None, text=None):
        """

        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        self._connection.execute("DELETE FROM Folder WHERE id=?", [index])
        self._connection.commit()

    @property
    def notes(self):
        """

        :return: 
        """
        query = "SELECT * FROM Note ORDER BY name ASC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, date, name, text = row
            yield Note(str(index), str(date), str(name), str(text))

    @notes.setter
    def notes(self, collection):
        """

        :param collection: 
        :return: 
        """
        pass

    def addNote(self, name=None, text=None):
        """

        :param word: 
        :param translation: 
        :return: 
        """
        time = datetime.now()
        fields = (time.strftime("%Y.%m.%d %H:%M:%S"), name, text)
        self._connection.execute("INSERT INTO Note VALUES (NULL, ?, ?, ?)", fields)
        self._connection.commit()

    def updateNote(self, index=None, name=None, text=None):
        """

        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        fields = (name, text, index)
        self._connection.execute("UPDATE Note SET name=?, text=? WHERE id=?", fields)
        self._connection.commit()

    def removeNote(self, index=None, name=None, description=None):
        """
        
        :param index: 
        :param date: 
        :param word: 
        :param description: 
        :return: 
        """
        self._connection.execute("DELETE FROM Note WHERE id=?", [index])
        self._connection.commit()

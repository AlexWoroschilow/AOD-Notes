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
        self._index = index
        self._date = date
        self._name = name
        self._text = text

    def __eq__(self, other=None):
        if other is not None:
            return self.index == other.index
        return False

    @property
    def index(self):
        return self._index

    @property
    def date(self):
        return self._date

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value=None):
        self._name = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value


class Folder(Entity):

    def __init__(self, index=None, date=None, name=None, text=None):
        super(Folder, self).__init__(index, date, name, text)


class Note(Entity):

    def __init__(self, index=None, folder=None, date=None, name=None, text=None):
        super(Note, self).__init__(index, date, name, text)
        self._folder = folder

    @property
    def folder(self):
        return self._folder

    @folder.setter
    def folder(self, value):
        self._folder = value


class SQLiteStorage(object):
    _connection = None

    def __init__(self, database=None):
        database = database.replace('~', expanduser('~'))
        if not os.path.isfile(database):
            self.__init_database(database)
        if self._connection is None:
            self._connection = sqlite3.connect(database, check_same_thread=False)
            self._connection.text_factory = str

    def __init_database(self, database=None):
        self._connection = sqlite3.connect(database, check_same_thread=False)
        self._connection.text_factory = str
        self._connection.execute("CREATE TABLE Folder (id INTEGER PRIMARY KEY, date TEXT, name TEXT, text TEXT)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_NAME ON Folder(name)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_DATE ON Folder(date)")
        self._connection.execute("CREATE INDEX IDX_FOLDER_INDEX ON Folder(id)")

        self._connection.execute("CREATE TABLE Note (id INTEGER PRIMARY KEY, folder INTEGER, date TEXT, name TEXT, text TEXT)")
        self._connection.execute("CREATE INDEX IDX_NOTE_FOLDER ON Note(folder)")
        self._connection.execute("CREATE INDEX IDX_NOTE_NAME ON Note(name)")
        self._connection.execute("CREATE INDEX IDX_NOTE_DATE ON Note(date)")
        self._connection.execute("CREATE INDEX IDX_NOTE_INDEX ON Note(id)")

    def getFolder(self, index=None):
        query = "SELECT * FROM Folder WHERE id=?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [index]):
            index, date, name, text = row
            return Folder(index, date, name, text)

    @property
    def folders(self):
        query = "SELECT * FROM Folder ORDER BY name ASC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, date, name, text = row
            yield Folder(str(index), str(date), str(name), str(text))

    def foldersByString(self, string=None):
        query = "SELECT Folder.* FROM Folder " \
                "LEFT JOIN Note ON Note.folder = Folder.id " \
                "WHERE Note.name LIKE ? OR Note.text LIKE ? " \
                "GROUP BY Folder.id " \
                "ORDER BY Folder.name ASC "

        cursor = self._connection.cursor()
        for row in cursor.execute(query, ["%%%s%%" % string, "%%%s%%" % string]):
            index, date, name, text = row
            yield Folder(str(index), str(date), str(name), str(text))

    @folders.setter
    def folders(self, collection):
        pass

    def addFolder(self, name=None, text=None):
        time = datetime.now()
        fields = (time.strftime("%Y.%m.%d %H:%M:%S"), name, text)
        self._connection.execute("INSERT INTO Folder VALUES (NULL, ?, ?, ?)", fields)
        self._connection.commit()

        cursor = self._connection.cursor()
        for row in cursor.execute("SELECT last_insert_rowid()"):
            index, = row
            return self.getFolder(index)

    def updateFolder(self, index=None, name=None, text=None):
        fields = (name, text, index)
        self._connection.execute("UPDATE Folder SET name=?, text=? WHERE id=?", fields)
        self._connection.commit()

    def removeFolder(self, index=None, name=None, text=None):
        for note in self.notesByFolderIndex(index):
            self.updateNoteFolder(note.index, None)
        self._connection.execute("DELETE FROM Folder WHERE id=?", [index])
        self._connection.commit()

    @property
    def notes(self):
        query = "SELECT * FROM Note ORDER BY name ASC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            index, folder, date, name, text = row
            yield Note(index, folder, date, name, text)

    def notesByFolder(self, folder=None, search=None):
        if folder is None and search is None:
            return None
        if search is None or not len(search):
            return self.notesByFolderIndex(folder.index)
        return self.notesByFolderIndexAndString(folder.index, search)

    def notesByFolderIndex(self, folder=None):
        query = "SELECT * FROM Note WHERE folder=? OR folder IS NULL ORDER BY name ASC"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [folder]):
            index, folder, date, name, text = row
            yield Note(index, folder, date, name, text)

    def notesByFolderIndexAndString(self, folder=None, string=None):
        query = "SELECT * FROM Note " \
                "WHERE (folder=? OR folder IS NULL) " \
                "AND (Note.name LIKE ? OR Note.text LIKE ?) " \
                "ORDER BY name ASC"

        cursor = self._connection.cursor()
        for row in cursor.execute(query, [folder, "%%%s%%" % string, "%%%s%%" % string]):
            index, folder, date, name, text = row
            yield Note(index, folder, date, name, text)

    @property
    def notesCount(self):
        query = "SELECT COUNT(*) as count FROM Note"
        cursor = self._connection.cursor()
        for row in cursor.execute(query):
            count, = row
            return count

    @notes.setter
    def notes(self, collection):
        pass

    def getNote(self, index=None):
        query = "SELECT * FROM Note WHERE id=?"
        cursor = self._connection.cursor()
        for row in cursor.execute(query, [index]):
            index, folder, date, name, text = row
            return Note(str(index), folder, str(date), str(name), str(text))

    def addNote(self, name=None, text=None, folder=None):
        time = datetime.now()
        fields = (folder, time.strftime("%Y.%m.%d %H:%M:%S"), name, text)
        self._connection.execute("INSERT INTO Note VALUES (NULL, ?, ?, ?, ?)", fields)
        self._connection.commit()

        cursor = self._connection.cursor()
        for row in cursor.execute("SELECT last_insert_rowid()"):
            index, = row
            return self.getNote(index)

    def updateNote(self, index=None, name=None, text=None):
        fields = (name, text, index)
        self._connection.execute("UPDATE Note SET name=?, text=? WHERE id=?", fields)
        self._connection.commit()

    def updateNoteFolder(self, index=None, folderId=None):
        fields = (folderId, index)
        self._connection.execute("UPDATE Note SET folder=? WHERE id=?", fields)
        self._connection.commit()

    def removeNote(self, index=None, name=None, text=None):
        self._connection.execute("DELETE FROM Note WHERE id=?", [index])
        self._connection.commit()

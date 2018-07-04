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
import json
import base64

from sqlalchemy import Column 
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import relationship
from sqlalchemy import or_

Base = declarative_base()


class Folder(Base):
    __tablename__ = 'Folder'
    id = Column(Integer, primary_key=True, autoincrement=True)
    total = Column(Integer)
    name = Column(String)
    createdAt = Column(DateTime)

    notes = relationship("Note", backref="Folder")

    def __eq__(self, entity):
        if entity is None:
            return False
        return self.id == entity.id
    
    def __ne__(self, entity):
        if entity is None:
            return True
        return self.id != entity.id


class Note(Base):
    __tablename__ = 'Note'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    createdAt = Column(DateTime)
    text = Column(String)
    description = Column(String)
    tags = Column(String)
    folderId = Column(Integer, ForeignKey('Folder.id'))
    
    folder = relationship("Folder", backref="Note")

    def __eq__(self, entity=None):
        if entity is None:
            return False
        return self.id == entity.id
    
    def __ne__(self, entity):
        if entity is None:
            return True
        return self.id != entity.id
    
    def toJson(self):
        return json.dumps({
            'name': self.name,
            'description': self.description,
            'text': self.text,
        })

class SQLAlechemyStorage(object):
    _engine = None
    _session = None

    def __init__(self, database=None):
        self._engine = create_engine('sqlite:///%s' % (
            database
        ), convert_unicode=True)

        session = self._session_create(self._engine)
        Base.query = session.query_property()
        Base.metadata.create_all(bind=self._engine)
        session.commit()

    def _session_create(self, engine):
        if self._session is not None:
            return self._session
        self._session = scoped_session(sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        ))
        return self._session

    def create(self, entity=None):
        session = self._session_create(self._engine)
        session.add(entity)
        session.commit()
        session.flush()
        session.refresh(entity)
        return entity

    def update(self, entity=None):
        session = self._session_create(self._engine)
        session.commit()
        session.flush()

    def delete(self, entity=None):
        session = self._session_create(self._engine)
        session.delete(entity)
        session.commit()

    def folders(self, string=None):
        session = self._session_create(self._engine)

        query = session.query(Folder)
        if string is not None:
            return query.filter(
                Folder.name.like('%%%s%%' % string)
            ).order_by(Folder.name.asc()).all()
        
        return query.order_by(Folder.name.asc()).all()

    def notes(self, folder=None, string=None):
        
        session = self._session_create(self._engine)

        query = session.query(Note)
        
        if folder is not None and string is None:
            return query.filter(Note.folder == folder).all()

        if string is not None and folder is None:
            return query.filter(or_(
                Note.name.like('%%%s%%' % string),
                Note.text.like('%%%s%%' % string)
            )).order_by(Note.name.asc()).all()

        if folder is not None and string is not None:
            return query.filter(
                Note.folder == folder,
                or_(
                    Note.name.like('%%%s%%' % string),
                    Note.text.like('%%%s%%' % string)
                )
            ).order_by(Note.name.asc()).all()
        
        return query.all()

    @property
    def notesCount(self):
        return 10


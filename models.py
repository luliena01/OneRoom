# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, BigInteger
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()


class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True)
    name = Column(String(64), unique=True)
    default = Column(Boolean, default=False, index=True)
    permissions = Column(Integer)
    # users = relationship('User', backref='role', lazy='dynamic')


class Room(Base):
    __tablename__ = 'rooms'
    room = Column(Integer, primary_key=True)
    is_living = Column(Boolean, default=False)
    # tanent = db.relationship('User', backref='room', lazy='dynamic')


class User(Base):
    __tablename__ = 'users'

    email = Column(String(64), primary_key=True, index=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    user_name = Column(String(64), index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))           # ForeignKey( 'table name.column name')
    location = Column(String(64), ForeignKey('rooms.room'))
    phone = Column(String(64))
    member_since = Column(DateTime(), default=datetime.utcnow)
    last_seen = Column(DateTime(), default=datetime.utcnow)

    role = relationship("Role")
    room = relationship("Room")


class Notice(Base):
    __tablename__ = 'notices'

    index = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(Text)
    counter = Column(Integer, default=0)
    register_date = Column(DateTime(), default=datetime.utcnow)
    author_id = Column(Text, ForeignKey('users.email'))

    user = relationship("User")


class Shop(Base):
    __tablename__ = 'products'

    index = Column(Integer, primary_key=True)
    title = Column(String(80))
    title_img = Column(String(100))
    title_info = Column(String(80))
    content = Column(Text)
    counter = Column(Integer, default=0)
    register_date = Column(BigInteger, default=0)
    author_id = Column(Text, ForeignKey('users.email'))

    user = relationship("User")


import json
from sqlalchemy.ext.declarative import DeclarativeMeta
class AlchemyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                try:
                    json.dumps(data) # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields

        return json.JSONEncoder.default(self, obj)
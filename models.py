# from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, Text, BigInteger, Enum as Db_Enumn
# from sqlalchemy.types import Enum as Db_Enumn
from sqlalchemy.orm import relationship
from datetime import datetime
from enum import Enum

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
    room = Column(String(10), primary_key=True)
    is_living = Column(Boolean, default=False)

    user = relationship("User")
    # tanent = db.relationship('User', backref='room', lazy='dynamic')


class User(Base):
    __tablename__ = 'users'

    code = Column(String(100), primary_key=True)
    email = Column(String(100), index=True)
    password_hash = Column(String(128))
    confirmed = Column(Boolean, default=False)
    user_name = Column(String(64), index=True)
    role_id = Column(Integer, ForeignKey('roles.id'))           # ForeignKey( 'table name.column name')
    room = Column(String(64), ForeignKey('rooms.room'))
    phone = Column(String(64))
    member_since = Column(DateTime(), default=datetime.utcnow)
    last_seen = Column(DateTime(), default=datetime.utcnow)

    role = relationship("Role")
    room_info = relationship("Room")


class Confirm_type(Enum):
    CONFIRM_REGISTER = 'CONFIRM_REGISTER',
    RESET_PASSWORD = 'RESET_PASSWORD'


class Confirm(Base):
    __tablename__ = 'confirm'

    url = Column(String(256), primary_key=True)
    email = Column(String(100), ForeignKey('users.email'))
    # type = Column(Db_Enumn(Confirm_type))
    type = Column(String(100))

    user = relationship("User")


class Notice(Base):
    __tablename__ = 'notices'

    index = Column(Integer, primary_key=True)
    title = Column(String(80))
    content = Column(Text)
    counter = Column(Integer, default=0)
    register_date = Column(DateTime(), default=datetime.utcnow)
    author_id = Column(String(100), ForeignKey('users.code'))

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
    author_id = Column(String(100), ForeignKey('users.code'))

    user = relationship("User")


class Bill(Base):
    __tablename__ = 'bill'

    target_date = Column(DateTime(), default=datetime.utcnow, primary_key=True)
    room = Column(String(64), ForeignKey('rooms.room'), primary_key=True)
    author_id = Column(String(100))
    electric_usage = Column(Integer, default=0)
    electric_amount = Column(Integer, default=0)
    gas_usage = Column(Integer, default=0)
    gas_amount = Column(Integer, default=0)
    description = Column(String(200))

    room_info = relationship("Room")


# import json
# from sqlalchemy.ext.declarative import DeclarativeMeta
# class AlchemyEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 try:
#                     json.dumps(data) # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields
#
#         return json.JSONEncoder.default(self, obj)
import uuid
import hashlib
import datetime

import transaction

from sqlalchemy import (
    Column,
    Index,
    ForeignKey,
    Integer,
    Text,
    DateTime,
    Boolean,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(
    sessionmaker(extension=ZopeTransactionExtension(),
    expire_on_commit=False,
))
Base = declarative_base()


#class MyModel(Base):
#    __tablename__ = 'models'
#    id = Column(Integer, primary_key=True)
#    name = Column(Text)
#    value = Column(Integer)
#
#Index('my_index', MyModel.name, unique=True, mysql_length=255)

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(Text)
    passhash = Column(Text)
    salt = Column(Text)
    name = Column(Text)
    token = Column(Text)
    token_expire_datetime = Column(DateTime)

    @classmethod
    def create_user(cls, session, username, password, name):
        with transaction.manager:
            salt = str(uuid.uuid4())
            password = "{0}{1}".format(password,salt)
            passhash = str(hashlib.sha256(password).hexdigest())
            user = cls(
                username = username,
                passhash = passhash,
                salt = salt,
                name = name,
            )
            session.add(user)
            transaction.commit()
        return user

    @classmethod
    def get_user_from_id(cls, session, id):
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.id == id,
            ).first()
        return user

    @classmethod
    def get_user_from_token(cls, session, token):
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.token == token
            ).first()
        return user

    @classmethod
    def login_user(cls, session, username, password):
        success = False
        user = None
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.username == username,
            ).first()
            passhash = str(hashlib.sha256(
                "{0}{1}".format(password,user.salt),
            ).hexdigest())
            if user.passhash == passhash:
                token = str(uuid.uuid4())
                user.token = token
                user.token_expire_datetime = datetime.datetime.now() + \
                    datetime.timedelta(hours=24)
                session.add(user)
                transaction.commit()
                success = True
        return success,user

    @classmethod
    def validate_token(cls, session, token):
        valid = False
        with transaction.manager:
            user = session.query(
                Users,
            ).filter(
                Users.token == token,
            ).first()
            if user != None and \
                    user.token_expire_datetime > datetime.datetime.now():
                valid = True
        return valid

    @classmethod
    def get_users(cls, session, token):
        users = None
        with transaction.manager:
            if Users.validate_token(session, token) == True:
                users = session.query(
                    Users.id,
                    Users.name,
                ).all()
        return users

class Tasks(Base):

    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey('users.id'))
    owner_id = Column(Integer, ForeignKey('users.id'))
    title = Column(Text)
    content = Column(Text)
    due_datetime = Column(DateTime)
    completed = Column(Boolean)
    notes = Column(Text)

    @classmethod
    def get_tasks(cls, session, token):
        tasks = None
        with transaction.manager:
            if Users.validate_token(session, token) == True:
                user = Users.get_user_from_token(session, token)
                tasks = session.query(
                    Tasks.id,
                    Tasks.creator_id,
                    Tasks.owner_id,
                    Tasks.title,
                    Tasks.content,
                    Tasks.due_datetime,
                    Tasks.completed,
                    Tasks.notes,
                    Users.name,
                ).join(
                    Users,Tasks.creator_id == Users.id,
                ).filter(
                    Tasks.owner_id == user.id,
                ).all()
        return tasks

    @classmethod
    def get_created_tasks(cls, session, token):
        tasks = None
        with transaction.manager:
            if Users.validate_token(session, token) == True:
                user = Users.get_user_from_token(session, token)
                tasks = session.query(
                    Tasks.id,
                    Tasks.creator_id,
                    Tasks.owner_id,
                    Tasks.title,
                    Tasks.content,
                    Tasks.due_datetime,
                    Tasks.completed,
                    Tasks.notes,
                    Users.name,
                ).join(
                    Users,Tasks.creator_id == Users.id,
                ).filter(
                    Tasks.creator_id == user.id,
                ).all()
        return tasks

    @classmethod
    def create_task(cls, session, owner_id, token, title, content, due_datetime):
        task = None
        with transaction.manager:
            if Users.validate_token(session, token) == True:
                creator = Users.get_user_from_token(session, token)
                task = cls(
                    creator_id = creator.id,
                    owner_id = owner_id,
                    title = title,
                    content = content,
                    due_datetime = due_datetime,
                    completed = False,
                    notes = '',
                )
                session.add(task)
                transaction.commit()
        return task


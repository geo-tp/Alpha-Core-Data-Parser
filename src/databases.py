from enum import Enum
import mysql.connector
from mysql.connector import errorcode
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

class MysqlDatabase:

    def __init__(
        self, user="root", 
        password="pwd", 
        host="localhost", 
        database_name="alpha_world"):

        self.user = user
        self.password = password
        self.host = host
        self.database_name = database_name
        self.database_session = None

    def connect(self):  
        db_engine = create_engine(f'mysql+pymysql://{self.user}:{self.password}@{self.host}/{self.database_name}?charset=utf8mb4',
                                    pool_pre_ping=True)
        self.database_session = SessionHolder = scoped_session(sessionmaker(bind=db_engine, autoflush=True))

    def close(self):
        self.database_session.close()

    def get_all(self, model):
        return self.database_session.query(model).all()

    def get_by_entry(self, model, entry):
        return self.database_session.query(model).filter_by(entry=entry).first()

    def get_by_name(self, model, name):
        return self.database_session.query(model).filter_by(name=name).first()

    def get_by_title(self, model, title):
        return self.database_session.query(model).filter_by(Title=title).first()

    def has_multiple_entry(self, model, name):
        results = [r for r in self.database_session.query(model).filter_by(Title=name)]
        
        if len(results) > 1:
            return True

        return False
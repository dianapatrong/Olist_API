from flask import Flask
import config as conf
from flask import jsonify
from sqlalchemy import create_engine

app = Flask(__name__)


class DBConnection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(DBConnection)
        return cls._instance

    def __init__(self):
        self.conn = self.create_connection()

    def create_connection(self):
        try:
            engine = create_engine(
                f"mysql://{conf.db_username}:{conf.db_pwd}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4")
            return engine.connect()
        except Exception as e:
            print(e)

    def query(self, query):
        response = None
        try:
            rows = self.conn.execute(query)
            response = jsonify([dict(r) for r in rows])
            response.status_code = 200
        except Exception as e:
            print(e)
        return response

    def close_connection(self):
        self.conn = self.conn.close()
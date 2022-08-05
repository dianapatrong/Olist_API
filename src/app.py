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
        self.conn = None

    def create_connection(self):
        if not self.conn:
            try:
                engine = create_engine(
                    f"mysql://{conf.db_username}:{conf.db_pwd}@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4")
                self.conn = engine.connect()
            except Exception as e:
                print(e)

    def query(self, query, metadata=None):
        response = {}
        self.create_connection()
        try:
            rows = self.conn.execute(query)
            rows = [dict(r) for r in rows]
            response["data"] = rows
            if metadata:
                response["metadata"] = metadata
            response = jsonify(response)
            response.status_code = 200
        except Exception as e:
            print(e)
        finally:
            self.close_connection()
        return response

    def close_connection(self):
        if self.conn:
            try:
                self.conn.close()
                self.conn = None
            except Exception as e:
                print(f"There was an issue while closing the connection: {e}")
    def build_response(self):
        pass
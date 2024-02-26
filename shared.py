from queue import Queue

from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from models.task import Task
from config import config


app = Flask(__name__)
db = SQLAlchemy()
auth = HTTPBasicAuth()

task_queue: Queue[Task] = Queue()


@auth.verify_password
def verify_password(username, password):
    if username == config["Credentials"]["Username"] and password == config["Credentials"]["Password"]:
        return True
    return False

import bottle
from bottle import response
from truckpad.bottle.cors import CorsPlugin, enable_cors

import json
import sqlite3
import uuid
import datetime
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


app = bottle.Bottle()

DB_PATH = "sqlite:///user.sqlite3"
Base = declarative_base()

class User(Base):
   
    __tablename__ = 'user'
    uid = sa.Column(sa.INTEGER, primary_key=True)
    description = sa.Column(sa.TEXT)
    is_completed = sa.Column(sa.BOOLEAN)

def connect_db():
    engine = sa.create_engine(DB_PATH)
    Base.metadata.create_all(engine)
    session = sessionmaker(engine)
    return session()

    
def main():
    session = connect_db()
    query = session.query(User)
    for instance in query:
        my_tasks = instance.description
    return my_tasks


class TodoItem:
    def __init__(self, description, unique_id):
        self.description = description
        self.is_completed = False
        self.uid = unique_id

    def __str__(self):
        return self.description.lower()

    def to_dict(self):
        return {
            "description": self.description,
            "is_completed": self.is_completed,
            "uid": self.uid
        }

tasks_db = {
    uid: TodoItem(desc, uid)
    for uid, desc in enumerate(
        start=1,
        iterable=[
        main()
        ],
    )
}

@enable_cors
@app.route("/api/tasks/")
def index():
    tasks = [task.to_dict() for task in tasks_db.values()]
    return {"tasks": tasks}

@enable_cors
@app.route("/api/tasks/", method=["GET", "POST", "OPTIONS"])
def add_task():
    response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.140:8080/fetch'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'
    if bottle.request.method == 'GET':
        tasks = [task.to_dict() for task in tasks_db.values()]
        return {"tasks": tasks}
    elif bottle.request.method == "POST":
        desc = bottle.request.json['description']
        is_completed = bottle.request.json.get('is_completed', False)
        if len(desc) > 0:
            new_uid = max(tasks_db.keys()) + 1
            t = TodoItem(desc, new_uid)
            t.is_completed = is_completed
            tasks_db[new_uid] = t
        user = User(
        description=desc,
        is_completed=is_completed,
    )
        session = connect_db()
        # просим пользователя выбрать режим
        # запрашиваем данные пользоватлея
        # добавляем нового пользователя в сессию
        session.add(user)
        # обновляем время последнего визита для этого пользователя
        # сохраняем все изменения, накопленные в сессии
        session.commit()
        print("Спасибо, данные сохранены!")
        return "OK"

@enable_cors
@app.route("/api/tasks/<uid:int>", method=["GET", "PUT", "DELETE"])
def show_or_modify_task(uid):
    if bottle.request.method == "GET":
        return tasks_db[uid].to_dict()
    elif bottle.request.method == "PUT":
        if "description" in bottle.request.json:
            tasks_db[uid].description = bottle.request.json['description']
        if "is_completed" in bottle.request.json:
            tasks_db[uid].is_completed = bottle.request.json['is_completed']
        return f"Modified task {uid}"
    elif bottle.request.method == "DELETE":
        tasks_db.pop(uid)
        return f"Deleted task {uid}"                                                                        

@app.hook('after_request')
def enable_cors():
    response.headers['Access-Control-Allow-Origin'] = 'http://192.168.1.140:8080'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

app.install(CorsPlugin(origins=['http://192.168.1.140:8080']))




if __name__ == "__main__":
    bottle.run(app, host="192.168.1.140", port=5000)
    main()
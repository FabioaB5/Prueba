from flask_pymongo import flask_pymongo
import flask 

app = flask.Flask(__name__)
mongodb_client = PyMongo(app, uri="mongodb://localhost:27017/todo_db")
db = mongodb_client.db

@app.route("/add_one")
def add_one():
    db.todos.insert_one({'title': "todo title", 'body': "todo body"})
    return flask.jsonify(message="success")
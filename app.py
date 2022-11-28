from flask import Flask 
from pymongo import MongoClient
import json 
import certifi

app = Flask(__name__)

@app.route('/')
def inicio():
    return "Hola Prueba"

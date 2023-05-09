from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv() 
APP_SECRET = os.environ.get("APP_SECRET")
DATABASE_URI = os.environ.get("DATABASE_URI")
app = Flask(__name__)
app.config["SECRET_KEY"] = APP_SECRET
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
print(os.environ.get("DATABASE_URI"))
db = SQLAlchemy()
db.init_app(app)
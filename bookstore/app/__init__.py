from flask import Flask
from flask_admin import Admin
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = 'KDSFJIUDN*&$#@#VIJSDWIRUGHIURWG%$KSNFIJ'
app.config["SQLALCHEMY_DATABASE_URI"] ="mysql+pymysql://root:%s@localhost/storebook?charset=utf8mb4" % quote('Abc123')
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["PAGE_SIZE"] = 20

db = SQLAlchemy(app)

cloudinary.config(cloud_name='dauhkaecb',api_key='848373387842926',api_secret='fdfMgzXtAQNCVPjIryuihRtjVBM')

login = LoginManager(app)




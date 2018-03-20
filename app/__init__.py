# coding:utf8

from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1/wechat"  # 替换pymysql为mysqlconnector,解决1366报错
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SECRET_KEY"] = '6ea7eb99cc4a47e4a0c9d912633ceaf1'
app.config["UP_DIR"] = os.path.join(os.path.abspath(os.path.dirname(__file__)), "static/uploads/")

#微信借口设置
app.config["TOKEN"] = "malloc"
app.config["AES_KEY"] = "设置AES_KEY"
app.config["APPID"] = "设置微信APPID"
app.debug = True
db = SQLAlchemy(app)

from app.api import api as api_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(api_blueprint, url_prefix='/api')
app.register_blueprint(admin_blueprint, url_prefix='/admin')

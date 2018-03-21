# coding:utf8


# 创建数据库
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:root@127.0.0.1/wechat"  # 替换pymysql为mysqlconnector,解决1366报错
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
db = SQLAlchemy(app)


# 管理员
class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    oplogs = db.relationship("Oplog", backref='admin')
    adminlogs = db.relationship("Adminlog", backref='admin')

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


# 视频数据
class Video(db.Model):
    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    url_bt = db.Column(db.String(100))
    url_baiduyun = db.Column(db.String(100))
    logo = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    release_time = db.Column(db.String(10))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return "<video %r>" % self.title


# 登录日志
class Adminlog(db.Model):
    __tablename__ = "adminlog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 关联admin外键
    ip = db.Column(db.String(100))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 登录时间

    def __repr__(self):
        return "<adminlog %r>" % self.id


# 后台操作日志
class Oplog(db.Model):
    __tablename__ = "oplog"
    id = db.Column(db.Integer, primary_key=True)
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"))  # 关联admin外键
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))  # 操作原因
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())  # 登录时间

    def __repr__(self):
        return "<oplog %r>" % self.id


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)
    movies = db.relationship("Video", backref='tag')  # 电影外键

    def __repr__(self):
        return "<Tag %r>" % self.name


if __name__ == "__main__":
    db.create_all()

    from werkzeug.security import generate_password_hash

    admin = Admin(
        name="orange",
        pwd=generate_password_hash("orange"),
    )
    tag = Tag(
        name="科幻"
    )
    tag2 = Tag(
        name="喜剧"
    )
    db.session.add(admin)
    db.session.add(tag)
    db.session.add(tag2)
    db.session.commit()


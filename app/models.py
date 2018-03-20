# coding:utf8

from app import db
from datetime import datetime


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
    __tablename__ = "vedio"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), unique=True)
    url_bt = db.Column(db.String(100))
    url_baiduyun = db.Column(db.String(100))
    logo = db.Column(db.String(255), unique=True)
    release_time = db.Column(db.String(10))
    addtime = db.Column(db.DateTime, index=True, default=datetime.now())
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))

    def __repr__(self):
        return "<vedio %r>" % self.title


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

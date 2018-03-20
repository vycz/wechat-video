from . import admin
from flask import render_template, redirect, url_for, flash, session, request
from app.admin.forms import VideoForm, LoginForm
from app.models import Admin, Video, Tag
from app import db, app
import os
import uuid
from datetime import datetime
from functools import wraps
from werkzeug.utils import secure_filename


def admin_login_req(f):
    @wraps(f)
    def decorate_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return f(*args, **kwargs)

    return decorate_function


@admin.route("/")
@admin_login_req
def index():
    return render_template("admin/index.html")


@admin.route("/login/", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data["username"]).first()
        if not admin.check_pwd(data["pwd"]):
            flash("密码错误", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data["username"]
        session["admin_id"] = admin.id
        return redirect(request.args.get("next") or url_for("admin.index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
def logout():
    session.pop("admin", None)
    session.pop("admin_id", None)
    return redirect(url_for("admin.login"))


@admin.route("/video/add", methods=["GET", "POST"])
@admin_login_req
def video_add():
    form = VideoForm()
    if form.validate_on_submit():
        data = form.data
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], 775)
        file_logo = secure_filename(form.logo.data)
        if file_logo != "":
            form.logo.data.save(app.config["UP_DIR"] + file_logo)
        video = Video(
            title=data["title"],
            url_baiduyun=data["baiduyun"] or "",
            url_bt=data["bt"] or "",
            logo=file_logo,
            release_time=data['release_time'],
            tag_id=int(data['tag']),
        )
        db.session.add(video)
        db.session.commit()
        flash("添加视频成功", "ok")
        return redirect(url_for('admin.video_add'))
    return render_template("admin/video_add.html", form=form)


@admin.route("/video/list/<int:page>/")
@admin_login_req
def video_list(page=None):
    if page is None:
        page = 1
    page_data = Video.query.join(Tag).filter(
        Tag.id == Video.tag_id
    ).order_by(
        Video.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template("admin/video_list.html",
                           page_data=page_data, )


@admin.route("/video/search/<int:page>/")
@admin_login_req
def video_search(page=None):
    if page is None:
        page = 1
    key = request.args.get("key", "")
    page_data = Video.query.join(Tag).filter(
        Video.title.ilike("%" + key + "%")
    ).order_by(
        Video.addtime.desc()
    ).paginate(page=page, per_page=20)
    return render_template("admin/video_search.html",
                           key=key,
                           page_data=page_data)


@admin.route("/video/edit/<int:id>/", methods=["GET", "POST"])
@admin_login_req
def video_edit(id=None):
    form = VideoForm()
    video = Video.query.get_or_404(int(id))
    form.logo.validators = []
    if form.validate_on_submit():
        data = form.data
        video_count = Video.query.filter_by(title=data["title"]).count
        if video_count == 1 and video.title != data["title"]:
            flash("片名重复", "err")
            return redirect(url_for("admin.video_edit", id=id))

        if form.logo.data != "":
            file_logo = secure_filename(form.data.filename)
            video.logo = file_logo
            form.logo.data.save(app.config["UP_DIR"] + video.logo)

        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        video.title = data["title"]
        video.tag_id = data["tag"]
        video.release_time = data["release_time"]
        video.url_baiduyun = data["baiduyun"]
        video.url_bt = data["bt"]
        db.session.add(video)
        db.session.commit()
        flash("修改视频成功", "ok")
        return redirect(url_for('admin.video_edit', id=video.id))
    return render_template("admin/video_edit.html", form=form, video=video)


@admin.route("/video/del/<int:id>/")
@admin_login_req
def video_del(id=None):
    video = Video.query.get_or_404(id)
    db.session.delete(video)
    db.session.commit()
    return render_template(url_for('admin.move_list', page=1))

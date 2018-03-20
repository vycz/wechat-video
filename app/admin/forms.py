from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, SelectField
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Video, Tag

tags = Tag.query.all()


class VideoForm(FlaskForm):
    """视频添加"""
    title = StringField(
        label="片名",
        validators={
            DataRequired("请输入片名")
        },
        description="片名",
        render_kw={
            "class": "layui-input",
            "placeholder": "请输入片名"
        }
    )
    baiduyun = StringField(
        label="百度云链接",
        description="片名",
        default="",
        render_kw={
            "class": "layui-input",
            "placeholder": "请输入百度云链接"
        }
    )
    bt = StringField(
        label="BT链接",
        description="BT链接",
        default="",
        render_kw={
            "class": "layui-input",
            "placeholder": "请输入BT链接"
        }
    )
    release_time = StringField(
        label="上映年份",
        validators=[
            DataRequired("请选择上映年份")
        ],
        description="上映年份",
        render_kw={
            "class": "layui-input",
            "placeholder": "请选择上映年份",
            "id": "input_release_time"
        }
    )
    tag = SelectField(
        label="影片类别",
        validators=[
            DataRequired("请选择影片类别")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="影片类别",
    )
    logo = FileField(
        label='上传封面',
        description="封面",
    )
    submit = SubmitField(
        '立即提交',
        render_kw={
            "class": "layui-btn",
        }
    )


class LoginForm(FlaskForm):
    """登录"""
    username = StringField(
        label="用户名",
        validators=[
            DataRequired("请输入用户名")
        ],
        render_kw={
            "class": "layui-input",
            "placeholder": "用户名"
        }
    )

    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "layui-input",
            "placeholder": "密码",
        }
    )

    submit = SubmitField(
        '登录',
        render_kw={
            "class": "layui-btn"
        }
    )

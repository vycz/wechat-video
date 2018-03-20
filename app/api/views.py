# coding:utf8
from . import api
from app import app
from flask import render_template, redirect, url_for, request, abort
from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.replies import TextReply,ArticlesReply
from wechatpy.exceptions import (
    InvalidSignatureException,
    InvalidAppIdException,
)

TOKEN = app.config["TOKEN"]

@app.route('/')
def index():
    host = request.url_root
    return render_template('api/index.html', host=host)


@api.route("/wechat", methods=["GET", "POST"])
def wechat():
    signature = request.args.get('signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    encrypt_type = request.args.get('encrypt_type', 'raw')
    msg_signature = request.args.get('msg_signature', '')
    try:
        check_signature(TOKEN, signature, timestamp, nonce)
    except InvalidSignatureException:
        abort(403)
    if request.method == "POST":
        xml = request.get_data()
        msg = parse_message(xml)
        print(msg)
        reply = ArticlesReply(message=msg, articles=[
            {
                'title': u'你好',
                'description': u'你好',
                'url': u'http://www.qq.com',
                'image': 'http://image.tupian114.com/20121203/13050451.jpg.thumb.jpg'
            }])
        xml = reply.render()
        return xml

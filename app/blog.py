#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import(
    Blueprint,request,session,render_template,redirect,url_for,abort,jsonify
)
from models import db,Category,Tag,Article,Dictionary
import os
import re
import json
import time

bdp = Blueprint('blog',__name__,static_folder="blog/static",template_folder="blog/templates")

@bdp.route('/',methods=['GET'])
def index():
    aboutMe = Dictionary.query.filter_by(key="index_about_me_txt").first()
    aboutMeImg = Dictionary.query.filter_by(key="index_about_me_img").first()

    page = request.args.get('page', 1, type=int)
    article_list = Article.query.order_by(Article.date.desc()).paginate(page=page, per_page=15)
    return render_template('blog/index.html',aboutMe=aboutMe,aboutMeImg=aboutMeImg,article_list = article_list.items)

@bdp.route('/list')
def list():
    cid = request.args.get('cid',0,type=int)
    page = request.args.get('page', 1, type=int)

    cidList = [cid]

    category_list = Category.query.filter_by(fid=cid)
    for value in category_list:
        cidList.append(value.id)
    article_list = Article.query.order_by(Article.date.desc()).filter(Article.category_id.in_(cidList)).paginate(page=page, per_page=5)
    return render_template('blog/list.html',article_list=article_list.items,pagination=article_list,cid=cid)

@bdp.route('/article')
def article():
    id = request.args.get('id',0,type=int)

    article = Article.query.get(id)
    return render_template('blog/info.html',article=article)

@bdp.route('/about')
def about():
    about = Dictionary.query.filter_by(key="about").first()
    return render_template('blog/about.html',about=about)
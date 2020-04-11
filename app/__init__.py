#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import Flask,render_template
from config import  Config
from admin import adp
from blog import bdp
from models import init_db,Category,getCateList,getFidCate,getReArticle,getClickArticle
import sys

reload(sys)
sys.setdefaultencoding("utf-8")

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.jinja_env.globals['Category'] = Category
    app.jinja_env.globals['GETCATELIST'] = getCateList
    app.jinja_env.globals['GETFIDCATE'] = getFidCate
    app.jinja_env.globals['GETREARTICLE'] = getReArticle
    app.jinja_env.globals['GETCLICKARTICLE'] = getClickArticle


    '''blog模板'''
    app.register_blueprint(bdp)
    app.add_url_rule('/', endpoint='index')
    '''admin模块'''
    app.register_blueprint(adp)
    '''db数据库'''
    init_db(app)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('admin/error.html'), 404
    return app

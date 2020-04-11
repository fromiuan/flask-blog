#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
def init_db(app):
    db.init_app(app)

def getCateList():
    data = Category.query.all()
    new_data = []
    d_data = []

    for d in data:
        dict = {'name': d.name, 'level': d.level, 'fid': d.fid,'id':d.id,'son':[]}
        new_data.append(dict)

    son_id = []
    for d in new_data:
        for nd in new_data:
            if d["id"] == nd["fid"]:
                d["son"].append(nd)
                son_id.append(nd["id"])
        if d["id"] not in son_id:
            d_data.append(d)
    return d_data

def getFidCate():
    data = Category.query.filter_by(fid=0).all()
    return data

def getReArticle():
    data = Article.query.filter_by(flag=2).order_by(Article.date.desc()).limit(10).all()
    return data

def getClickArticle():
    data = Article.query.order_by(Article.views.desc()).limit(10).all()
    return data

sys_article_tag = db.Table('sys_article_tag',
    db.Column('article_id',db.Integer,db.ForeignKey('sys_article.id'),primary_key=True),
    db.Column('tag_id',db.Integer,db.ForeignKey('sys_tag.id'),primary_key=True)
)

class Category(db.Model):
    __tablename__ = 'sys_category'
    id = db.Column(db.Integer,primary_key=True,autoincrement=True)
    fid = db.Column(db.Integer,default=0)
    name = db.Column(db.String(64))
    level = db.Column(db.Integer,default=0)
    tree = db.Column(db.String(64),default='')
    def __repr__(self):
        return '<Category %s>' % self.name

    @staticmethod
    def getLevel(self):
        return self.query.all()


class Tag(db.Model):
    __tablename__ = 'sys_tag'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64))
    def __repr__(self):
        return '<Tag %s>' % self.name

class Article(db.Model):
    __tablename__ = 'sys_article'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column(db.Integer)
    title = db.Column(db.String(64))
    content = db.Column(db.Text)
    date = db.Column(db.DateTime,default=datetime.utcnow)
    views = db.Column(db.Integer)
    flag = db.Column(db.Integer,default=0)
    description = db.Column(db.Text,default='')
    img = db.Column(db.String(64),default='')
    tags = db.relationship('Tag', secondary=sys_article_tag, backref=db.backref('articles'))
    def __repr__(self):
        return '<Article %s>' % self.title

    def list(self):
        return self.query.order_by('id desc').all()

class User(db.Model):
    __tablename__ = 'sys_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(64))
    password = db.Column(db.String(64))
    date = db.Column(db.Date)

class Dictionary(db.Model):
    __tablename__ = 'sys_dictionary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(64))
    value = db.Column(db.Text)
    types = db.Column(db.Integer)
    describe = db.Column(db.String(64))
    date = db.Column(db.Date)

class Image(db.Model):
    __tablename__ = 'sys_images'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    types = db.Column(db.Integer)
    article_id = db.Column(db.Integer)
    name = db.Column(db.String(64))
    path = db.Column(db.String(64))
    date = db.Column(db.Date)

class Comment(db.Model):
    __tablename__ = 'sys_comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer)
    author = db.Column(db.String(64))
    content = db.Column(db.String(64))
    date = db.Column(db.DateTime, default=datetime.utcnow)
    up = db.Column(db.Integer)
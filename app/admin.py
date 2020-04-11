#!/usr/bin/python
# -*- coding: UTF-8 -*-
from flask import(
    Blueprint,request,session,render_template,redirect,url_for,abort,jsonify
)
from models import db,Category,Tag,Article,Dictionary,getCateList,Comment
from utils import Utils
import os
import re
import json
import time

adp = Blueprint('admin',__name__,url_prefix='/admin')

@adp.route('/')
def index():
    return render_template('admin/index.html')

@adp.route('/login',methods=['POST','GET'])
def login():
    if request.method == 'POST':
        if request.form['user'] == 'admin':
            session['user'] = request.form['user']
        else:
            return 'not user'
    else:
        if 'user' in session:
            return redirect(url_for('admin.index'))
        return render_template('admin/login.html')

@adp.route('/article')
def article():
    page = request.args.get('page', 1, type=int)
    if not page:
        page = 1
    article_list = Article.query.order_by(Article.id.desc()).paginate(page=page,per_page=5)
    return render_template('admin/article.html',article_list = article_list.items,pagination=article_list)

@adp.route('/article/add',methods=['POST','GET'])
def article_add():
    utils = Utils()
    if request.method == 'POST':
        id = request.form.get('id')
        title = request.form.get('title')
        category_id = request.form.get('category_id')
        content = request.form.get('content')
        views = request.form.get('views',0 ,type=int)
        flag = request.form.get('flag',0 ,type=int)
        tags = request.form.getlist('tags')
        description = request.form.get('description')

        imgList = utils.reImg(content)
        print imgList,len(imgList)
        print "======"
        img = ''
        if len(imgList) != 0:
            img = imgList[0]

        if id == '':
            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            article = Article(title=title,category_id=category_id,content=content,views=views,date=times,flag=flag,description=description,img=img)
            db.session.add(article)
            db.session.flush()
            db.session.commit()
            for value in tags:
                tag_info = Tag.query.filter_by(name=value).first()
                if tag_info is None:
                    tag = Tag(name=value)
                    article.tags.append(tag)
                    db.session.add(tag)
                    db.session.commit()
                else:
                    article.tags.append(tag_info)
                    db.session.add(tag_info)
                    db.session.commit()
        else:
            article = Article.query.filter_by(id=id).first()
            article.title = title
            article.category_id = category_id
            article.content = content
            article.views = views
            article.flag = flag
            article.img = img
            article.description = description
            db.session.commit()
            for value in tags:
                tag_info = Tag.query.filter_by(name=value).first()
                if tag_info is None:
                    tag = Tag(name=value)
                    article.tags.append(tag)
                    db.session.add(tag)
                    db.session.commit()
                else:
                    article.tags.append(tag_info)
                    db.session.add(tag_info)
                    db.session.commit()
        return redirect(url_for('admin.article'))

    id = request.args.get('id', 0)
    article_info = Article.query.get(id)
    category_list = Category.query.all()
    return render_template('admin/article_add.html',article_info = article_info,category_list = category_list)

@adp.route('/article/del')
def article_del():
    result = {'result':'fail'}
    id = request.args.get('id')
    if id != "":
        article = Article.query.get(id)
        db.session.delete(article)
        db.session.commit()
        result = {'result':'ok'}

    return jsonify(result)

@adp.route('/article/tag_del')
def article_tag_del():
    result = {'result':'fail'}
    article_id = request.args.get('article_id')
    tag_id = request.args.get('tag_id')
    if id != "":
        article = Article.query.get(article_id)
        tag = Tag.query.get(tag_id)
        article.tags.remove(tag)
        db.session.commit()
        result = {'result':'ok'}

    return jsonify(result)

@adp.route('/category')
def category():
    category_list = getCateList()
    return render_template('admin/category.html',category_list=category_list)

@adp.route('/category/add',methods=['POST','GET'])
def category_add():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']
        fid = request.form.get('fid',0,type=int)

        if id == '':
            category_info = Category.query.filter_by(id=fid).first()
            level = 1
            if category_info is not None:
                level = category_info.level + 1
                if level > 2:
                    return
            category = Category(fid=fid, name=name,level=level,tree='')
            db.session.add(category)
            db.session.flush()
            db.session.commit()

            if category.id > 0:
                category_update = Category.query.filter_by(id=category.id).first()
                if fid == 0:
                    category_update.tree = category.id
                else:
                    category_update.tree = "%(tree)s-%(id)d" %{"tree":category_info.tree,"id":category.id}
                db.session.add(category_update)
                db.session.commit()
        else:
            category = Category.query.filter_by(id=id).first()
            category.name = name
            category.fid = fid
            db.session.add(category)
            db.session.commit()
        return redirect(url_for('admin.category'))

    id = request.args.get('id', 0)
    category_info = Category.query.get(id)
    category_list = Category.query.all()
    return render_template('admin/category_add.html',category_info=category_info,category_list=category_list)

@adp.route('/tag')
def tag():
    tag_list = Tag.query.all()
    return render_template('admin/tag.html',tag_list=tag_list)

@adp.route('/tag/add',methods=['POST','GET'])
def tag_add():
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['name']

        if id == '':
            tag = Tag(name=name)
            db.session.add(tag)
            db.session.commit()
        else:
            tag = Tag.query.filter_by(id=id).first()
            tag.name = name
            db.session.add(tag)
            db.session.commit()
        return redirect(url_for('admin.tag'))

    id = request.args.get('id', 0)
    tag_info = Tag.query.get(id)
    tag_list = Tag.query.all()
    return render_template('admin/tag_add.html',tag_info=tag_info,tag_list=tag_list)

@adp.route('/set')
def set():
    set_list = Dictionary.query.all()
    return render_template('admin/set.html',set_list=set_list)

@adp.route('/set/add',methods=['POST','GET'])
def set_add():
    if request.method == 'POST':
        id = request.form['id']
        key = request.form.get('key')
        describe = request.form.get('describe')
        types = request.form.get('types',0,type=int)
        content = request.form.get('content')
        text = request.form.get('text')
        imgfile = request.files.get('imgfile')

        base_dir = os.path.dirname(__file__)

        if id == '':
            value = text
            if types == 1:
                value = content
            if types == 2:
                image_path = '/app/static/uploads/' + time.strftime("%Y%m%d")
                image_path_all = os.path.dirname(base_dir) + image_path
                if not os.path.exists(image_path_all):
                    os.mkdir(image_path_all)

                imgfile.save(image_path_all + "/" + imgfile.filename)
                value = image_path+"/"+imgfile.filename

            times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            set = Dictionary(key=key,value=value,types=types,date=times,describe=describe)
            db.session.add(set)
            db.session.commit()
        else:
            set = Dictionary.query.filter_by(id=id).first()

            value = text
            if types == 1:
                value = content
            if types == 2:
                image_path = '/app/static/uploads/' + time.strftime("%Y%m%d")
                image_path_all = os.path.dirname(base_dir) + image_path
                if not os.path.exists(image_path_all):
                    os.mkdir(image_path_all)

                imgfile.save(image_path_all + "/" + imgfile.filename)
                value = '/static/uploads/' + time.strftime("%Y%m%d") + "/" + imgfile.filename

            set.key = key
            set.value = value
            set.describe = describe
            set.types = types
            db.session.add(set)
            db.session.commit()
        return redirect(url_for('admin.set'))

    id = request.args.get('id', 0)
    set_info = Dictionary.query.get(id)
    return render_template('admin/set_add.html',set_info=set_info)

@adp.route('/comment',methods=['POST','GET'])
def comment():
    page = request.args.get('page', 1, type=int)
    if not page:
        page = 1
    comment_list = Comment.query.order_by(Comment.id.desc()).paginate(page=page, per_page=5)
    return render_template('admin/comment.html', comment_list=comment_list.items,pagination=comment_list)

@adp.route('/upload',methods=['POST','GET'])
def upload():
    result = {}
    action = request.args.get('action')

    base_dir = os.path.dirname(__file__)
    if action == 'config':
        f = open(os.path.dirname(base_dir)+'/app/static/admin/ueditor/php/config.json')
        new_content = re.sub(r'\/\*.*\*\/', '', f.read())
        result = json.loads(new_content)
        f.close()
    if action in ('uploadimage', 'uploadvideo', 'uploadfile'):
        upfile = request.files['upfile']

        image_path = '/app/static/uploads/'+time.strftime("%Y%m%d")
        image_path_all = os.path.dirname(base_dir)+image_path
        if not os.path.exists(image_path_all):
            os.mkdir(image_path_all)

        upfile.save(image_path_all+"/"+upfile.filename)
        result = {
            "state": "SUCCESS",
            "url": "/static/uploads/%s/%s" % (time.strftime("%Y%m%d"),upfile.filename),
            "title": upfile.filename,
            "original": upfile.filename
        }
        # times = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # db_images = Image(types=0,article_id=0,name=upfile.filename,path=time.strftime("%Y%m%d")+'/'+upfile.filename,date=times)
        # db.session.add(db_images)
        # db.session.commit()
    return jsonify(result)
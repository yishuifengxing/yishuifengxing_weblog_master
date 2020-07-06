import tornado.web
import tornado.ioloop
import tornado.httpserver
import time
from tornado.options import define, options
from utils.auth import authenticate, authadminenticate, regist, regist_userid, regist_tagname, regist_article_del, \
    regist_comment, regist_tag_del, regist_preview, regist_preview_del, regist_movie_del, regist_authname, \
    regist_rolename, regist_adminname, regist_acount_pwd, regist_article, regist_article_tagname, regist_acticle_tag_del
from pycket.session import SessionMixin
from files.regist_form import Regist_form
from files.user_form import UserdetailForm
from files.pwd_form import ModifypwdForm
from files.account.tag_form import TagForm
from files.account.account_login_form import Account_LoginForm
from files.account.movie_add_form import MovieForm
from files.account.PreviewForm import PreviewForm
from files.account.role_form import RoleForm
from files.account.auth_form import AuthForm
from files.account.admin_form import AdminForm
from files.account.account_pwd_form import Acount_pwd_Form
from files.account.article_form import ArticleForm
from files.comment_form import CommentForm
from files.account.article_tag_form import Article_Tag_Form
from data.user_module import User, Userlog, Tag, Movie, Preview, Comment, Role, Auth, Admin, Acticle, Acticle_tag
from utils.photo import sava_upload, save_upload_log, save_upload_Plog
from utils.auth import hashed, Pageination
import tornado.web
from tornado import gen
from tornado.concurrent import run_on_executor
from tornado.concurrent import futures
from tornado.web import StaticFileHandler
from tornado.web import RequestHandler
from PIL import Image
import json
import os
import re
import base64
import datetime
import uuid

define('port', default='8005', help='Listening port', type=int)


class AuthBaseHandle(tornado.web.RequestHandler, SessionMixin):
    def get_current_user(self):
        return self.session.get('username', None)


class BaseHandler(RequestHandler):

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '127.0.0.1')
        self.set_header('Access-Control-Max-Age', 1000)
        self.set_header('Content-type', 'application/json')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, DELETE, PUT, PATCH, OPTIONS')
        self.set_header('Access-Control-Allow-Headers',
                        'Content-Type, tsessionid, Access-Control-Allow-Origin, Access-Control-Allow-Headers, X-Requested-By, Access-Control-Allow-Methods')

    def options(self, *args, **kwargs):
        pass


class LoginHandler(AuthBaseHandle):
    def get(self):
        self.render('home/login.html')

    def post(self):
        username = self.get_argument('contact', '')
        password = self.get_argument('password', '')
        remote_ip = self.request.remote_ip
        user_id = regist_userid(username)
        user_id = user_id[0]
        now_time = time.asctime(time.localtime(time.time()))
        print("时间：", now_time)
        print('用户名:', username, '密码:', password, "ip:", remote_ip)
        if authenticate(username, password):
            Userlog.add_userlog(user_id, remote_ip)
            self.session.set('username', username)
            self.redirect('/index_login/')
        else:
            self.redirect('/login')


class LoginoutHandler(AuthBaseHandle):
    def get(self):
        self.session.delete('username')
        self.redirect('/login')


class IndexHandler(AuthBaseHandle):
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        # movie_page_date = Movie.movie_msg(key)
        movie_sign_data = Tag.tag_msg(key)
        # lastmovie_tag = 0
        movie_tag = self.get_query_argument('movie_tag', 0)
        print("movie_tag:", movie_tag)
        if movie_tag == "0":
            movie_tag = 0
        # print("star_movie:", star_movie)
        if movie_tag != 0:
            movie_id = Tag.tag_id(movie_tag)
            print("movie_id['id']:", movie_id['id'])
            movie_page_date = Movie.movie_msg(movie_id['id'])
            print("movie:", movie_page_date)
            page_obj = Pageination(page, movie_page_date)
            str_page = page_obj.str_page('/index/', key)
            star_movie = self.get_query_argument('star_movie', 0)
            print("star_movie:", star_movie)
            if star_movie != '0':
                movie_page_date = Movie.movie_star_msg(star_movie)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
            time_movie = self.get_query_argument('time_movie', 0)
            if time_movie != "0":
                if time_movie != '1':
                    movie_page_date = Movie.movie_star_msg(time_movie)
                    page_obj = Pageination(page, movie_page_date)
                    str_page = page_obj.str_page('/index/', key)
                else:
                    pass
            play_num_movie = self.get_query_argument('play_num_movie', 0)
            if play_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
                # print('movie_page_date2:', movie_page_date2)
            else:
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
            comm_num_movie = self.get_query_argument('comm_num_movie', 0)
            if comm_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
            else:
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
        else:
            movie_page_date = Movie.movie_msg()
            page_obj = Pageination(page, movie_page_date)
            # page_date = page_date[page_obj.start:page_obj.end]
            str_page = page_obj.str_page('/index/', key)

            star_movie = self.get_query_argument('star_movie', 0)
            print("star_movie:", star_movie)
            if star_movie == 0:
                star_movie = '0'
            if star_movie != '0':
                movie_page_date = Movie.movie_star_msg(star_movie)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)

            time_movie = self.get_query_argument('time_movie', 0)
            if time_movie != 0:
                pass

            play_num_movie = self.get_query_argument('play_num_movie', 0)
            if play_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
                # print('movie_page_date2:', movie_page_date2)
            if play_num_movie == "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)

            comm_num_movie = self.get_query_argument('comm_num_movie', 0)
            if comm_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)
            if comm_num_movie == "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index/', key)

        p_dic = dict(
            movie_tag=movie_tag,
            star_movie=star_movie,
            time_movie=time_movie,
            play_num_movie=play_num_movie,
            comm_num_movie=comm_num_movie,
        )
        print(p_dic)
        self.render('home/index.html', items=page_date, items_movie=movie_sign_data, items_movie_data=movie_page_date,
                    p_dic=p_dic, str_page=str_page)


class Index_loginHandler(AuthBaseHandle):
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        # movie_page_date = Movie.movie_msg(key)
        movie_sign_data = Tag.tag_msg(key)
        # lastmovie_tag = 0
        movie_tag = self.get_query_argument('movie_tag', 0)
        print("movie_tag:", movie_tag)
        if movie_tag == "0":
            movie_tag = 0
        # print("star_movie:", star_movie)
        if movie_tag != 0:
            movie_id = Tag.tag_id(movie_tag)
            print("movie_id['id']:", movie_id['id'])
            movie_page_date = Movie.movie_msg(movie_id['id'])
            print("movie:", movie_page_date)
            page_obj = Pageination(page, movie_page_date)
            str_page = page_obj.str_page('/index_login/', key)
            star_movie = self.get_query_argument('star_movie', 0)
            print("star_movie:", star_movie)
            if star_movie != '0':
                movie_page_date = Movie.movie_star_msg(star_movie)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
            time_movie = self.get_query_argument('time_movie', 0)
            if time_movie != "0":
                if time_movie != '1':
                    movie_page_date = Movie.movie_star_msg(time_movie)
                    page_obj = Pageination(page, movie_page_date)
                    str_page = page_obj.str_page('/index/', key)
                else:
                    pass
            play_num_movie = self.get_query_argument('play_num_movie', 0)
            if play_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
                # print('movie_page_date2:', movie_page_date2)
            else:
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
            comm_num_movie = self.get_query_argument('comm_num_movie', 0)
            if comm_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
            else:
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
        else:
            movie_page_date = Movie.movie_msg()
            page_obj = Pageination(page, movie_page_date)
            # page_date = page_date[page_obj.start:page_obj.end]
            str_page = page_obj.str_page('/index_login/', key)

            star_movie = self.get_query_argument('star_movie', 0)
            print("star_movie:", star_movie)
            if star_movie == 0:
                star_movie = '0'
            if star_movie != '0':
                movie_page_date = Movie.movie_star_msg(star_movie)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)

            time_movie = self.get_query_argument('time_movie', 0)
            if time_movie != 0:
                pass

            play_num_movie = self.get_query_argument('play_num_movie', 0)
            if play_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
                # print('movie_page_date2:', movie_page_date2)
            if play_num_movie == "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-1])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)

            comm_num_movie = self.get_query_argument('comm_num_movie', 0)
            if comm_num_movie != "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2], reverse=True)
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)
            if comm_num_movie == "0":
                movie_page_date = sorted(movie_page_date, key=lambda x: x[-2])
                page_obj = Pageination(page, movie_page_date)
                str_page = page_obj.str_page('/index_login/', key)

        p_dic = dict(
            movie_tag=movie_tag,
            star_movie=star_movie,
            time_movie=time_movie,
            play_num_movie=play_num_movie,
            comm_num_movie=comm_num_movie,
        )
        print(p_dic)
        self.render('home/index_login.html', items=page_date, items_movie=movie_sign_data,
                    items_movie_data=movie_page_date, p_dic=p_dic, str_page=str_page)


class RegistAnHandler(AuthBaseHandle):
    def get(self):
        form = Regist_form()
        msg = self.get_argument('msg', '')
        self.render('home/regist.html', form=form, msg={msg})

    def post(self):
        form = Regist_form(self.request.arguments)
        if form.validate():
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            name = form.name.data
            name = name.encode(encoding='UTF-8', errors='strict')
            email = form.email.data
            phone = form.phone.data
            password = form.pwd.data
            repassword = form.repwd.data
            uuid = str(User.UUID(now_time))
            # print(type(uuid))
            uuid = ''.join(uuid.split('-'))
            # print('name:', name ,'email:', email, 'phone:', phone, 'password:', password, 'repassword:', repassword, 'uuid:', uuid)
            if password == repassword:
                ret = regist(name, email, phone, password, uuid)
                if ret['msg'] == '用户名重复':
                    self.render('home/regist.html', form=form, msg=ret['msg'])
                elif ret['msg'] == '邮箱已经注册':
                    self.render('home/regist.html', form=form, msg=ret['msg'])
                    # self.redirect('/regist?msg={}'.format(ret['msg']),form = form)
                elif ret['msg'] == '手机已经注册':
                    self.render('home/regist.html', form=form, msg=ret['msg'])
                elif ret['msg'] == 'OK':
                    self.redirect('/login')
            pass
        else:
            self.render('home/regist.html', form=form)


class UserHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        username = self.current_user
        form = UserdetailForm()
        msg = self.get_argument('msg', '')
        user = User.get_user_msg(username)
        form.name.data = user.username
        form.email.data = user.email
        form.phone.data = user.phone
        form.info.data = user.info
        form.face.data = user.face
        if user.face:
            form.face.data = form.face.data[7:]
        print(type(form.face.data))
        self.render('home/user.html', form=form, msg={msg})

    def post(self):
        form = UserdetailForm(self.request.arguments)
        # f = self.request.files['face']
        username = self.current_user
        user = User.get_user_msg(username)
        uuid = user.uuid
        img_list = self.request.files.get('face', [])
        upload_img = img_list[0]
        if form.validate():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            info = form.info.data
            info = info.encode(encoding='UTF-8', errors='strict')
            face = sava_upload(upload_img)
            User.updata_user(uuid, name, email, phone, info, face)
            self.redirect('/user')
        else:
            self.redirect('/')


class PwdHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = ModifypwdForm(self.request.arguments)
        self.render('home/pwd.html', form=form)

    def post(self):
        username = self.current_user
        form = ModifypwdForm(self.request.arguments)
        if form.validate():
            old_pwd = form.old_pwd.data
            new_pwd = form.new_pwd.data
            new_repwd = form.new_repwd.data
            if authenticate(username, old_pwd):
                if new_pwd == new_repwd:
                    new_pwd = hashed(new_pwd)
                    User.updata_pwd(username, new_pwd)
                    Admin.updata_pwd(username, new_pwd)
                    self.session.delete('username')
                    self.redirect('/login')
            else:
                self.render('home/pwd.html', form=form)


class CommentsHandler(AuthBaseHandle):
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Comment.comment_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/comments/', key)
        self.render('home/comments.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)
        # self.render('home/comments.html')


class LoginlogHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Userlog.userlog_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/loginlog/', key)
        self.render('home/loginlog.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)
        # self.render('home/loginlog.html')


class MoviecolHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        self.render('home/moviecol.html')


class SearchHandler(AuthBaseHandle):
    def get(self):
        self.render('home/search.html')


class PlayHandler(AuthBaseHandle):

    def get(self, page):
        remote_ip = self.request.remote_ip
        print("ip:", remote_ip)
        form = CommentForm(self.request.arguments)
        key = self.get_argument("id", "")
        key_page = self.get_argument("page", "")
        movie_data = Movie.movie_play_msg(key)
        mov_data = movie_data
        mov_list = []
        for m in movie_data:
            tag_id = m.tag_id
            tag_name = Tag.get_tag_name(tag_id)
            tag_name = tag_name[0]
            mo_data = movie_data[0]
            mo_data = list(mo_data)
            mo_data[7] = tag_name
            mov_list.append(tuple(mo_data))
            print("page_data[0]", mov_list)
        key2 = self.get_argument("key", "")
        page_date = Comment.comment_msg(key)
        print("page:", page_date)
        page_data = page_date
        user_list = []
        j = 0
        k = 0
        for f in page_date:
            k = k + 1
        Movie.updata_commentnum(key, k)
        Movie.updata_playtnum(key)
        for i in page_date:
            user_id = i.user_id
            user = User.get_user_name(user_id)
            username = user.username
            userface = user.face
            data = page_data[j]
            j = j + 1
            data = list(data)
            data[3] = username
            data.append(userface)
            data.append(k)
            # print("data:",data)
            user_list.append(tuple(data))
        print("user_list", user_list)
        page_obj = Pageination(key_page, user_list)
        page_date = user_list[page_obj.start:page_obj.end]
        base_url = '/play?id=%s' % (key)
        str_page = page_obj.str_page_play(base_url, key2)

        self.render('home/play.html', items_movie=mov_list, form=form, items=page_date,
                    count_page=page_obj.current_page, str_page=str_page, count=j)

    def post(self, page):
        content = self.get_argument('content', 'None')
        movie_col = self.get_argument('m_c_id', 0)
        key_id = int(self.get_argument('mid', 0))
        user_name = self.current_user
        user_id = regist_userid(user_name)
        user_id = user_id[0]
        if content and key_id != 0:
            # print('在这里呢')
            ret = regist_comment(content, key_id, user_id)
            if ret['msg'] == 'ok':
                self.write(json.dumps(dict(ok=1)))
        elif movie_col != 0:
            self.write(json.dumps(dict(ok=2)))
        elif content == '':
            self.write(json.dumps(dict(ok=0)))


class Movie_colHandler(AuthBaseHandle):
    def get(self):
        movie_col = self.get_argument('m_c_id', None)
        print('m_c_id', movie_col)
        print('movie_col', type(movie_col))


class CommentHandler(AuthBaseHandle):
    pass


class MusicHandler(AuthBaseHandle):
    def get(self):
        self.render('home/music.html')


class ArticleHandler(AuthBaseHandle):
    # def get(self):
    #     form = ArticleForm(self.request.arguments)
    #     msg = self.get_argument('msg', '')
    #     self.render('home/article.html', form=form, msg={msg})

    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        article_sign_data = Acticle_tag.tag_msg(key)
        # lastmovie_tag = 0
        article_tag = self.get_query_argument('article_tag', 0)
        if article_tag != 0:
            movie_id = Acticle_tag.tag_id(article_tag)
            print("movie_id['id']:", movie_id['id'])
            article_page_date = Acticle.article_msg(movie_id['id'])
        else:
            article_page_date = Acticle.article_msg()
            page_obj = Pageination(page, page_date)
            page_date = page_date[page_obj.start:page_obj.end]
            str_page = page_obj.str_page('/article/', key)

        time_movie = self.get_body_argument('time_movie', 0)
        if time_movie != 0:
            pass

        play_num_movie = self.get_body_argument('play_num_movie', 0)
        if play_num_movie != 0:
            pass

        comm_num_movie = self.get_body_argument('comm_num_movie', 0)
        if comm_num_movie != 0:
            pass

        p_dic = dict(
            movie_tag=article_tag,
            time_movie=time_movie,
            play_num_movie=play_num_movie,
            comm_num_movie=comm_num_movie,
        )
        print(p_dic)
        self.render('home/article.html', items=page_date, items_movie=article_sign_data, items_movie_data=article_page_date,
                    p_dic=p_dic, str_page=str_page)


class Article_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = ArticleForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/article_add.html', form=form, msg={msg})

    def post(self):
        form = ArticleForm(self.request.arguments)
        logo = self.request.files.get('logo', [])
        upload_img = logo[0]
        if form.validate():
            title = form.title.data
            info = form.info.data
            logo = save_upload_Plog(upload_img)
            tag_id = form.tag_id.data
            content = form.artic.data
            logo = logo[7:]
            print(logo)
            ret = regist_article(title, info, logo, tag_id, content)
            if ret['msg'] == 'OK':
                self.render('account/article_add.html', form=form, msg=ret['msg'])


class Article_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        id = self.get_argument('id', '')

        if id:
            regist_article_del(id)
        key = self.get_argument("key", "")
        page_date = Acticle.article_msg(key)
        mov_list = []
        i = 0
        for m in page_date:
            tag_id = m.tag_id
            tag_name = Tag.get_tag_name(tag_id)
            mo_data = page_date[i]
            tag_name = tag_name[0]
            i += 1
            mo_data = list(mo_data)
            mo_data[5] = tag_name
            mov_list.append(tuple(mo_data))
        print("mov_list:", mov_list)
        page_obj = Pageination(page, mov_list)
        page_date = mov_list[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/article_list/', key)
        self.render('account/article_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Article_list_delHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        regist_movie_del(id)
        self.render('account/article_list.html')

    # 文章添加标签


class Article_tag_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = Article_Tag_Form(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/article_tag.html', form=form, msg={msg})

    def post(self):
        form = Article_Tag_Form(self.request.arguments)
        if form.validate():
            name = form.name.data
            ret = regist_article_tagname(name)
            if ret['msg'] == 'OK':
                self.render('account/article_tag.html', form=form, msg=ret['msg'])
            else:
                self.render('account/article_tag.html', form=form, msg=ret['msg'])


# 文章标签列表
class Article_tag_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        id = self.get_argument('id', '')
        if id:
            regist_acticle_tag_del(id)
        key = self.get_argument("key", "")
        page_date = Acticle_tag.tag_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/article_tag_list/', key)
        self.render('account/article_tag_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Article_tag_list_delHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        regist_tag_del(id)
        self.render('account/article_tag_list.html')


class Aticle_viweHandler(AuthBaseHandle):
    def get(self):
        remote_ip = self.request.remote_ip
        print("ip:", remote_ip)
        form = CommentForm(self.request.arguments)
        key = self.get_argument("id", "")
        key_page = self.get_argument("page", "")
        Acticle_data = Acticle.article_viwe_msg(key)
        act_data = Acticle_data
        act_list = []
        for m in act_data:
            tag_id = m.tag_id
            tag_name = Acticle_tag.get_tag_name(tag_id)
            tag_name = tag_name[0]
            mo_data = act_data[0]
            mo_data = list(mo_data)
            mo_data[3] = tag_name
            act_list.append(tuple(mo_data))
            print("page_data[0]",act_list)
        key2 = self.get_argument("key", "")
        page_date = Comment.comment_msg(key)
        print("page:", page_date)
        page_data = page_date
        user_list = []
        j = 0
        k = 0
        for f in page_date:
            k = k + 1
        # Movie.updata_commentnum(key, k)
        # Movie.updata_playtnum(key)
        for i in page_date:
            user_id = i.user_id
            user = User.get_user_name(user_id)
            username = user.username
            userface = user.face
            data = page_data[j]
            j = j + 1
            data = list(data)
            data[3] = username
            data.append(userface)
            data.append(k)
            # print("data:",data)
            user_list.append(tuple(data))
        print("user_list", user_list)
        page_obj = Pageination(key_page, user_list)
        page_date = user_list[page_obj.start:page_obj.end]
        base_url = '/play?id=%s' % (key)
        str_page = page_obj.str_page_play(base_url, key2)

        self.render('home/article_viwe.html', items_article=act_list, items_movie=act_list, form=form, items=page_date,
                    count_page=page_obj.current_page, str_page=str_page, count=j)

    def post(self, page):
        content = self.get_argument('content', 'None')
        movie_col = self.get_argument('m_c_id', 0)
        key_id = int(self.get_argument('mid', 0))
        user_name = self.current_user
        user_id = regist_userid(user_name)
        user_id = user_id[0]
        if content and key_id != 0:
            # print('在这里呢')
            ret = regist_comment(content, key_id, user_id)
            if ret['msg'] == 'ok':
                self.write(json.dumps(dict(ok=1)))
        elif movie_col != 0:
            self.write(json.dumps(dict(ok=2)))
        elif content == '':
            self.write(json.dumps(dict(ok=0)))


class AdminHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        self.render('account/admin.html')


class Aadmin_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = AdminForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/admin_add.html', form=form, msg={msg})

    def post(self):
        form = AdminForm(self.request.arguments)
        if form.validate():
            now_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
            uuid = str(User.UUID(now_time))
            uuid = ''.join(uuid.split('-'))
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            pwd = form.pwd.data
            repwd = form.repwd.data
            role_id = form.role_id.data
            if pwd == repwd:
                pwd = hashed(pwd)
                ret = regist_adminname(name, pwd, role_id, email, phone, uuid)
                if ret['msg'] == 'OK':
                    self.render('account/admin_add.html', form=form, msg=ret['msg'])
                else:
                    self.render('account/admin_add.html', form=form, msg=ret['msg'])


class Aadmin_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Admin.admin_msg(key)
        print(page_date)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/admin_list/', key)
        self.render('account/admin_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Aadminloginlog_listHandler(AuthBaseHandle):
    def get(self):
        self.render('account/adminloginlog_list.html')


class Auth_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = AuthForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/auth_add.html', form=form, msg={msg})

    def post(self):
        form = AuthForm(self.request.arguments)
        if form.validate():
            name = form.name.data
            url = form.url.data
            ret = regist_authname(name, url)
            if ret['msg'] == 'OK':
                self.render('account/auth_add.html', form=form, msg=ret['msg'])
            else:
                self.render('account/auth_add.html', form=form, msg=ret['msg'])


class Auth_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Auth.auth_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/auth_list/', key)
        self.render('account/auth_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)

    # def get(self, page):
    #     key = self.get_argument("key", "")
    #     page_date = Auth.auth_msg(key)
    #     print('page_date', page_date)
    #     page_obj = Pageination(page, page_date)
    #     page_date = page_date[page_obj.start:page_obj.end]
    #     str_page = page_obj.str_page('/auth_list/', key)
    #     self.render('account/auth_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
    #                 key=key)


class GridHandler(AuthBaseHandle):
    def get(self):
        self.render('account/grid.html')


class Account_indexHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        self.render('account/index.html')


class Account_loginHandler(AuthBaseHandle):
    def get(self):
        form = Account_LoginForm(self.request.arguments)
        self.session.delete('username')
        self.render('account/login.html', form=form)

    def post(self):
        form = Account_LoginForm(self.request.arguments)
        username = form.account.data
        password = form.pwd.data
        print('用户名:', username, '密码:', password)
        if authadminenticate(username, password):
            self.session.set('username', username)
            self.redirect('/account_index')
        else:
            self.redirect('/account_login')


class Account_login_outHandler(AuthBaseHandle):
    def get(self):
        self.session.delete('username')
        self.redirect('/account_login')


class Movie_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        msg = self.get_argument('msg', '')
        form = MovieForm(self.request.arguments)
        self.render('account/movie_add.html', form=form, msg={msg})

    def post(self):
        form = MovieForm(self.request.arguments)
        logo = self.request.files.get('logo', [])
        upload_img = logo[0]
        url = self.request.files.get('url', [])
        upload_url = url[0]
        err = {'err': '上传失败'}
        if form.validate():
            title = form.title.data
            url = save_upload_log(upload_url)
            info = form.info.data
            logo = save_upload_log(upload_img)
            star = form.star.data
            tag_id = form.tag_id.data
            area = form.area.data
            length = form.length.data
            release_time = form.release_time.data
            ret = Movie.movie_updata(title, url, info, logo, star, tag_id, area, length, release_time)
            if ret['msg'] == 'OK':
                self.render('account/movie_add.html', form=form, msg=ret['msg'])
            else:
                self.render('account/movie_add.html', form=form, msg=err['err'])


class Movie_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        id = self.get_argument('id', '')
        if id:
            regist_movie_del(id)
        key = self.get_argument("key", "")
        page_date = Movie.movie_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/movie_list/', key)
        self.render('account/movie_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Movie_list_delHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        regist_movie_del(id)
        self.render('account/movie_list.html')


class Moviecol_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/movidcol_list/', key)
        self.render('account/moviecol_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)
    # def get(self):
    #     self.render('account/movidcol_list.html')


class Oplog_listHandler(AuthBaseHandle):
    def get(self):
        self.render('account/oplog_list.html')


class Preview_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = PreviewForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/preview_add.html', form=form, msg={msg})

    def post(self):
        form = PreviewForm(self.request.arguments)
        logo = self.request.files.get('logo', [])
        upload_img = logo[0]
        if form.validate():
            title = form.title.data
            logo = save_upload_Plog(upload_img)
            logo = logo[7:]
            print(logo)
            ret = regist_preview(title, logo)
            if ret['msg'] == 'OK':
                self.render('account/preview_add.html', form=form, msg=ret['msg'])
            else:
                self.render('account/preview_add.html', form=form, msg=ret['msg'])


class Preview_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        id = self.get_argument('id', '')
        if id:
            regist_preview_del(id)
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/preview_list/', key)
        self.render('account/preview_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Preview_list_delHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        regist_tag_del(id)
        self.render('account/preview_list.html')


#
#
#         self.render('account/preview_list.html')

# class Preview_listHandler(AuthBaseHandle):
#     @tornado.web.authenticated
#     def get(self):
#         self.render('account/preview_list.html')

class Comment_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Comment.comment_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/comment_list/', key)
        self.render('account/comment_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


# class Comment_listHandler(AuthBaseHandle):
#     def get(self):
#         self.render('account/comment_list.html')

class Account_pwdHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = Acount_pwd_Form(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/pwd.html', form=form, msg={msg})

    def post(self):
        form = Acount_pwd_Form(self.request.arguments)
        user = self.get_current_user()
        if form.validate():
            oldpwd = form.oldpwd.data
            newpwd = form.newpwd.data
            renewpwd = form.renewpwd.data
            newpwd = hashed(newpwd)
            renewpwd = hashed(renewpwd)
            ret = regist_acount_pwd(user, oldpwd, newpwd, renewpwd)
            if ret['msg'] == 'OK':
                # self.render('account/login.html', form=form, msg=ret['msg'])
                self.session.delete('username')
                self.redirect('/account_login')
                # self.render('account/login.html')
            else:
                self.render('account/pwd.html', form=form, msg=ret['msg'])


class Role_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = RoleForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/role_add.html', form=form, msg={msg})

    def post(self):
        form = RoleForm(self.request.arguments)
        if form.validate():
            name = form.name.data
            auths = form.auths_list.data
            ret = regist_rolename(name, auths)
            if ret['msg'] == 'OK':
                self.render('account/role_add.html', form=form, msg=ret['msg'])
            else:
                self.render('account/role_add.html', form=form, msg=ret['msg'])


class Role_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = Role.role_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/role_list/', key)
        self.render('account/role_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


# 添加标签
class Tag_addHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        form = TagForm(self.request.arguments)
        msg = self.get_argument('msg', '')
        self.render('account/tag_add.html', form=form, msg={msg})

    def post(self):
        form = TagForm(self.request.arguments)
        if form.validate():
            name = form.name.data
            ret = regist_tagname(name)
            if ret['msg'] == 'OK':
                self.render('account/tag_add.html', form=form, msg=ret['msg'])
            else:
                self.render('account/tag_add.html', form=form, msg=ret['msg'])


# 标签列表
class Tag_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        id = self.get_argument('id', '')
        if id:
            regist_tag_del(id)
        key = self.get_argument("key", "")
        page_date = Tag.tag_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/tag_list/', key)
        self.render('account/tag_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)


class Tag_list_delHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        regist_tag_del(id)
        self.render('account/tag_list.html')


class User_listHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self, page):
        key = self.get_argument("key", "")
        page_date = User.user_msg(key)
        page_obj = Pageination(page, page_date)
        page_date = page_date[page_obj.start:page_obj.end]
        str_page = page_obj.str_page('/user_list/', key)
        self.render('account/user_list.html', items=page_date, count_page=page_obj.current_page, str_page=str_page,
                    key=key)
        # self.render('account/user_list.html')


class User_viewHandler(AuthBaseHandle):
    @tornado.web.authenticated
    def get(self):
        id = self.get_argument('id')
        print("id:", id)
        page_date = User.user_msg_data(id)
        self.render('account/user_view.html', items=page_date)


class UserloginlogHandler(AuthBaseHandle):
    def get(self):
        self.render('account/userloginlog_list.html')


class Not_findHandler(AuthBaseHandle):
    def get(self):
        self.render('home/404.html')


class AnimationHandler(AuthBaseHandle):
    def get(self):
        key = self.get_argument("key", "")
        page_date = Preview.preview_msg(key)
        self.render('home/animation.html', items=page_date)


# /* 前后端通信相关的配置,注释只允许使用多行方式 */

ueditor_config = {
    # /* 上传图片配置项 */
    "imageActionName": "uploadimage",  # /* 执行上传图片的action名称 */
    "imageFieldName": "upfile",  # /* 提交的图片表单名称 */
    "imageMaxSize": 2048000,  # /* 上传大小限制，单位B */
    "imageAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # /* 上传图片格式显示 */
    "imageCompressEnable": True,  # /* 是否压缩图片,默认是true */
    "imageCompressBorder": 1600,  # /* 图片压缩最长边限制 */
    "imageInsertAlign": "center",  # /* 插入的图片浮动方式 */
    "imageUrlPrefix": "/upload/image/",  # /* 图片访问路径前缀 */
    "imagePathFormat": "upload/image/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    # /* {filename} 会替换成原文件名,配置这项需要注意中文乱码问题 */
    # /* {rand:6} 会替换成随机数,后面的数字是随机数的位数 */
    # /* {time} 会替换成时间戳 */
    # /* {yyyy} 会替换成四位年份 */
    # /* {yy} 会替换成两位年份 */
    # /* {mm} 会替换成两位月份 */
    # /* {dd} 会替换成两位日期 */
    # /* {hh} 会替换成两位小时 */
    # /* {ii} 会替换成两位分钟 */
    # /* {ss} 会替换成两位秒 */
    # /* 非法字符 \ : * ? " < > | */
    # /* 具请体看线上文档: fex.baidu.com/ueditor/#use-format_upload_filename */

    # /* 涂鸦图片上传配置项 */
    "scrawlActionName": "uploadscrawl",  # /* 执行上传涂鸦的action名称 */
    "scrawlFieldName": "upfile",  # /* 提交的图片表单名称 */
    "scrawlPathFormat": "upload/image/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    "scrawlMaxSize": 2048000,  # /* 上传大小限制，单位B */
    "scrawlUrlPrefix": "/upload/image/",  # /* 图片访问路径前缀 */
    "scrawlInsertAlign": "center",

    # /* 截图工具上传 */
    "snapscreenActionName": "uploadimage",  # /* 执行上传截图的action名称 */
    "snapscreenPathFormat": "upload/image/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    "snapscreenUrlPrefix": "/upload/image/",  # /* 图片访问路径前缀 */
    "snapscreenInsertAlign": "center",  # /* 插入的图片浮动方式 */

    # /* 抓取远程图片配置 */
    "catcherLocalDomain": ["127.0.0.1", "localhost", "img.baidu.com"],
    "catcherActionName": "catchimage",  # /* 执行抓取远程图片的action名称 */
    "catcherFieldName": "source",  # /* 提交的图片列表表单名称 */
    "catcherPathFormat": "upload/image/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    "catcherUrlPrefix": "/upload/image/",  # /* 图片访问路径前缀 */
    "catcherMaxSize": 2048000,  # /* 上传大小限制，单位B */
    "catcherAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # /* 抓取图片格式显示 */

    # /* 上传视频配置 */
    "videoActionName": "uploadvideo",  # /* 执行上传视频的action名称 */
    "videoFieldName": "upfile",  # /* 提交的视频表单名称 */
    "videoPathFormat": "upload/video/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    "videoUrlPrefix": "/upload/video/",  # /* 视频访问路径前缀 */
    "videoMaxSize": 102400000,  # /* 上传大小限制，单位B，默认100MB */
    "videoAllowFiles": [
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid"],  # /* 上传视频格式显示 */

    # /* 上传文件配置 */
    "fileActionName": "uploadfile",  # /* controller里,执行上传视频的action名称 */
    "fileFieldName": "upfile",  # /* 提交的文件表单名称 */
    "filePathFormat": "upload/file/",  # /* 上传保存路径,可以自定义保存路径和文件名格式 */
    "fileUrlPrefix": "/upload/file/",  # /* 文件访问路径前缀 */
    "fileMaxSize": 51200000,  # /* 上传大小限制，单位B，默认50MB */
    "fileAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ],  # /* 上传文件格式显示 */

    # /* 列出指定目录下的图片 */
    "imageManagerActionName": "listimage",  # /* 执行图片管理的action名称 */
    "imageManagerListPath": "upload/image/",  # /* 指定要列出图片的目录 */
    "imageManagerListSize": 20,  # /* 每次列出文件数量 */
    "imageManagerUrlPrefix": "/upload/image/",  # /* 图片访问路径前缀 */
    "imageManagerInsertAlign": "center",  # /* 插入的图片浮动方式 */
    "imageManagerAllowFiles": [".png", ".jpg", ".jpeg", ".gif", ".bmp"],  # /* 列出的文件类型 */

    # /* 列出指定目录下的文件 */
    "fileManagerActionName": "listfile",  # /* 执行文件管理的action名称 */
    "fileManagerListPath": "upload/file/",  # /* 指定要列出文件的目录 */
    "fileManagerUrlPrefix": "/upload/file/",  # /* 文件访问路径前缀 */
    "fileManagerListSize": 20,  # /* 每次列出文件数量 */
    "fileManagerAllowFiles": [
        ".png", ".jpg", ".jpeg", ".gif", ".bmp",
        ".flv", ".swf", ".mkv", ".avi", ".rm", ".rmvb", ".mpeg", ".mpg",
        ".ogg", ".ogv", ".mov", ".wmv", ".mp4", ".webm", ".mp3", ".wav", ".mid",
        ".rar", ".zip", ".tar", ".gz", ".7z", ".bz2", ".cab", ".iso",
        ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".pdf", ".txt", ".md", ".xml"
    ]  # /* 列出的文件类型 */
}


class UeditorEnv():
    walkImageCache = []
    walkFileCache = []

    def __init__(self, with_list_cache=False):
        self.config = ueditor_config
        # print(self.config)

        # build file lists as cache
        if with_list_cache:
            self.walkin(self.config['imagePathFormat'], self.walkImageCache)
            self.walkin(self.config['filePathFormat'], self.walkFileCache)
        # print json.dumps(self.config, indent=1)

    # this only for single runtime instance
    # only if you use NAS as the file backend
    # for multi runtime instance please use database for indexing
    # also ,please add your file sync implement

    def walkin(self, base_dir, cache):
        for root, dirs, files in os.walk(base_dir):
            for name in files:
                cache.append({'file': os.path.join(root.replace(base_dir, ''), name)})

    def get_list(self, start=0, count=20, is_image=True):
        ret = []
        if is_image:
            cache = self.walkImageCache
        else:
            cache = self.walkFileCache

        # fill it as possible, if overthe range, simplely go out
        try:
            for index in range(start, start + count):
                ret.append({'url': cache[index]['file']})
        except:
            pass

        return ret

    def append_file(self, filename, is_image=True):
        if is_image:
            cache = self.walkImageCache
        else:
            cache = self.walkFileCache
        cache.append({'file': filename})


u4Ts = UeditorEnv(with_list_cache=True)


# from MxForm.handler import BaseHandler
class UploadHandler(AuthBaseHandle):
    executor = futures.ThreadPoolExecutor(100)

    @run_on_executor()
    def save_file(self, fileobj, base_dir, filename=None, user=None, is_image=True):
        if not user:
            user = 'ueditor'

        upload_path = user + '/' + datetime.datetime.utcnow().strftime('%Y%m%d') + '/'

        # 安全过滤
        base_dir = base_dir.replace('../', '')
        base_dir = re.sub(r'^/+', '', base_dir)
        if not os.path.exists(base_dir + upload_path):
            os.makedirs(base_dir + upload_path)

        if not filename:
            uuidhex = uuid.uuid1().hex
            file_ext = os.path.splitext(fileobj['filename'])[1].lower()
            filename = uuidhex + file_ext

        if not os.path.exists(base_dir + upload_path + filename):
            with open(base_dir + upload_path + filename, 'wb') as f:
                f.write(fileobj['body'])
            result = {
                'state': 'SUCCESS',
                'url': upload_path + filename,
                'title': filename,
                'original': fileobj['filename'],
            }
            u4Ts.append_file(upload_path + filename, is_image=is_image)
            return result
            # self.write(result)
            # self.finish()

    @gen.coroutine
    def get(self):
        action = self.get_argument('action')
        if action == 'config':
            self.write(ueditor_config)
            return

        elif action == u4Ts.config['imageManagerActionName']:
            start = int(self.get_argument('start'))
            size = int(self.get_argument('size'))
            urls = u4Ts.get_list(start, size, is_image=True)
            result = {
                'state': 'SUCCESS',
                'list': urls,
                'start': start,
                'total': len(urls)
            }
            # self.write(result)
            # self.finish()
            return result

        elif action == u4Ts.config['fileManagerActionName']:
            start = int(self.get_argument('start'))
            size = int(self.get_argument('size'))
            urls = u4Ts.get_list(start, size, is_image=False)
            result = {
                'state': 'SUCCESS',
                'list': urls,
                'start': start,
                'total': len(urls)
            }
            self.write(result)
            self.finish()
            return

        self.finish()

    @gen.coroutine
    def post(self):
        data = {}
        action = self.get_argument('action')
        if action == u4Ts.config['imageActionName']:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    data = yield self.save_file(base_dir=u4Ts.config['imagePathFormat'], fileobj=fileobj)

        elif action == u4Ts.config['scrawlActionName']:
            # python2
            # fileobj = {'filename': 'scrawl.png', 'body': base64.decodestring(self.get_argument(u4Ts.config['scrawlFieldName']))}
            # python3
            fileobj = {'filename': 'scrawl.png',
                       'body': base64.decodebytes(self.get_argument(u4Ts.config['scrawlFieldName']).encode('utf-8'))}
            data = yield self.save_file(base_dir=u4Ts.config['scrawlPathFormat'], fileobj=fileobj)

        elif action == u4Ts.config['snapscreenActionName']:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    data = yield self.save_file(base_dir=u4Ts.config['snapscreenPathFormat'], fileobj=fileobj)

        elif action == u4Ts.config['videoActionName']:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    data = yield self.save_file(base_dir=u4Ts.config['videoPathFormat'], fileobj=fileobj)

        elif action == u4Ts.config['fileActionName']:
            for keys in self.request.files:
                for fileobj in self.request.files[keys]:
                    data = yield self.save_file(base_dir=u4Ts.config['filePathFormat'], fileobj=fileobj, is_image=False)
        self.set_header("Content-Type", "text/html")
        self.write(json.dumps(data))
        self.finish()
        # self.finish(data)


# class UeditorHandler(RequestHandler):
#
#     @gen.coroutine
#     def get(self):
#         self.render('ueditor.html')


class Application(tornado.web.Application):
    def __init__(self):
        autoescape = None
        handlers = [
            (r"/login", LoginHandler),
            (r"/logout", LoginoutHandler),
            (r"/index/(?P<page>\d*)", IndexHandler),
            (r"/index_login/(?P<page>\d*)", Index_loginHandler),
            (r"/regist", RegistAnHandler),
            (r"/user", UserHandler),
            (r"/pwd", PwdHandler),
            (r"/comments/(?P<page>\d*)", CommentsHandler),
            (r"/loginlog/(?P<page>\d*)", LoginlogHandler),
            (r"/moviecol", MoviecolHandler),
            (r"/search", SearchHandler),
            (r"/play(?P<page>\d*)", PlayHandler),
            (r"/play_comm", CommentHandler),
            (r"/play_movie_col", Movie_colHandler),

            (r"/music", MusicHandler),
            (r"/article/(?P<page>\d*)", ArticleHandler),
            (r"/article_add", Article_addHandler),
            (r"/article_list/(?P<page>\d*)", Article_listHandler),
            (r"/article_tag", Article_tag_addHandler),
            (r"/article_tag_list/(?P<page>\d*)", Article_tag_listHandler),
            (r"/tag_list_del", Article_tag_list_delHandler),
            (r"/article_viwe", Aticle_viweHandler),
            (r"/admin", Aadmin_addHandler),
            (r"/admin_add", Aadmin_addHandler),
            (r"/admin_list/(?P<page>\d*)", Aadmin_listHandler),
            (r"/comment_list/(?P<page>\d*)", Comment_listHandler),
            (r"/auth_list/(?P<page>\d*)", Auth_listHandler),
            (r"/auth_add", Auth_addHandler),
            (r"/grid", GridHandler),
            (r"/account_index", Account_indexHandler),
            (r"/account_login", Account_loginHandler),
            (r"/account_login_out", Account_login_outHandler),
            (r"/movie_add", Movie_addHandler),
            (r"/movie_list/(?P<page>\d*)", Movie_listHandler),
            (r"/movie_list_del", Movie_list_delHandler),
            (r"/moviecol_list/(?P<page>\d*)", Moviecol_listHandler),
            (r"/adminloginlog_list", Aadminloginlog_listHandler),
            (r"/oplog_list", Oplog_listHandler),
            (r"/preview_add", Preview_addHandler),
            (r"/preview_list_del", Preview_list_delHandler),
            (r"/preview_list/(?P<page>\d*)", Preview_listHandler),
            (r"/account_pwd", Account_pwdHandler),
            (r"/role_add", Role_addHandler),
            (r"/role_list/(?P<page>\d*)", Role_listHandler),
            (r"/tag_add", Tag_addHandler),
            (r"/tag_list/(?P<page>\d*)", Tag_listHandler),
            (r"/tag_list_del", Tag_list_delHandler),
            (r"/user_list/(?P<page>\d*)", User_listHandler),
            (r"/user_view", User_viewHandler),
            (r"/userloginlog_list", UserloginlogHandler),
            (r"/animation", AnimationHandler),
            (r"/article_add", ArticleHandler),
            (r"/*", Not_findHandler),
            (r'/upload/', UploadHandler),
            # (r'/ueditor', UeditorHandler),
            (r'/upload/(.*)', StaticFileHandler, {'path': 'upload'}),
        ]
        settings = dict(
            debug=True,
            template_path='templates',
            static_path='static',
            login_url='/login',  # 没有登录则跳转至此
            cookie_secret='1q2w3e4r',  # 加密cookie的字符串
            pycket={  # 固定写法packet，用于保存用户登录信息
                'engine': 'redis',
                'storage': {
                    'host': 'localhost',
                    # 'host': '172.17.0.6',
                    'port': 6379,
                    'db_sessions': 5,
                    'db_notifications': 11,
                    'max_connections': 2 ** 33,
                },
                'cookie': {
                    'expires_days': 38,
                    'max_age': 100
                }
            }
        )
        super().__init__(handlers, **settings)


application = Application()

if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(application, xheaders=True)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

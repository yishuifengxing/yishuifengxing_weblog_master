import hashlib
from data.connect import Base
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, TEXT, Date, SmallInteger, BigInteger
from sqlalchemy.sql import exists
from datetime import datetime
from data.connect import session
from sqlalchemy.orm import relationship,backref

def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer,primary_key=True,autoincrement=True)
    username = Column(String(20),unique=True,nullable=False)
    email = Column(String(80),unique=True,nullable=False)
    phone = Column(String(80),unique=True,nullable=False)
    password = Column(String(9999),nullable=False)
    info = Column(TEXT)
    face = Column(String(255),unique=True)
    uuid = Column(String(255),unique=True)
    creat_time = Column(DateTime,default=datetime.now())
    _locked = Column(Boolean,default=False,nullable=False)
    userlogs = relationship('Userlog',backref='user')

    def __repr__(self):
        return '<User #{}:{}>'.format(self.id, self.username)

    @classmethod
    def add_user(cls,name,email,phone,password,uuid):
        user = User(username=name,email=email,phone=phone,password=password,uuid=uuid)
        session.add(user)
        session.commit()

    @classmethod
    def updata_user(cls, uuid, username, email, phone, info, face):
        user = session.query(cls).filter_by(uuid=uuid).first()
        user.username = username
        user.email = email
        user.phone = phone
        user.info = info
        user.face = face
        session.commit()

    @classmethod
    def updata_pwd(cls, username, pwd):
        user = session.query(cls).filter_by(username=username).first()
        user.password = pwd
        session.commit()

    @classmethod
    def get_password(cls, username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            return user.password
        else:
            return ''

    @classmethod
    def is_exit_username(cls, username):
        return session.query(exists().where(User.username == username)).scalar()

    @classmethod
    def is_exit_email(cls, email):
        return session.query(exists().where(User.email == email)).scalar()

    @classmethod
    def is_exit_phone(cls, phone):
        return session.query(exists().where(User.phone == phone)).scalar()

    @classmethod
    def get_user_msg(cls,username):
        user = session.query(cls).filter_by(username=username).first()
        if user:
            return user
        else:
            return ''

    @classmethod
    def get_user_name(cls, user_id):
        user = session.query(cls).filter_by(id=user_id).first()
        if user:
            return user
        else:
            return ''

    @classmethod
    def UUID(cls, username):
        H_user = hashed(username)
        return H_user

    @classmethod
    def user_msg(cls, key=None):

        if key is None:
            page_data = session.query(User.id, User.username, User.email, User.phone, User.face, User._locked,
                                      User.creat_time).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(User.id, User.username, User.email, User.phone, User.face, User._locked,
                                      User.creat_time).filter(User.username.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def user_id_msg(cls,username):
        key = '%' + '%s' % (username) + '%'
        user_id = session.query(User.id).filter(User.username.like(key)).first()
        return user_id

    @classmethod
    def user_msg_data(cls, key=None):
        key = '%' + '%s' % (key) + '%'
        page_data = session.query(User.id, User.username, User.email, User.phone, User.face, User._locked,
                                      User.creat_time,User.uuid,User.info).filter(User.id.like(key)).all()
        print(page_data)
        return page_data


class Userlog(Base):
    __tablename__ = 'userlog'
    id = Column(Integer,primary_key=True,autoincrement=True)
    user_id = Column(Integer,ForeignKey('user.id'))
    ip = Column(String(100),unique=False,nullable=False)
    add_time = Column(DateTime,index=True,default=datetime.now())

    def __repr__(self):
        return '<User %r>'.format(self.id)

    @classmethod
    def add_userlog(cls, user_id, ip):
        userlog = Userlog(user_id=user_id, ip=ip)
        session.add(userlog)
        session.commit()

    @classmethod
    def userlog_msg(cls, key=None):
        if key is None:
            page_data = session.query(Userlog.id, Userlog.user_id, Userlog.ip, Userlog.add_time).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Userlog.id, Userlog.user_id, Userlog.ip, Userlog.add_time).filter(Userlog.user_id.like(key)).all()
        print(page_data)
        return page_data

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    addtime = Column(DateTime, index=True, default=datetime.now())  # 添加时间
    movies = relationship("Movie", backref='tag')

    def __repr__(self):
        return '<Tag %r>'.format(self.name)

    @classmethod
    def add_tag(cls, name):
        tag = Tag(name=name)
        session.add(tag)
        session.commit()

    @classmethod
    def is_exit_tagname(cls, name):
        return session.query(exists().where(Tag.name == name)).scalar()

    @classmethod
    def is_exit_tag_id(cls, id):
        return session.query(exists().where(Tag.id == id)).scalar()

    @classmethod
    def tag_msg(cls, key=None):
        if key is None:
            page_data = session.query(Tag.id, Tag.name, Tag.addtime).all()
        else:
            key = '%'+'%s'%(key)+'%'
            page_data =  session.query(Tag.id, Tag.name, Tag.addtime).filter(Tag.name.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def tag_id_name(cls, id):
        page_data = session.query(Tag.id, Tag.name, Tag.addtime).all()
        return page_data

    @classmethod
    def tag_list_id(cls, id=None):
        tag = session.query(cls).filter_by(id=id).first()
        session.delete(tag)
        session.commit()

    @classmethod
    def tag_movie(cls, key=None):
        movie_tag = session.query(Tag.id, Tag.name, Tag.addtime).all()
        return movie_tag

    @classmethod
    def get_tag_name(cls, tag_id):
        tag_name = session.query(Tag.name).filter_by(id=tag_id).first()
        if tag_name:
            print("tag_name_mo:",tag_name)
            return tag_name
        else:
            return ''



    @classmethod
    def tag_id(cls, key=None):
        list_dict = []
        if key is None:
            page_data = session.query(Tag.id).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Tag.id).filter(Tag.name.like(key)).all()
        print('tag_name:', page_data)
        for v in page_data:
            v_dict = v._asdict()
            list_dict.append(v_dict)
        id = list_dict[0]
        return id




# 电影
class Movie(Base):
    __tablename__ = "movie"
    id = Column(Integer, primary_key=True)  # 编号
    title = Column(String(255), unique=True)  # 标题
    url = Column(String(255), unique=True)  # 地址
    info = Column(TEXT)  # 简介
    logo = Column(String(255), unique=True)  # 封面
    star = Column(SmallInteger)  # 星级
    playnum = Column(BigInteger)  # 播放量
    commentnum = Column(BigInteger)  # 评论量
    tag_id = Column(Integer, ForeignKey('tag.id'))  # 所属标签
    area = Column(String(255))  # 上映地区
    release_time = Column(Date)  # 上映时间
    length = Column(String(100))  # 播放时间
    addtime = Column(DateTime, index=True, default=datetime.now())  # 添加时间
    comments = relationship("Comment", backref='movie')  # 评论外键关系关联
    moviecols = relationship("Moviecol", backref='movie')  # 收藏外键关系关联

    def __repr__(self):
        return "<Movie %r>".format(self.title)

    @classmethod
    def movie_updata(cls, title, url, info, logo, star, tag_id, area, length, release_time):
        movie_add = Movie(title=title, url=url, info=info, logo=logo, star=star, tag_id=tag_id, area=area, length=length, release_time=release_time)
        session.add(movie_add)
        session.commit()
        return {'msg': "OK"}

    @classmethod
    def movie_msg(cls, key=None):
        if key is None:
            page_data = session.query(Movie.id, Movie.title, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id, Movie.star, Movie.length, Movie.commentnum, Movie.playnum).all()
        else:
            key = '%' + '%s' % (key) + '%'
            print("key:",key)
            page_data = session.query(Movie.id, Movie.title, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id, Movie.star, Movie.length, Movie.commentnum, Movie.playnum).filter(Movie.tag_id.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def movie_star_msg(cls, key=None):
        if key is None:
            page_data = session.query(Movie.id, Movie.title, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id,
                                      Movie.star, Movie.length, Movie.commentnum, Movie.playnum).all()
        else:
            key = '%' + '%s' % (key) + '%'
            print("star_key:", key)
            page_data = session.query(Movie.id, Movie.title, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id,
                                      Movie.star, Movie.length, Movie.commentnum, Movie.playnum).filter(
                Movie.star.like(key)).all()
        print("star:", page_data)
        return page_data
    
    @classmethod
    def movie_play_msg(cls, key=None):
        if key is None:
            page_data = session.query(Movie.id, Movie.title, Movie.url, Movie.info, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id,
                                      Movie.star, Movie.length, Movie.commentnum, Movie.playnum).all()
        else:
            key = '%' + '%s' % (key) + '%'
            print("key:", key)
            page_data = session.query(Movie.id, Movie.title, Movie.url, Movie.info, Movie.release_time, Movie.area, Movie.logo, Movie.tag_id,
                                      Movie.star, Movie.length, Movie.commentnum, Movie.playnum).filter(Movie.id.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def is_exit_movie_id(cls, id):
        return session.query(exists().where(Movie.id == id)).scalar()

    @classmethod
    def movie_list_id(cls, id=None):
        movie = session.query(cls).filter_by(id=id).first()
        session.delete(movie)
        session.commit()

    @classmethod
    def updata_commentnum(cls, id, num):
        movie_c_num = session.query(cls).filter_by(id=id).first()
        print("movie_c_num",movie_c_num.commentnum)
        movie_c_num.commentnum = num
        session.commit()

    @classmethod
    def updata_playtnum(cls, id):
        movie_p_num = session.query(cls).filter_by(id=id).first()
        print("movie_p_num", movie_p_num.playnum)
        if movie_p_num.playnum:
            movie_p_num.playnum += 1
        else:
            movie_p_num.playnum = 1
        session.commit()



# 评论
class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)  # 编号
    content = Column(TEXT)  # 内容
    movie_id = Column(Integer, ForeignKey('movie.id'))  # 所属电影
    acticle_id = Column(Integer, ForeignKey('acticle.id'))  # 所属文章
    music_id = Column(Integer, ForeignKey('music.id'))  # 所属文章
    user_id = Column(Integer, ForeignKey('user.id'))  # 所属用户
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Comment %r>".format(self.id)

    @classmethod
    def comment_msg(cls, key=None):
        if key is None:
            page_data = session.query(Comment.id, Comment.content, Comment.movie_id, Comment.acticle_id, Comment.music_id, Comment.user_id, Comment.addtime).join(User,Movie).filter( Comment.movie_id==Movie.id , Comment.user_id==User.id ).all()
            print(page_data)
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Comment.id, Comment.content, Comment.movie_id, Comment.acticle_id, Comment.music_id, Comment.user_id, Comment.addtime).filter(Comment.movie_id.like(key)).all()
        print(page_data)
        #     page_data = session.query(Comment.id, Comment.content, Comment.movie_id, Comment.user_id,
        #                               Comment.addtime).join( User,Movie).filter(Comment.movie_id == Movie.id ,
        #                                                                         Comment.user_id == User.id ).all()
        #     print(page_data)
        return page_data

    @classmethod
    def comment_add(cls, comments, movie_id, user_id):
        comment_add = Comment(content=comments, movie_id=movie_id, user_id=user_id)
        session.add(comment_add)
        session.commit()




# 电影收藏
class Moviecol(Base):
    __tablename__ = "moviecol"
    id = Column(Integer, primary_key=True)  # 编号
    movie_id = Column(Integer, ForeignKey('movie.id'))  # 所属电影
    user_id = Column(Integer, ForeignKey('user.id'))  # 所属用户
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Moviecol %r>" .format(self.id)

# 上映预告
class Preview(Base):
    __tablename__ = "preview"
    id = Column(Integer, primary_key=True)  # 编号
    title = Column(String(255), unique=True)  # 标题
    logo = Column(String(255), unique=True)  # 封面
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Preview %r>" .format(self.title)

    @classmethod
    def is_exit_previewname(cls, title):
        return session.query(exists().where(Preview.title == title)).scalar()

    @classmethod
    def preview_updata(cls, title, logo):
        preview_add = Preview(title=title, logo=logo)
        session.add(preview_add)
        session.commit()

    @classmethod
    def is_exit_preview_id(cls, id):
        return session.query(exists().where(Preview.id == id)).scalar()

    @classmethod
    def preview_list_id(cls, id=None):
        preview = session.query(cls).filter_by(id=id).first()
        session.delete(preview)
        session.commit()

    @classmethod
    def preview_msg(cls, key=None):

        if key is None:
            page_data = session.query(Preview.id, Preview.title, Preview.logo, Preview.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Preview.id, Preview.title, Preview.logo, Preview.addtime).filter(Preview.title.like(key)).all()
        print(page_data)
        return page_data

# 权限
class Auth(Base):
    __tablename__ = "auth"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 名称
    url = Column(String(255), unique=True)  # 地址
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间

    def __repr__(self):
        return "<Auth %r>" % self.name

    @classmethod
    def is_exit_authname(cls, name):
        return session.query(exists().where(Auth.name == name)).scalar()

    @classmethod
    def is_exit_url(cls, url):
        return session.query(exists().where(Auth.url == url)).scalar()

    @classmethod
    def add_auth(cls, name, url):
        auth = Auth(name=name, url=url)
        session.add(auth)
        session.commit()

    @classmethod
    def auth_msg(cls, key=None):
        if key is None:
            page_data = session.query(Auth.id, Auth.name, Auth.url, Auth.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Auth.id, Auth.name, Auth.url, Auth.addtime).filter(Auth.name.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def auth_list(cls):
        auth_lists = session.query(Auth.id,Auth.name).all()
        return auth_lists

# 角色
class Role(Base):
    __tablename__ = "role"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 名称
    auths = Column(String(600))  # 角色权限列表
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间
    admins = relationship("Admin", backref='role')  # 管理员外键关系关联

    def __repr__(self):
        return "<Role %r>" % self.name

    @classmethod
    def is_exit_rolename(cls, name):
        return session.query(exists().where(Role.name == name)).scalar()

    @classmethod
    def add_role(cls, name,auths):
        role = Role(name=name,auths=auths)
        session.add(role)
        session.commit()

    @classmethod
    def role_msg(cls, key=None):
        if key is None:
            page_data = session.query(Role.id, Role.name, Role.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Role.id, Role.name, Role.addtime).filter(Role.name.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def role_list(cls):
        role_lists = session.query(Role.id, Role.name).all()
        return role_lists



class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)  # 编号
    name = Column(String(100), unique=True)  # 用户名
    pwd = Column(String(100))  # 密码
    is_super = Column(SmallInteger)#是否为超级管理员，0为超级管理员
    role_id = Column(Integer,ForeignKey('role.id'))#所属角色
    addtime = Column(DateTime, index=True, default=datetime.now)  # 添加时间
    adminlogs = relationship('Adminlog',backref='admin')
    oplogs = relationship('Oplog',backref='admin')

    def __repr__(self):
        return "<Admin %r>" .format(self.name)

    @classmethod
    def is_exit_adminname(cls, name):
        return session.query(exists().where(Admin.name == name)).scalar()

    @classmethod
    def is_exit_role_id(cls, role_id):
        return session.query(exists().where(Admin.role_id == role_id)).scalar()

    @classmethod
    def add_admin(cls, name, pwd, role_id):
        is_super = 1
        admin = Admin(name=name, pwd=pwd, role_id=role_id, is_super = is_super)
        session.add(admin)
        session.commit()

    @classmethod
    def add_admin_use(cls, name, pwd, role_id):
        is_super = 2
        admin = Admin(name=name, pwd=pwd, role_id=role_id, is_super=is_super)
        session.add(admin)
        session.commit()


    @classmethod
    def admin_msg(cls, key=None):
        if key is None:
            page_data = session.query(Admin).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Admin).filter(
                Admin.name.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def get_password(cls, username):
        user = session.query(cls).filter_by(name=username).first()
        print('admin_userpwd:',user)
        if user:
            return user.pwd
        else:
            return ''

    @classmethod
    def updata_pwd(cls, username, pwd):
        admin = session.query(cls).filter_by(name=username).first()
        admin.pwd = pwd
        print('admin.pwd:', admin.pwd)
        session.commit()


# 管理员登录日志
class Adminlog(Base):
    __tablename__ = "adminlog"
    id = Column(Integer, primary_key=True)  # 编号
    admin_id = Column(Integer, ForeignKey('admin.id'))  # 所属管理员
    ip = Column(String(100))  # 登录IP
    addtime = Column(DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Adminlog %r>" % self.id

    @classmethod
    def is_exit_previewname(cls, title):
        return session.query(exists().where(Preview.title == title)).scalar()

    @classmethod
    def preview_updata(cls, title, logo):
        preview_add = Preview(title=title, logo=logo)
        session.add(preview_add)
        session.commit()



# 操作日志
class Oplog(Base):
    __tablename__ = "oplog"
    id = Column(Integer, primary_key=True)  # 编号
    admin_id = Column(Integer, ForeignKey('admin.id'))  # 所属管理员
    ip = Column(String(100))  # 登录IP
    reason = Column(String(600))  # 操作原因
    addtime = Column(DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Oplog %r>" % self.id

# 文章
class Acticle(Base):
    __tablename__ = "acticle"
    id = Column(Integer, primary_key=True)  # 编号
    title = Column(String(255), unique=True)  # 标题
    info = Column(TEXT)  # 简介
    logo = Column(String(255), unique=True)  # 封面
    tag_id = Column(Integer, ForeignKey('acticle_tag.id'))  # 所属标签
    content = Column(TEXT)
    viwenum = Column(BigInteger)  # 点击量
    commentnum = Column(BigInteger)#评论量
    comments = relationship("Comment", backref='acticle')  # 评论外键关系关联
    addtime = Column(DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Acticle %r>" % self.id

    @classmethod
    def article_updata(cls, title, info, logo, tag_id, content ):
        article_add = Acticle(title=title, info=info, logo=logo, tag_id=tag_id, content=content)
        session.add(article_add)
        session.commit()

    @classmethod
    def article_msg(cls, key=None):
        if key is None:
            page_data = session.query(Acticle.id, Acticle.title, Acticle.info, Acticle.content, Acticle.logo, Acticle.tag_id, Acticle.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            print("key:", key)
            page_data = session.query(Acticle.id, Acticle.title, Acticle.info, Acticle.content, Acticle.logo, Acticle.tag_id, Acticle.addtime).filter(
                Acticle.tag_id.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def article_viwe_msg(cls, key=None):
        if key is None:
            page_data = session.query(Acticle.id, Acticle.title, Acticle.info, Acticle.tag_id, Acticle.content, Acticle.logo, Acticle.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            print("key:", key)
            page_data = session.query(Acticle.id, Acticle.title, Acticle.info, Acticle.tag_id, Acticle.content, Acticle.logo,Acticle.addtime).filter(Acticle.id.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def is_exit_article_id(cls, id):
        return session.query(exists().where(Acticle.id == id)).scalar()

    @classmethod
    def article_list_id(cls, id=None):
        article = session.query(cls).filter_by(id=id).first()
        session.delete(article)
        session.commit()

class Acticle_tag(Base):
    __tablename__ = 'acticle_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    addtime = Column(DateTime, index=True, default=datetime.now())  # 添加时间
    movies = relationship("Acticle", backref='acticle_tag')

    def __repr__(self):
        return "<Acticle_tag %r>" % self.id

    @classmethod
    def is_exit_tagname(cls, name):
        return session.query(exists().where(Acticle_tag.name == name)).scalar()

    @classmethod
    def add_tag(cls, name):
        tag = Acticle_tag(name=name)
        session.add(tag)
        session.commit()

    @classmethod
    def tag_msg(cls, key=None):
        if key is None:
            page_data = session.query(Acticle_tag.id, Acticle_tag.name, Acticle_tag.addtime).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Acticle_tag.id, Acticle_tag.name, Acticle_tag.addtime).filter(Acticle_tag.name.like(key)).all()
        print(page_data)
        return page_data

    @classmethod
    def is_exit_tag_id(cls, id):
        return session.query(exists().where(Acticle_tag.id == id)).scalar()

    @classmethod
    def tag_list_id(cls, id=None):
        tag = session.query(cls).filter_by(id=id).first()
        session.delete(tag)
        session.commit()

    @classmethod
    def tag_acticle(cls, key=None):
        acticle_tag = session.query(Acticle_tag.id, Acticle_tag.name, Acticle_tag.addtime).all()
        return acticle_tag

    @classmethod
    def tag_id(cls, key=None):
        list_dict = []
        if key is None:
            page_data = session.query(Acticle_tag.id).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Acticle_tag.id).filter(Acticle_tag.name.like(key)).all()
        print('tag_name:', page_data)
        for v in page_data:
            v_dict = v._asdict()
            list_dict.append(v_dict)
        id = list_dict[0]
        return id

    @classmethod
    def get_tag_name(cls, tag_id):
        tag_name = session.query(Acticle_tag.name).filter_by(id=tag_id).first()
        if tag_name:
            print("tag_name_mu:", tag_name)
            return tag_name
        else:
            return ''


# 音乐
class Music(Base):
    __tablename__ = "music"
    id = Column(Integer, primary_key=True)  # 编号
    title = Column(String(255), unique=True)  # 标题
    info = Column(TEXT)  # 简介
    logo = Column(String(255), unique=True)  # 封面
    tag_id = Column(Integer, ForeignKey('music_tag.id'))  # 所属标签
    content = Column(TEXT)
    viwenum = Column(BigInteger)  # 点击量
    commentnum = Column(BigInteger)#评论量
    comments = relationship("Comment", backref='music')  # 评论外键关系关联
    addtime = Column(DateTime, index=True, default=datetime.now)  # 登录时间

    def __repr__(self):
        return "<Music %r>" % self.id

class Music_tag(Base):
    __tablename__ = 'music_tag'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)
    addtime = Column(DateTime, index=True, default=datetime.now())  # 添加时间
    movies = relationship("Music", backref='music_tag')

    def __repr__(self):
        return "<Music_tag %r>" % self.id

    @classmethod
    def is_exit_tagname(cls, name):
        return session.query(exists().where(Music_tag.name == name)).scalar()

    @classmethod
    def add_tag(cls, name):
        tag = Music_tag(name=name)
        session.add(tag)
        session.commit()

    @classmethod
    def is_exit_tag_id(cls, id):
        return session.query(exists().where(Music_tag.id == id)).scalar()

    @classmethod
    def tag_list_id(cls, id=None):
        tag = session.query(cls).filter_by(id=id).first()
        session.delete(tag)
        session.commit()

    @classmethod
    def tag_music(cls, key=None):
        music_tag = session.query(Music_tag.id, Music_tag.name, Music_tag.addtime).all()
        return music_tag

    @classmethod
    def tag_id(cls, key=None):
        list_dict = []
        if key is None:
            page_data = session.query(Music_tag.id).all()
        else:
            key = '%' + '%s' % (key) + '%'
            page_data = session.query(Music_tag.id).filter(Music_tag.name.like(key)).all()
        print('tag_name:', page_data)
        for v in page_data:
            v_dict = v._asdict()
            list_dict.append(v_dict)
        id = list_dict[0]
        return id

    @classmethod
    def get_tag_name(cls, tag_id):
        tag_name = session.query(Music_tag.name).filter_by(id=tag_id).first()
        if tag_name:
            print("tag_name_mu:", tag_name)
            return tag_name
        else:
            return ''


if __name__ == '__main__':
    Base.metadata.create_all()
import hashlib
from data.user_module import User, Tag, Preview, Role, Auth, Admin, Movie, Acticle, Comment, Acticle_tag


def hashed(text):
    return hashlib.md5(text.encode('utf8')).hexdigest()


def authenticate(username, password):
    if username and password:
        is_match = hashed(password) == User.get_password(username)
        print("userpwd:", User.get_password(username))
        print("is_match:",is_match)
        return is_match
    else:
        return False


def authadminenticate(admin, password):
    if admin and password:
        is_match = hashed(password) == Admin.get_password(admin)
        print("is_match_admin:",hashed(password))
        print("is_match_adminpwd:", Admin.get_password(admin))
        return is_match
    else:
        return False

def regist(name, email, phone, password, uuid):
    role_id = 0
    if not User.is_exit_username(name):
        if not User.is_exit_email(email):
            if not User.is_exit_phone(phone):
                User.add_user(name, email, phone, hashed(password), uuid)
                Admin.add_admin_use(name, password, role_id)
                return {'msg': "OK"}
            else:
                return {'msg': "手机已经注册"}
        else:
            return {'msg': "邮箱已经注册"}
    else:
        return {'msg': "用户名重复"}


def regist_user(name, email, phone, info, face):
    if not User.is_exit_username(name):
        if not User.is_exit_email(email):
            if not User.is_exit_phone(phone):
                User.add_user(name, email, phone, info, face)
                return {'msg': "OK"}
            else:
                return {'msg': "手机已经注册"}
        else:
            return {'msg': "邮箱已经注册"}
    else:
        return {'msg': "用户名重复"}


def regist_tagname(name):
    if not Tag.is_exit_tagname(name):
        Tag.add_tag(name)
        return {'msg': "OK"}

    else:
        return {'msg': "标签重复"}

def regist_article_tagname(name):
    if not Acticle_tag.is_exit_tagname(name):
        Acticle_tag.add_tag(name)
        return {'msg': "OK"}
    else:
        return {'msg': "标签重复"}


def regist_tag_del(id):
    if Tag.is_exit_tag_id(id):
        Tag.tag_list_id(id)
        return {'msg': "OK"}

def regist_acticle_tag_del(id):
    if Acticle_tag.is_exit_tag_id(id):
        Acticle_tag.tag_list_id(id)
        return {'msg': "OK"}

def regist_preview(title, logo):
    if not  Preview.is_exit_previewname(title):
        Preview.preview_updata(title, logo)
        return {'msg': "OK"}
    else:
        return {'msg': "预告片重复"}

def regist_article(title, info, logo, tag_id, content):

    Acticle.article_updata(title, info, logo, tag_id, content)
    return {'msg': "OK"}


def regist_preview_del(id):
    if Preview.is_exit_preview_id(id):
        Preview.preview_list_id(id)
        return {'msg': "OK"}

def regist_movie_del(id):
    if Movie.is_exit_movie_id(id):
        Movie.movie_list_id(id)
        return {'msg': "OK"}


def regist_article_del(id):
    if Acticle.is_exit_article_id(id):
        Acticle.article_list_id(id)
        return {'msg': "OK"}

def regist_rolename(name,auths):
    if not Role.is_exit_rolename(name):
        Role.add_role(name,auths)
        return {'msg': "OK"}
    else:
        return {'msg': "角色重复"}

def regist_acount_pwd(user, oldpwd, newpwd, renewpwd):
    pwd = Admin.get_password(user)
    if hashed(oldpwd) == pwd:
        if newpwd == renewpwd:
            Admin.updata_pwd(user, newpwd)
            User.updata_pwd(user, newpwd)
            return {'msg': "OK"}
        else:
            return {'msg': "密码不一致"}
    else:
        return {'msg': "密码错误"}

def regist_authname(name, url):
    if not Auth.is_exit_authname(name):
        if not Auth.is_exit_url(url):
            Auth.add_auth(name, url)
            return {'msg': "OK"}
        else:
            return {'msg':'权限地址重复'}
    else:
        return {'msg': "权限重复"}

def regist_adminname(name, pwd, role_id, email, phone, uuid):
    if not Admin.is_exit_adminname(name) :
        if not User.is_exit_username(name):
            if not User.is_exit_phone(phone):
                Admin.add_admin(name, pwd, role_id)
                User.add_user(name, email, phone, pwd, uuid)
                return {'msg': "OK"}
            else:
                return {'msg': '手机号重复'}
        else:
            return {'msg':'用户名重复'}
    else:
        return {'msg': "管理员重复"}

def regist_comment(comment, movie_id, user_id):
    Comment.comment_add(comment, movie_id, user_id)
    return {'msg': "ok"}

def regist_userid(username):
    user_id = User.user_id_msg(username)
    return user_id


class Pageination:
    def __init__(self, current_page, all_itms):

        all_page, c = divmod(len(all_itms), 5)
        # print('数据长度', all_page, c)
        if c > 0:
            all_page += 1
        try:
            current_page = int(current_page)
        except:
            current_page = 1
        if  current_page < 1:
            current_page = 1
        self.current_page = current_page
        self.all_page = all_page

    @property
    def start(self):
        return (self.current_page - 1) * 5

    @property
    def end(self):
        return (self.current_page - 0) * 5

    def str_page(self, base_url, key):
        print(base_url)
        list_page = []
        if self.all_page < 5:
            s = 1
            e = self.all_page
        else:
            if self.current_page <= 3:
                s = 1
                e = 5
            else:
                if (self.current_page + 2) > self.all_page:
                    if self.current_page is not self.all_page:
                        s = self.current_page - 3
                        e = self.all_page
                    else:
                        s = self.current_page - 4
                        e = self.all_page
                else:
                    s = self.current_page - 2
                    e = self.current_page + 2

        first_page = '<li><a href="1?key=%s">首页</a></li>' % (key)
        list_page.append(first_page)
        if self.current_page == 1:
            prev_page = '<li><a href="javascript:viod(0)">上一页</a></li>'
        else:
            prev_page = '<li><a href="%s?key=%s">上一页</a></li>' % (self.current_page - 1, key)
        list_page.append(prev_page)
        for p in range(s, e + 1):
            if p == self.current_page:
                temp = '<li class="active"><a style=color:white href="%s?key=%s">%s</a></li>' % (p, key, p)
            else:
                temp = '<li><a href="%s?key=%s">%s</a></li>' % (p, key, p)
            list_page.append(temp)
        if self.current_page >= self.all_page:
            next_page = '<li><a href="javascript:viod(0)">下一页</a></li>'
        else:
            next_page = '<li><a href="%s?key=%s">下一页</a></li>' % (self.current_page + 1, key)
        list_page.append(next_page)

        last_page = '<li><a href="%s?key=%s">尾页</a></li>' % (self.all_page, key)
        list_page.append(last_page)
        jump = """<li><input class="input-sm" type="text"  placeholder="请输入页码">
                <a onclick="Jump('%s',this);"class= 'pull-right'>前往</a></li>""" % (base_url)
        script = """<script>
                            function Jump(base_url,ths){
                                var val = ths.previousElementSibling.value;
                                if(val.trim().length>0){
                                    location.href = base_url + val + "?"+ "key="+"%s";
                                }
                            }
                            </script>"""%(key)
        list_page.append(jump)
        list_page.append(script)
        return "".join(list_page)

    def str_page_play(self, base_url, key):
        print(base_url)
        list_page = []
        if self.all_page < 5:
            s = 1
            e = self.all_page
        else:
            if self.current_page <= 3:
                s = 1
                e = 5
            else:
                if (self.current_page + 2) > self.all_page:
                    if self.current_page is not self.all_page:
                        s = self.current_page - 3
                        e = self.all_page
                    else:
                        s = self.current_page - 4
                        e = self.all_page
                else:
                    s = self.current_page - 2
                    e = self.current_page + 2

        first_page = '<li><a href="%s&page=1&key=%s">首页</a></li>' % (base_url,key)
        list_page.append(first_page)
        if self.current_page == 1:
            prev_page = '<li><a href="javascript:viod(0)">上一页</a></li>'
        else:
            prev_page = '<li><a href="%s&page=%s&key=%s">上一页</a></li>' % (base_url,self.current_page - 1, key)
        list_page.append(prev_page)
        for p in range(s, e + 1):
            if p == self.current_page:
                temp = '<li class="active"><a style=color:white href="%s&page=%s&key=%s">%s</a></li>' % (base_url,p, key, p)
            else:
                temp = '<li><a href="%s&page=%s&key=%s">%s</a></li>' % (base_url,p, key, p)
            list_page.append(temp)
        if self.current_page >= self.all_page:
            next_page = '<li><a href="javascript:viod(0)">下一页</a></li>'
        else:
            next_page = '<li><a href="%s&page=%s&key=%s">下一页</a></li>' % (base_url,self.current_page + 1, key)
        list_page.append(next_page)

        last_page = '<li><a href="%s&page=%s&key=%s">尾页</a></li>' % (base_url,self.all_page, key)
        list_page.append(last_page)
        jump = """<li>
                <input class="input-sm" type="text" placeholder="请输入页码">
                <a onclick="Jump('%s',this);"class= 'pull-right'>前往</a></li>""" % (base_url)
        script = """<script>
                            function Jump(base_url,ths){
                                var val = ths.previousElementSibling.value;
                                if(val.trim().length>0){
                                    location.href = base_url + "&page=" + val + "&"+ "key="+"%s";
                                }
                            }
                            </script>"""%(key)
        list_page.append(jump)
        list_page.append(script)
        return "".join(list_page)
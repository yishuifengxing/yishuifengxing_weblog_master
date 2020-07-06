from wtforms.fields import SubmitField, StringField, SelectField
from wtforms.validators import DataRequired,Email,Regexp
from wtforms_tornado import Form
from data.user_module import Role

role_list = Role.role_list()
print(role_list)

class AdminForm(Form):
    """添加管理员表单"""
    name = StringField(
        label="管理员名称",
        validators=[
            DataRequired("请输入管理员名称！")
        ],
        description="管理员名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员名称！"
        }
    )
    email = StringField(
        label="邮箱",
        validators=[
            DataRequired("请输入邮箱！"),
            Email("邮箱格式不正确！")
        ],
        description="邮箱",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入邮箱！",
        }
    )
    phone = StringField(
        label="手机",
        validators=[
            DataRequired("请输入手机！"),
            Regexp("1[3458]\\d{9}", message="手机格式不正确！")
        ],
        description="手机",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入手机！",
        }
    )
    pwd = StringField(
        label="管理员密码",
        validators=[
            DataRequired("请输入管理员密码！")
        ],
        description="管理员密码",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员密码！"
        }
    )

    repwd = StringField(
        label="管理员重复密码",
        validators=[
            DataRequired("请输入管理员重复密码！")
        ],
        description="管理员重复密码",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入管理员重复密码！"
        }
    )

    role_id = SelectField(
        label="所属角色",
        coerce=int,
        choices=[(v.id, v.name) for v in role_list],
        description="所属角色",
        render_kw={
            "class": "form-control",
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )
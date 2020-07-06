from wtforms.fields import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form


class Acount_pwd_Form(Form):
    """修改密码表单"""
    oldpwd = StringField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入旧密码！"
        }
    )

    newpwd = StringField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入新密码！"
        }
    )

    renewpwd = StringField(
        label="重复新密码",
        validators=[
            DataRequired("请重复输入新密码！")
        ],
        description="重复新密码",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请重复输入新密码！"
        }
    )

    submit = SubmitField(
        '修改',
        render_kw={
            "class": "btn btn-primary",
        }
    )
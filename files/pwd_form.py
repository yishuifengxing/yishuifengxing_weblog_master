from wtforms.fields import SubmitField , PasswordField
from wtforms.validators import DataRequired, EqualTo
from wtforms_tornado import Form

class ModifypwdForm(Form):
    old_pwd = PasswordField(
        label="旧密码",
        validators=[
            DataRequired("请输入旧密码！")
        ],
        description="旧密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请旧输入密码！",
        }
    )
    new_pwd = PasswordField(
        label="新密码",
        validators=[
            DataRequired("请输入新密码！")
        ],
        description="新密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请新输入密码！",
        }
    )
    new_repwd = PasswordField(
        label="确认密码",
        validators=[
            DataRequired("请输入确认密码！"),
            EqualTo('new_pwd', message="两次密码不一致！")
        ],
        description="确认密码",
        render_kw={
            "class": "form-control input-lg",
            "placeholder": "请输入确认密码！",
        }
    )

    submit = SubmitField(
        '保存修改',
        render_kw={
            "class": "btn btn-lg btn-success btn-block",
        }
    )
from wtforms.fields import SubmitField ,StringField,PasswordField
from wtforms.validators import DataRequired,EqualTo,Email,Regexp,ValidationError
from wtforms_tornado import Form

class Account_LoginForm(Form):
    """管理员登录表单"""
    account = StringField(
        label="账号",
        validators=[
            DataRequired("请输入账号！")
        ],
        description="账号",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入账号！",
            # "required": "required"
        }
    )
    pwd = PasswordField(
        label="密码",
        validators=[
            DataRequired("请输入密码！")
        ],
        description="密码",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码！",
            # "required": "required"
        }
    )
    submit = SubmitField(
        '登录',
        render_kw={
            "class": "btn btn-primary btn-block btn-flat",
        }
    )

    # def validate_account(self, field):
    #     account = field.data
    #     admin = Admin.query.filter_by(name=account).count()
    #     if admin == 0:
    #         raise ValidationError("账号不存在！")
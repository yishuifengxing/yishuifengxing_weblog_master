from wtforms.fields import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form


class AuthForm(Form):
    """权限管理表单"""
    name = StringField(
        label="权限名称",
        validators=[
            DataRequired("请输入权限名称！")
        ],
        description="权限名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限名称！"
        }
    )

    url = StringField(
        label="权限地址",
        validators=[
            DataRequired("请输入权限地址！")
        ],
        description="权限地址",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入权限地址！"
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

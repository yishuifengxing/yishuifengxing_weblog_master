from wtforms.fields import SubmitField, StringField,SelectMultipleField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
from data.user_module import Auth

auth_list = Auth.auth_list()
print(auth_list)

class RoleForm(Form):
    """标签管理表单"""
    name = StringField(
        label="角色名称",
        validators=[
            DataRequired("请输入角色名称！")
        ],
        description="角色名称",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入角色名称！"
        }
    )
    auths_list = SelectMultipleField(
        label="权限列表",
        validators=[
            DataRequired("请选择权限列表！")
        ],
        coerce=int,
        choices=[(v.id,v.name) for v in auth_list],
        description="权限列表",
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

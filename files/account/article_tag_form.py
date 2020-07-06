from wtforms.fields import SubmitField, StringField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
class Article_Tag_Form(Form):
    """文章标签管理表单"""
    name = StringField(
        label="名称",
        validators=[
            DataRequired("请输入文章标签！")
        ],
        description="标签",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入文章标签名称！"
        }
    )

    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

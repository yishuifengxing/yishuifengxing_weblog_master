from wtforms.fields import SubmitField, StringField, FileField, TextAreaField,  SelectField
from wtforms.validators import DataRequired
from wtforms_tornado import Form
from data.user_module import Acticle_tag

class ArticleForm(Form):
    """文章管理表单"""
    title = StringField(
        label="标题",
        validators=[
            DataRequired("请输入预标题！")
        ],
        description="标题",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入标题！"
        }
    )
    info = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    logo = FileField(
        label="封面",
        validators=[
        ],
        description="封面",
    )
    tag_id = SelectField(
        label="标签",
        validators=[
            DataRequired("请选择标签！")
        ],
        coerce=int,
        choices=[(v.id, v.name) for v in Acticle_tag.tag_acticle()],
        description="标签",
        render_kw={
            "class": "form-control",
        }
    )

    artic = TextAreaField(
        label="内容",
        validators=[
            DataRequired("请输入文章")
        ],
        description="内容",
        render_kw={
            "id" : "input_content",
        }
    )

    submit = SubmitField(
        '编辑',
        render_kw={
            "class": "btn btn-success pull-left",


        }
    )
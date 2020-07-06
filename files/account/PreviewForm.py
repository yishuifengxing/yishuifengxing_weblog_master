from wtforms.fields import SubmitField, StringField, FileField
from wtforms.validators import DataRequired
from wtforms_tornado import Form


class PreviewForm(Form):
    """标签管理表单"""
    title = StringField(
        label="预告标题",
        validators=[
            DataRequired("请输入预告片片名！")
        ],
        description="片名",
        render_kw={
            "class": "form-control",
            "id": "input_name",
            "placeholder": "请输入预告片片名！"
        }
    )
    logo = FileField(
        label="预告封面",
        validators=[
        ],
        description="封面",
    )
    submit = SubmitField(
        '添加',
        render_kw={
            "class": "btn btn-primary",
        }
    )

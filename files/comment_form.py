from wtforms.fields import SubmitField, TextAreaField
from wtforms.validators import DataRequired,Email,Regexp
from wtforms_tornado import Form

class CommentForm(Form):
    comment = TextAreaField(
        label="简介",
        validators=[
            DataRequired("请输入简介")
        ],
        description="简介",
        render_kw={
            "id" : "input_content",
        }
    )
    submit = SubmitField(
        '提交评论',
        render_kw={
            "id":"btn-sub",
            "class": "btn btn-success pull-left",
            "class": "glyphicon glyphicon-heart",
        }
    )
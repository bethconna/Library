#! -*- coding:utf-8 -*-
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    # validator 验证器
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField(validators=[DataRequired(), Length(min=2, max=20, message='收件人姓名长度必须在2-20个字符之间')])
    mobile = StringField('手机号', validators=[DataRequired(), Regexp('^1[0-9]{10}$', message='请输入正确的手机号')])
    message = StringField('留言')
    address = StringField('邮寄地址', validators=[DataRequired(), Length(min=10, max=70, message='地址还不到10个字吗？尽量写详细一些吧')])

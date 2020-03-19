#! -*- coding:utf-8 -*-
from wtforms import Form, StringField, IntegerField, PasswordField
from wtforms.validators import Length, NumberRange, DataRequired, Email, ValidationError, EqualTo
from app.models.user import User


class EmailForm(Form):
    # validator 验证器
    email = StringField(validators=[DataRequired(message='邮箱不可以为空'),
                                    Length(8, 64, message='邮箱长度在8-64之间'), Email(message='电子邮箱不符合规范')])


class LoginForm(EmailForm):
    password = PasswordField(validators=[DataRequired(message='密码不可以为空'), Length(6, 32, message='密码长度在6-32之间')])


class RegisterForm(LoginForm):
    nickname = StringField(validators=[DataRequired(message='昵称不可以为空'), Length(2, 10, message='昵称长度在2-10之间')])

    # 业务逻辑：判断email字段注册是否唯一
    # wtforms自定义校验函数命名格式：validate_xxx
    def validate_email(self, field):
        # db.session
        # query.filter_by(一组查询条件)
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('电子邮件已被注册')

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError('昵称已被注册')


class ResetPasswordForm(Form):
    password1 = PasswordField(validators=[DataRequired(), Length(6, 32, message='密码长度在6-32之间'),
                              EqualTo('password2', message='两次输入的密码不相同')])
    password2 = PasswordField(validators=[DataRequired(), Length(6, 32)])


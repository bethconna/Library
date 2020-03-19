from flask import render_template, request, redirect, url_for, flash
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.base import db
from app.models.user import User
from app.web.blueprint import web
from flask_login import login_user, logout_user


@web.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            # orm思想：数据库操作
            db.session.add(user)
        # 重定向跳转页面：flask.redirect
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next = request.args.get('next')
            # 1、防止next为空 2、防止重定向攻击
            if not next or not next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash('账号不存在或密码错误')
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    if request.method == 'POST':
        form = EmailForm(request.form)
        if form.validate():
            account_email = form.email.data
            # first_or_404-->HTTPException（code:404）
            user = User.query.filter_by(email=account_email).first_or_404()
            # 密码重置
            from app.libs.email import send_mail
            send_mail(form.email.data, '重置密码', 'email/reset_password.html', user=user, token=user.generate_token())
            flash('重置密码邮件已经发送至你的邮箱，请查收')
    return render_template('auth/forget_password_request.html', form=form)


@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        res = User.reset_password(token, form.password1.data)
        if res:
            flash('密码重置成功，将自动跳转登录页面')
            return redirect(url_for('web.login'))
        else:
            flash('密码重置失败')
    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
def change_password():
    return '更改密码'


@web.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('web.index'))

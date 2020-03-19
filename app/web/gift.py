from flask import render_template, current_app, flash, redirect, url_for
from app.libs.enums import PendingStatus
from app.models.base import db
from app.models.drift import Drift
from app.models.gift import Gift
from app.view_models.trade import MyTrades
from app.web.blueprint import web
from flask_login import login_required, current_user


@web.route('/my/gifts')
@login_required    # flask_login装饰器：权限控制
def my_gifts():
    uid = current_user.id
    gifts_of_mine = Gift.get_user_gifts(uid)
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    wish_count_list = Gift.get_wish_counts(isbn_list)
    view_model = MyTrades(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=view_model.trades)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)
    else:
        flash('这本书已经添加至你的心愿清单或赠送清单了，请不要重复添加')
    # redirect可以使用AJAX技术
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
@login_required
def redraw_from_gifts(gid):
    gift = Gift.query.filter_by(id=gid, uid=current_user.id, launched=False).first_or_404()
    drift = Drift.query.filter_by(gift_id=gid, pending=PendingStatus.Waiting).first()
    if drift:
        flash('这个礼物正处于交易状态，请先处理鱼漂')
    else:
        with db.auto_commit():
            gift.delete()
            current_user.beans -= current_app.config['BEANS_UPLOAD_ONE_BOOK']
    return redirect(url_for('web.my_gifts'))




from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from app.libs.email import send_mail
from app.models.base import db
from app.models.gift import Gift
from app.models.wish import Wish
from app.view_models.trade import MyTrades
from app.web.blueprint import web


@web.route('/my/wish')
@login_required     # flask_login装饰器：权限控制(user.loader与login_required)
def my_wish():
    uid = current_user.id
    wishes_of_mine = Wish.get_user_wishes(uid)
    isbn_list = [gift.isbn for gift in wishes_of_mine]
    gift_count_list = Wish.get_gift_counts(isbn_list)
    view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.isbn = isbn
            wish.uid = current_user.id
            db.session.add(wish)
    else:
        flash('这本书已经添加至你的心愿清单或赠送清单了，请不要重复添加')
    # redirect可以使用AJAX技术
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
@login_required
def satisfy_wish(wid):
    wish = Wish.query.get_or_404(wid)
    gift = Gift.query.filter_by(uid=current_user.id, isbn=wish.isbn).first()
    if not gift:
        flash('你还没有上传此书，请先添加此书哦')
    else:
        # send_mail(wish.user.email, '赠送书籍', 'email/satisfy_wish.html', wish=wish, gift=gift)
        flash('我们已经发送给该心愿者一封邮件，如果他/她愿意接受你的赠送，你将收到一个鱼漂')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(isbn=isbn, uid=current_user.id, launched=False).first_or_404()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))

from flask import Flask, flash, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from sqlalchemy import ForeignKey

from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
app = Flask(__name__)
app.secret_key = os.getenv("MYKEY")
bstrap = Bootstrap5(app)

log_manager = LoginManager()
log_manager.init_app(app)


#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project1.db'
db.init_app(app)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class User(UserMixin, db.Model):
    __tablename__ = 'users_table'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    pw: Mapped[str] = mapped_column()
    #Parent
    comment_chld: Mapped[List["CommentsTable"]] = relationship(back_populates='user_map')

class CommentsTable(db.Model):
    __tablename__ = "comments_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(nullable=False)

    #child
    user_id: Mapped[int] = mapped_column(ForeignKey('users_table.id'))
    user_map: Mapped['User'] = relationship(back_populates='comment_chld')

with app.app_context():
    db.create_all()
    
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class LogForm(FlaskForm):
    email = EmailField('', validators=[DataRequired()])
    pw_form = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Submit')
    
class RegForm(FlaskForm):
    name = StringField('', validators=[DataRequired()])
    email = EmailField('', validators=[DataRequired()])
    pw_form = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Submit')

class CommentForm(FlaskForm):
    comment = StringField('', validators=[DataRequired()])
    submit = SubmitField('Comment')
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
from functools import wraps

def admin_only_dec(func):
    @wraps(func)
    def decorated_func(*args, **kwargs):
        if current_user.is_anonymous:
            return abort(406, "Not Acceptable, This mean you are just an anonymous.\nGo away.")

        return func(*args, **kwargs)
    return decorated_func

#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

@app.route('/', methods=['GET', 'POST'])
def log_page():
    form = LogForm()
    if form.validate_on_submit():
        user_exist = db.session.execute(db.select(User).where(User.email == form.email.data)).scalar()
        if user_exist:
            if check_password_hash(user_exist.pw, form.pw_form.data):
                login_user(user_exist)
                return redirect(url_for('main_page'))
            else:
                flash('Invalid Password')
                return redirect(url_for('log_page'))
        else:
            flash("This email doesn't exist!\nYou have to Register instead.")
            return redirect(url_for('log_page'))
    return render_template('login.html', form=form, current_user=current_user)
    
@app.route('/reg', methods=['GET', 'POST'])
def reg_page():
    form = RegForm()
    if form.validate_on_submit():
        salted_pw = generate_password_hash(form.pw_form.data,
                                       method='pbkdf2:sha256:600000',
                                       salt_length=8)
        new_user = User()
        new_user.name = form.name.data
        new_user.email = form.email.data
        new_user.pw = salted_pw

        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('log_page'))
    return render_template('reg.html', form=form, current_user=current_user)


@app.route('/main', methods=['POST', 'GET'])
@login_required
def main_page():
    all_comments = db.session.execute(db.select(CommentsTable).order_by(CommentsTable.id)).scalars().all()
    form = CommentForm()
    if form.validate_on_submit():
        new_cmnt = CommentsTable()
        new_cmnt.comment_text = form.comment.data
        new_cmnt.user_map = current_user
    
        db.session.add(new_cmnt)
        db.session.commit()
        return redirect(url_for('main_page'))
    return render_template('index.html', form=form, current_user=current_user, all_comments=all_comments)


@app.route('/out')
def logout():
    logout_user()
    return redirect(url_for('log_page'))

app.run(debug=True)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

































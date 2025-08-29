from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
app = Flask(__name__)
bstrap = Bootstrap5(app)

#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project1.db'
db.init_app(app)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class User(db.Model):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    pw: Mapped[str] = mapped_column()
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
    submit = SubmitField('submit')

#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
@app.route('/', methods=['GET', 'POST'])
def log_page():
    form = LogForm()
    return render_template('login.html', form=form)
    
@app.route('/reg', methods=['GET', 'POST'])
def reg_page():
    form = RegForm()
    return render_template('reg.html', form=form)


@app.route('/main')
def main_page():
    form = CommentForm()
    return render_template('index.html', form=form)




app.run(debug=True)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

























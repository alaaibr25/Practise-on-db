from flask import Flask, render_template, url_for, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from flask_bootstrap import Bootstrap5
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
app = Flask(__name__)
bstrap = Bootstrap5(app)


#◻🔘◻**********************◻🔘◻**********************◻🔘◻#

class LogForm(FlaskForm):
    email = EmailField('', validators=[DataRequired()])
    pw_form = PasswordField('', validators=[DataRequired()])
    submit = SubmitField('Submit')



#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
@app.route('/', methods=['GET', 'POST'])
def log_page():
    form = LogForm()
    return render_template('login.html', form=form)

@app.route('/main')
def main_page():
    return render_template('index.html')




app.run(debug=True)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#























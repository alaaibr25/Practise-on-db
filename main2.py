from flask import Flask, render_template, url_for, redirect
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
app = Flask(__name__)



#◻🔘◻**********************◻🔘◻**********************◻🔘◻#





#◻🔘◻**********************◻🔘◻**********************◻🔘◻#
@app.route('/')
def log_page():
    return render_template('login.html')

@app.route('/main')
def main_page():
    return render_template('index.html')




app.run(debug=True)
#◻🔘◻**********************◻🔘◻**********************◻🔘◻#






















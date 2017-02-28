from flask import Flask, render_template, session, redirect, url_for, request
from models import db, Drivers
import sys

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'
# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://group15.2016:K7fb7BpAn5Tk@csmysql.cs.cf.ac.uk/group15_2016'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

@app.route("/")
def index():
    if 'username' in session:
        driver_username = session['username']
        driver_info = Drivers.query.filter_by(username=driver_username)
        return render_template('index.html', u=driver_username)
    else:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        request_username = request.form['username']
        request_password = request.form['password']
        results = Drivers.query.filter_by(username=request_username).filter_by(password=request_password).first()
        # Check if driver exists
        if(results is not None):
            session['username'] = results.username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

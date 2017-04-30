from flask import Flask, render_template, session, redirect, url_for, request, json
from models import db, Drivers, Client
from classes.driver import Driver
import sys
from Calculations import *

app = Flask(__name__)

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'
# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://group15.2016:K7fb7BpAn5Tk@csmysql.cs.cf.ac.uk/group15_2016'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
calculation = Calculations()

@app.route("/")
def index():
    if 'username' in session:
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)
        if(len(driver_stats.routes) == 0):
            return render_template('index.html', map_route=0, average_speed=1, average_break_count=1, average_time=1)
        the_map_route = driver_stats.routes[0].GetID()
        the_average_speed = calculation.rateAverageSpeed(driver_stats.GetAllRoutes()) / 100
        the_average_break_count = calculation.rateBreaksTaken(driver_stats.GetAllRoutes()) / 100
        the_average_time = calculation.rateTimeOfDriving(driver_stats.GetAllRoutes()) / 100
        the_average_acceleration = calculation.rateAcceleration(driver_stats.GetAllRoutes()) / 100
        the_average_braking = calculation.rateBraking(driver_stats.GetAllRoutes()) / 100
        return render_template('index.html', map_route=driver_stats.routes[0].GetID(), average_speed=the_average_speed, average_break_count=the_average_break_count, average_time=the_average_time, average_acceleration=the_average_acceleration, average_braking=the_average_braking)
    else:
        return redirect(url_for('login'))

@app.route("/journeys", methods=['GET'])
def journeys():
    if 'username' in session:
        request_route = request.args.get('r')
        if(request_route == "0"):
            return render_template('journeys.html', routes=[], coordinates={}, origin={}, map_route=0)
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)
        route_coordinates = driver_stats.GetRouteById(request_route).GetRoutePath()
        origin = json.dumps(route_coordinates[0]).replace("\"", "")
        route_coordinates = json.dumps(route_coordinates).replace("\"", "")
        routes = []
        for route in driver_stats.GetAllRoutes():
            route_info = {}
            startTime = route.GetStartTime()
            duration = route.GetDuration()
            startPosition = route.GetStartPosition()
            endPosition = route.GetEndPosition()
            route_info['id'] = route.GetID()
            route_info['time'] = startTime
            route_info['duration'] = duration
            route_info['start'] = startPosition
            route_info['end'] = endPosition
            routes.append(route_info)
        return render_template('journeys.html', routes=routes, coordinates=route_coordinates, origin=origin, map_route=int(request_route))
    else:
        return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    if 'username' in session:
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)
        if(len(driver_stats.routes) == 0):
            return render_template('account.html', map_route=0, first_name=driver_information.GetForename(), last_name=driver_information.GetSurname(), username=driver_username, email=driver_information.GetEmailAddress(), insurance="")
        client_id = driver_information.GetClientID()
        client_information = Client.query.filter_by(Client_ID=client_id).first()
        the_map_route = driver_stats.routes[0].GetID()
        if request.method == 'POST':
            current_password = request.form['current']
            new_password = request.form['new']
            new_password_verify = request.form['renew']
            if(driver_information.CheckPassword(current_password) and new_password == new_password_verify):
                driver_information.ChangePassword(new_password)
                db.session.commit()
                session.pop('username', None)
                return redirect(url_for('index'))
            else:
                return render_template('account.html', map_route=the_map_route, first_name=driver_information.GetForename(), last_name=driver_information.GetSurname(), username=driver_username, email=driver_information.GetEmailAddress(), insurance=client_information.GetClientName())
        else:
            return render_template('account.html', map_route=the_map_route, first_name=driver_information.GetForename(), last_name=driver_information.GetSurname(), username=driver_username, email=driver_information.GetEmailAddress(), insurance=client_information.GetClientName())
    else:
        return redirect(url_for('login'))

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['Firstname']
        last_name = request.form['Lastname']
        username = request.form['Username']
        password = request.form['Password']
        email = request.form['Email']
        driver = Drivers(first_name, last_name, username, password, email)
        db.session.add(driver)
        db.session.commit()
        session['username'] = username
        return redirect(url_for('index'))
    else:
        return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'username' in session:
        return redirect(url_for('index'))
    else:
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

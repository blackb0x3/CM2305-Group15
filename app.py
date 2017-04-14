from flask import Flask, render_template, session, redirect, url_for, request, json
from models import db, Drivers
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
        the_map_route = driver_stats.routes[0].GetID()
        the_average_speed = calculation.rateAverageSpeed(driver_stats.GetAllRoutes()) / 100
        the_average_break_count = calculation.rateBreaksTaken(driver_stats.GetAllRoutes()) / 100
        the_average_time = calculation.rateTimeOfDriving(driver_stats.GetAllRoutes()) / 100
        return render_template('index.html', map_route=driver_stats.routes[0].GetID(), average_speed=the_average_speed, average_break_count=the_average_break_count, average_time=the_average_time)
    else:
        return redirect(url_for('login'))

@app.route("/journeys", methods=['GET'])
def journeys():
    if 'username' in session:
        request_route = request.args.get('r')
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
    app.run(debug=False)

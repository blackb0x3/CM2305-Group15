from flask import Flask, render_template, session, redirect, url_for, request, json
from models import db, Drivers, Client
from classes.driver import Driver
import sys
from Calculations import *

app = Flask(__name__)

# Used in order to start and end user sessions
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RS'

# MySQL configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://group15.2016:K7fb7BpAn5Tk@csmysql.cs.cf.ac.uk/group15_2016'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
calculation = Calculations()

@app.route("/")
def index():
    """
    Processes driver routes into relevant statistics, displayed on the index.hmtl page.
    :return: index.html, where each score is determined by the results of the rating methods in the Calculations class
    """
    if 'username' in session:
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)

        # Returns a blank set of scores if there is no driver data
        if(len(driver_stats.routes) == 0):
            return render_template('index.html', map_route=0, average_speed=1, average_break_count=1, average_time=1)

        # The scores for the various driving habits
        # (e.g. time of day driving, average speed, breaks taken on long journeys)
        the_map_route = driver_stats.routes[0].GetID()
        the_average_speed = calculation.rateAverageSpeed(driver_stats.GetAllRoutes()) / 100
        the_average_break_count = calculation.rateBreaksTaken(driver_stats.GetAllRoutes()) / 100
        the_average_time = calculation.rateTimeOfDriving(driver_stats.GetAllRoutes()) / 100
        the_average_acceleration = calculation.rateAcceleration(driver_stats.GetAllRoutes()) / 100
        the_average_braking = calculation.rateBraking(driver_stats.GetAllRoutes()) / 100

        # render_template() returns the HTML page for the specified link, optional arguments are included to link the
        # scores to their respective graphs
        return render_template('index.html',
                               map_route=the_map_route,
                               average_speed=the_average_speed,
                               average_break_count=the_average_break_count,
                               average_time=the_average_time,
                               average_acceleration=the_average_acceleration,
                               average_braking=the_average_braking)
    else:
        # Differentiates between portals for insurer and regular driver
        if 'admin' in session:
            return redirect(url_for('admin'))
        else:
            return redirect(url_for('login'))

@app.route("/journeys", methods=['GET'])
def journeys():
    """
    Gets the journeys for the driver currently logged in.
    :return: journeys.html, where the current journey displayed is the first journey in the list of journeys
    """
    # If driver is logged in, retrieve driver journeys
    if 'username' in session:
        request_route = request.args.get('r')

        # If a driver doesn't have any routes, send an empty list of routes by default
        if(request_route == "0"):
            return render_template('journeys.html',
                                   routes=[],
                                   coordinates={},
                                   origin={},
                                   map_route=0)

        # Get driver information, via their username
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)

        # Get routes for the driver logged in
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

        return render_template('journeys.html',
                               routes=routes,
                               coordinates=route_coordinates,
                               origin=origin,
                               map_route=int(request_route))
    else:
        return redirect(url_for('login'))

@app.route("/account", methods=['GET', 'POST'])
def account():
    """
    Displays the driver's details regarding their account, and allows the driver to change their password.
    :return: account.html, with the driver's details filled in the text boxes.
    """
    if 'username' in session:
        # Get driver from database.
        driver_username = session['username']
        driver_information = Drivers.query.filter_by(username=driver_username).first()
        driver_stats = Driver(driver_information)

        # map_route is 0 to prevent app from crashing with 0 routes (see journey() method)
        if(len(driver_stats.routes) == 0):
            return render_template('account.html',
                                   map_route=0,
                                   first_name=driver_information.GetForename(),
                                   last_name=driver_information.GetSurname(),
                                   username=driver_username,
                                   email=driver_information.GetEmailAddress(),
                                   insurance="")

        # Get information about driver's insurer
        client_id = driver_information.GetClientID()
        client_information = Client.query.filter_by(Client_ID=client_id).first()
        the_map_route = driver_stats.routes[0].GetID()

        # If the driver changed their password, get the current, new and confirmed new password
        if request.method == 'POST':
            current_password = request.form['current']
            new_password = request.form['new']
            new_password_verify = request.form['renew']

            # If the driver entered their current password correctly, and verified the new password, change it
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
    """
    Displays the registration page for new drivers.
    :return: index.html upon successful registration, otherwise, register.html - with an error message if the password 
    cannot be confirmed by the new driver.
    """
    # If the form was submitted, add the new driver to the database
    if request.method == 'POST': # POST requests used due to sending sensitive data across the network to the database.
        first_name = request.form['Firstname']
        last_name = request.form['Lastname']
        username = request.form['Username']
        password = request.form['Password']
        repassword = request.form['RePassword']
        email = request.form['Email']
        client_id = request.form['inputIRC'] # Not sure why insurer referral code cannot be added...?

        # If the new driver's password cannot be verified, then output an error, saying the driver hasn't confirmed
        # their password correctly
        if password != repassword:
            return render_template('register.html', noMatchingPasswords=True)

        # Add the new driver to the database
        else:
            driver = Drivers(first_name, last_name, username, password, email)
            db.session.add(driver)
            db.session.commit()
            session['username'] = username
            return redirect(url_for('index'))

    # Otherwise, just reload the page, with no error messages
    else:
        return render_template('register.html', noMatchingPasswords=False)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    The login method for the driver.
    :return: index.html upon successful login, login.html if unsuccessful
    """
    # Send to the home page if already logged in
    if 'username' in session:
        return redirect(url_for('index'))

    # Add new session and send user to the home page upon successful login
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

@app.route('/admin/login', methods=['POST'])
def admin_login():
    """
    The login method for the insurer.
    :return: admin.html upon successful login, login.html if unsuccessful
    """
    # Redirect the insurer to the admin page if they're already logged in
    if 'admin' in session:
        return redirect(url_for('admin'))

    # Send the insurer to the admin page upon successful login, otherwise, reload the login page
    else:
        request_username = request.form['username']
        request_password = request.form['password']
        results = Client.query.filter_by(Client_Number=request_username).filter_by(Password=request_password).first()
        if(results is not None):
            session['admin'] = results.Client_Number
            return redirect(url_for('admin'))
        else:
            return render_template('login.html', error=True)

@app.route('/admin', methods=['GET'])
def admin():
    """
    The home page for the car insurer.
    :return: admin.html if the insurer is logged in - containing all drivers insured with them.
    Otherwise, send the insurer to the login page.
    """
    if 'admin' in session:
        # Collects drivers associated with the insurer currently logged into the system.
        client_number = session['admin']
        client_information = Client.query.filter_by(Client_Number=client_number).first()
        client_drivers = Drivers.query.filter_by(Client_ID=client_information.Client_ID).all()
        return render_template('admin.html', drivers=client_drivers, client=client_information.Client_Name)

    else:
        return render_template('login.html', error=False)

@app.route('/admin/journeys', methods=['GET'])
def admin_journeys():
    """
    Gets the routes for an associated driver - selected by the insurer via the application.
    :return: The HTML document (admin-journeys.html) that displays routes for a selected driver.
    """
    if 'admin' in session:
        # Gets selected driver from database.
        client_number = session['admin']
        client_information = Client.query.filter_by(Client_Number=client_number).first()
        request_driver = request.args.get('u')
        request_route = request.args.get('r')
        driver_information = Drivers.query.filter_by(Client_ID=client_information.Client_ID,
                                                     Driver_ID=request_driver).first()
        driver_stats = Driver(driver_information)

        # If the selected driver doesn't have any routes, send a blank HTML document
        if(len(driver_stats.routes) == 0):
            return ('', 204)

        # Get the first route in the list of driver's routes
        if request_route == '0':
            request_route = driver_stats.routes[0].GetID()

        # Get the selected driver's routes, and return the HTML document which allows the insurer to select a route,
        # without refreshing the page
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
        return render_template('admin-journeys.html',
                               routes=routes,
                               coordinates=route_coordinates,
                               origin=origin,
                               map_route=int(request_route),
                               user=request_driver)
    else:
        return render_template('login.html', error=False)

@app.route('/admin/scores', methods=['GET'])
def admin_scores():
    """
    Gets the scores for a driver selected by the insurer.
    :return: The HTML document detailing the scores for each driving rating - for a selected driver. 
    """
    if 'admin' in session:
        # Get insurer's session data - to get the drivers they insure
        client_number = session['admin']
        client_information = Client.query.filter_by(Client_Number=client_number).first()

        # Get selected driver routes and statistics
        request_driver = request.args.get('u')
        driver_information = Drivers.query.filter_by(Client_ID=client_information.Client_ID,
                                                     Driver_ID=request_driver).first()
        driver_stats = Driver(driver_information)

        # Returns good statistics by default if driver's telematics has not yet recorded data
        if(len(driver_stats.routes) == 0):
            return render_template('admin-scores.html',
                                   average_speed=1,
                                   average_break_count=1,
                                   average_time=1,
                                   average_acceleration=1,
                                   average_braking=1)

        # Calculate ratings if there is data to be evaluated
        the_average_speed = calculation.rateAverageSpeed(driver_stats.GetAllRoutes()) / 100
        the_average_break_count = calculation.rateBreaksTaken(driver_stats.GetAllRoutes()) / 100
        the_average_time = calculation.rateTimeOfDriving(driver_stats.GetAllRoutes()) / 100
        the_average_acceleration = calculation.rateAcceleration(driver_stats.GetAllRoutes()) / 100
        the_average_braking = calculation.rateBraking(driver_stats.GetAllRoutes()) / 100
        return render_template('admin-scores.html',
                               average_speed=the_average_speed,
                               average_break_count=the_average_break_count,
                               average_time=the_average_time,
                               average_acceleration=the_average_acceleration,
                               average_braking=the_average_braking)
    else:
        return render_template('login.html', error=False)

@app.route('/admin/logout')
def admin_logout():
    """
    Logs the insurer out of the system if they are already logged in.
    :return: The login page (login.html)
    """
    # remove the username from the session if it's there
    session.pop('admin', None)
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    """
    Logs the driver out of the system if they are already logged in.
    :return: The login page (login.html)
    """
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)

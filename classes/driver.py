from classes.user import User
from classes.profile import Profile
from classes.route import Route
from models import Journey
from Calculations import Calculations

class Driver:
    def __init__(self, driver_information):
        # Do Not Move or Reorder
        self.routes = []
        self.calculation = Calculations()
        self.information = driver_information
        self.PopulateRoutes()
        self.averageWeeklyJourneys = self.UpdateWeeklyJourneys()
        self.averageBreaks = self.UpdateAverageBreaks()
        self.profile = Profile(driver_information)
        self.estimatedInsurance = self.CalculateInsurance()

    # If you're wondering why there's no user functions from the class diagram, see User

    def PopulateRoutes(self):
        """
        Retrieves and stores the driver's journeys retrieved from the database.
        :return: Nothing.
        """
        results = Journey.query.filter_by(Driver_ID=self.information.GetID()).all()
        for route in results:
            new_route = Route(route.Route_ID)
            self.AddRoute(new_route)

    def CalculateInsurance(self):
        pass

    def GetProfile(self):
        """
        Gets the driver's profile which stores their scores.
        :return: The driver's profile.
        """
        return self.profile

    def GetInsurance(self):
        """
        Should get the estimated insurance for a driver.
        :return: The estimated insurance for a driver.
        """
        return None

    def GetWeeklyJourneys(self):
        """
        Should get the weekly journeys made by a driver.
        Unable to use this function since our data doesn't contain dates, only times.
        :return: The number of journeys made on average per week.
        """
        return self.averageWeeklyJourneys

    def GetAverageNumberOfBreaks(self):
        """
        Should get the average number of breaks over the driver's routes.
        :return: THe average break count across all routes.
        """
        return self.averageBreaks

    def GetAllRoutes(self):
        """
        Gets all the routes for a particular driver.
        :return: The driver's routes.
        """
        return self.routes

    def GetRouteById(self, route_id):
        """
        Gets a route with a particular ID.
        :param route_id: The ID to search for.
        :return: The route with the specified ID, or None if not found.
        """
        for route in self.routes:
            if route.GetID() == int(route_id):
                return route
        return None

    def UpdateProfile(self, scores):
        """
        Updates the driver's profile based on different driving aspects (e.g. time of day, breaks taken, braking control etc.)
        :param scores: The dictionary containing the scores to be updated and their respective values.
        :return: Nothing.
        """
        for key in scores.keys():
            if key == "acceleration":
                self.profile.UpdateAccelerationScore(scores[key])
            elif key == "braking":
                self.profile.UpdateBrakingScore(scores[key])
            elif key == "time":
                self.profile.UpdateTimeScore(scores[key])
            elif key == "breaks":
                self.profile.UpdateBreakCountScore(scores[key])
            elif key == "speed":
                self.profile.UpdateAverageSpeedScore(scores[key])
            else:
                print(key + " is not a valid score!")
                print("Valid Score Names: acceleration, braking, time, breaks, speed")
                continue

    def AddRoute(self, newRoute):
        """
        Adds a route to a driver's list of driven routes.
        :param newRoute: The route to be added.
        :return: Nothing.
        """
        self.routes.append(newRoute)

    def UpdateWeeklyJourneys(self):
        """
        Should update the number of weekly journeys made by a driver. By removing the journeys older than 7 days and 
        adding new journeys that are less than a day old in it's place.
        
        Not implementable with our current data, due to no dates being available, only the time - measured in seconds.
        
        :return: Nothing.
        """
        self.averageWeeklyJourneys = self.calculation.meanAverage(len(self.routes), 7)

	# Points in each route should be sorted before calling this function
    def UpdateAverageBreaks(self):
        """
        Should update the number of average breaks a driver makes for the routes he drives along - per week.
        
        Not implementable due to the data not containing any dates - just the time the point was captured, measured in 
        seconds.
        
        :return: Nothing.
        """
        self.averageBreaks = 0
        for route in self.routes:
            thePoints = route.points
            # Gets each consecutive pair of points in the list
            for point1, point2 in zip(thePoints, thePoints[1:]):
                tempAcceleration = self.calculation.acceleration(point2.GetSpeed(), point1.GetSpeed(), point2.GetTimeRecorded(), point1.GetTimeRecorded())
                if tempAcceleration >= -0.1 and tempAcceleration <= 0.1:
                    self.averageBreaks = self.averageBreaks + 1

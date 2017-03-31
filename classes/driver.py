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
        results = Journey.query.filter_by(Driver_ID=self.information.GetID()).all()
        for route in results:
            new_route = Route(route.Route_ID)
            self.AddRoute(new_route)

    def CalculateInsurance(self):
        pass

    def GetProfile(self):
        return self.profile

    def GetInsurance(self):
        return self.estimatedInsurance

    def GetWeeklyJourneys(self):
        return self.averageWeeklyJourneys

    def GetAverageNumberOfBreaks(self):
        return self.averageBreaks

    def GetAllRoutes(self):
        return self.routes

    def GetRouteById(self, route_id):
        for route in self.routes:
            if route.GetID() == int(route_id):
                return route
        return None

    def UpdateProfile(self, scores):
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
        self.routes.append(newRoute)

    # FUNCTIONS TO BE COMPLETED - MOVE ABOVE ME WHEN COMPLETE

    # def RemoveRoute(self, specificID):
        # return 0

    # def RemoveRoute(self, specificPoint):
        # return 0

    # def GetSpecificRoutes(self, specificPoint):
        # return 0

    def UpdateWeeklyJourneys(self):
        self.averageWeeklyJourneys = self.calculation.meanAverage(len(self.routes), 7)

	# Points in each route should be sorted before calling this function
    def UpdateAverageBreaks(self):
        self.averageBreaks = 0
        for route in self.routes:
            thePoints = route.points
            # Gets each consecutive pair of points in the list
            for point1, point2 in zip(thePoints, thePoints[1:]):
                tempAcceleration = self.calculation.acceleration(point2.GetSpeed(), point1.GetSpeed(), point2.GetTimeRecorded(), point1.GetTimeRecorded())
                if tempAcceleration >= -0.1 and tempAcceleration <= 0.1:
                    self.averageBreaks = self.averageBreaks + 1

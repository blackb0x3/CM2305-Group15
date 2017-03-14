from classes.user import User
from classes.profile import Profile
from classes.route import Route
from models import Journey

class Driver:
    def __init__(self, driver_information):
        # Do Not Move or Reorder
        self.routes = []
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
        return 0

    def UpdateAverageBreaks(self):
        return 0

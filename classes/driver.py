from user import User
from profile import Profile

class Driver(User):
    def __init__(self, ID, forename, surname, email, estimatedInsurance, driverProfile, routes):        
        User.__init__(self, ID, forename, surname, email)
        self.estimatedInsurance = estimatedInsurance
        self.profile = driverProfile
        self.routes = routes
        self.averageWeeklyJourneys = self.UpdateWeeklyJourneys()
        self.averageBreaks = self.UpdateAverageBreaks()
        
    # If you're wondering why there's no user functions from the class diagram, see User
    
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
    
    def RemoveRoute(self, specificID):
        return 0
    
    def RemoveRoute(self, specificPoint):
        return 0
    
    def GetSpecificRoutes(self, specificPoint):
        return 0
    
    def UpdateWeeklyJourneys(self):
        return 0
    
    def UpdateAverageBreaks(self):
        return 0
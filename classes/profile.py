from models import Drivers

class Profile:
    def __init__(self, Drivers):
        self.accelerationScore = 0
        self.brakingScore = 0
        self.timeScore = 0
        self.breaksScore = 0
        self.speedScore = 0

    def GetAccelerationScore(self):
        return self.accelerationScore

    def GetBrakingScore(self):
        return self.brakingScore

    def GetTimeScore(self):
        return self.timeScore

    def GetBreakCountScore(self):
        return self.breaksScore

    def GetAverageSpeedScore(self):
        return self.speedScore

    def UpdateAccelerationScore(self, newScore):
        self.accelerationScore = newScore

    def UpdateBrakingScore(self, newScore):
        self.brakingScore = newScore

    def UpdateTimeScore(self, newScore):
        self.timeScore = newScore

    def UpdateBreakCountScore(self, newScore):
        self.breaksScore = newScore

    def UpdateAverageSpeedScore(self, newScore):
        self.speedScore = newScore

class Profile(object):
    def __init__(self, accel, brake, time, Break, speed):
        self.accelerationScore = accel
        self.brakingScore = brake
        self.timeScore = time
        self.breaksScore = Break
        self.speedScore = speed
    
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
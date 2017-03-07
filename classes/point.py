class Point(object):
    def __init__(self, ID, x, y, time, speed):
        self.id = ID
        self.x = x
        self.y = y
        self.time = time
        self.speed = speed
    
    def GetID(self):
        return self.id
    
    def GetXCoordinate(self):
        return self.x
    
    def GetYCoordinate(self):
        return self.y
    
    def GetTimeRecorded(self):
        return self.time
    
    def GetSpeed(self):
        return self.speed
    
    # FUNCTIONS TO BE COMPLETED - MOVE ABOVE ME WHEN COMPLETE
    
    # QUERY DATABASE FOR GPS POINT OF "pointID"
    def QueryPointInfo(pointID):
        return 0
from calculations import Calculations

class Route(object):
    
    
    def GetID(self):
        return self.id
    
    # NOT CURRENTLY FUNCTIONAL - NO "points" ATTRIBUTE
    def GetAverageSpeed(self):
        return Calculations.harmonicAverage(self.points)
    
    def AddPoint(self, newPoint):
        self.points.append(newPoint)
    
    # FUNCTIONS TO BE COMPLETED - MOVE ABOVE ME WHEN COMPLETE
    
    # NOT COMPLETE - NEEDS CODE TO QUERY DATABASE FOR ROUTE INFORMATION
    def __init__(ID):
        self.id = ID
        
    def GetSpecificPoint(self, specificID):
        return 0
    
    def GetSpecificPoint(self, specificX, specificY):
        return 0
    
    def GetNumberOfBreaks(self):
        return 0
    
    def RemovePoint(self, specificID):
        return 0
    
    def RemovePoint(self, specificX, specificY):
        return 0
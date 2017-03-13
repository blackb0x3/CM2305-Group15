from Calculations import Calculations
from models import Data

class Route:
    def __init__(self, ID):
        self.id = ID
        self.points = []
        self.PopulatePoints()

    def PopulatePoints(self):
        results = Data.query.filter_by(Route_ID=self.id).all()
        for point in results:
            self.AddPoint(point)

    def GetID(self):
        return self.id

    # NOT CURRENTLY FUNCTIONAL - NO "points" ATTRIBUTE
    def GetAverageSpeed(self):
        return Calculations.harmonicAverage(self.points)

    def AddPoint(self, newPoint):
        self.points.append(newPoint)

    # FUNCTIONS TO BE COMPLETED - MOVE ABOVE ME WHEN COMPLETE

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

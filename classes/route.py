from Calculations import Calculations
from models import Data

class Route:
    def __init__(self, ID):
        self.id = ID
        self.points = []
        self.PopulatePoints()
        self.calculation = Calculations()

    def PopulatePoints(self):
        results = Data.query.filter_by(Route_ID=self.id).all()
        for point in results:
            self.AddPoint(point)

    def GetID(self):
        return self.id

    # NOT CURRENTLY FUNCTIONAL - NO "points" ATTRIBUTE
    def GetAverageSpeed(self):
        return self.calculation.harmonicAverage(self.points)

    def AddPoint(self, newPoint):
        self.points.append(newPoint)

    def GetRoutePath(self):
        pathCoordinates = []
        for point in self.points:
            coordinates = {}
            pointX = float(point.X_Coord)
            pointY = float(point.Y_Coord)
            lng, lat = self.calculation.convertXY2LonLat(pointX, pointY)
            lat -= 0.00141938548
            lng += 0.00015534789
            coordinates["lat"] = lat
            coordinates["lng"] = lng
            pathCoordinates.append(coordinates)
        return pathCoordinates

    # FUNCTIONS TO BE COMPLETED - MOVE ABOVE ME WHEN COMPLETE

    # def GetSpecificPoint(self, specificID):
        # return 0

    # def GetSpecificPoint(self, specificX, specificY):
        # return 0

    # def GetNumberOfBreaks(self):
        # return 0

    # def RemovePoint(self, specificID):
        # return 0

    # def RemovePoint(self, specificX, specificY):
        # return 0

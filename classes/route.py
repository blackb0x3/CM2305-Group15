from Calculations import Calculations
from models import Data

class Route:
    def __init__(self, ID):
        self.id = ID
        self.points = []
        self.PopulatePoints()
        self.calculation = Calculations()

    def PopulatePoints(self):
        """
        Adds the points of the route to this instantiation.
        :return: Nothing.
        """
        results = Data.query.filter_by(Route_ID=self.id).all()
        for point in results:
            self.AddPoint(point)

    def GetID(self):
        """
        Gets the ID of this route, pulled from the database.
        :return: The ID of this Route object.
        """
        return self.id

    def GetAverageSpeed(self):
        """
        Gets the average driving speed over this route. Functionality implemented in the Calculations class 
        instead.
        
        :return: The average speed of the vehicle across this route.
        """
        return self.calculation.harmonicAverage(self.points)

    def AddPoint(self, newPoint):
        """
        Adds a new point to the list of points for this route.
        :param newPoint: The point to be added.
        :return: Nothing.
        """
        self.points.append(newPoint)

    def GetRoutePath(self):
        """
        Gets the path of the route, in order, from start to finish.
        :return: The sorted list of points for this route, from start to finish.
        """
        pathCoordinates = []
        for point in self.points:
            coordinates = {}
            pointX = float(point.X_Coord)
            pointY = float(point.Y_Coord)
            lng, lat = self.calculation.convertXY2LonLat(pointX, pointY)
            lat -= 0.00141938548 # Latitude offset
            lng += 0.00015534789 # Longitude offset
            coordinates["lat"] = lat
            coordinates["lng"] = lng
            pathCoordinates.append(coordinates)
        return pathCoordinates

    def GetStartTime(self):
        """
        Gets the time that the journey started.
        :return: The time the journey started, measured in seconds.
        """
        if len(self.points) > 0:
            firstPoint = self.points[0]
            startTime = self.calculation.timeToDate(firstPoint.GetTimeRecorded())
            return startTime
        else:
            return 0

    def GetDuration(self):
        """
        Gets the amount of minutes a particular route takes. Used on the journeys page for the driver portal.
        :return: The duration of the route, in MM:SS format.
        """
        if len(self.points) > 0:
            firstPoint = self.points[0]
            lastPoint = self.points[len(self.points) - 1]
            duration = lastPoint.GetTimeRecorded() - firstPoint.GetTimeRecorded()
            m, s = divmod(duration, 60)
            return "%02d:%02d" % (m, s)
        else:
            return "0"

    def GetStartPosition(self):
        """
        Gets the start (x, y) co-ordinates for the route.
        :return: A list of size 2, containing the (x, y) co-ordinates for the start of this route.
        """
        if len(self.points) > 0:
            point = self.points[0]
            lng, lat = self.calculation.convertXY2LonLat(float(point.GetXCoordinate()), float(point.GetYCoordinate()))
            return [round(lat, 4), round(lng, 4)]
        else:
            return [0, 0]

    def GetEndPosition(self):
        """
        Gets the end (x, y) co-ordinates for the route.
        :return: A list of size 2, containing the (x, y) co-ordinates for the end of this route.
        """
        if len(self.points) > 0:
            point = self.points[len(self.points) - 1]
            lng, lat = self.calculation.convertXY2LonLat(float(point.GetXCoordinate()), float(point.GetYCoordinate()))
            return [round(lat, 4), round(lng,4)]
        else:
            return [0, 0]

    # FUNCTIONS TO BE COMPLETED FOR EXTENSION TO THIS APPLICATION, SUCH AS REMOVING OLD POINTS ON A ROUTE.

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

from math import sqrt, pow, pi, cos
from haversine import haversine
import pyproj

class Calculations:
    def __init__(self):
        self._location = {}
        self._location["projParameter"] = "+proj=utm +zone=32 +ellps=WGS84 +datum=WGS84 +units=m +no_defs"
        self._location["netOffset"] = "-342498.65,-5630866.92"
        self._location["origin"] = (51.016862, 6.90314)

    def timeToDate(self, seconds):
        """ Convert Seconds to Hours:Minutes:Seconds """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def pythagoreanDistance(self, x, y):
        """ Calculate the distance between two points. """
        return sqrt(pow(x, 2) + pow(y, 2))

    def haversineDistance(self, lat1, lat2, lon1, lon2):
        """ Calculate the distance (in km or in miles) bewteen two points on Earth, located by their latitude and longitude. """
        origin = (lat1, lon1)
        position = (lat2, lon2)
        return haversine(origin, position)

    def getGeoProj(self):
        p1 = self._location["projParameter"].split()
        params = {}
        for p in p1:
            ps = p.split("=")
            if len(ps) == 2:
                params[ps[0]] = ps[1]
            else:
                params[ps[0]] = True
        return pyproj.Proj(projparams=params)

    def getLocationOffset(self):
        """ offset to be added after converting from geo-coordinates to UTM"""
        return list(map(float, self._location["netOffset"].split(",")))

    def convertLonLat2XY(self, lon, lat, rawUTM=False):
        """ Convert longitude and latitude to X and Y Positions"""
        x, y = self.getGeoProj()(lon, lat)
        if rawUTM:
            return x, y
        else:
            x_off, y_off = self.getLocationOffset()
            return x + x_off, y + y_off

    def convertXY2LonLat(self, x, y, rawUTM=False):
        """ Convert X and Y Positions to longitude and latitude"""
        if not rawUTM:
            x_off, y_off = self.getLocationOffset()
            x = x - float(x_off)
            y = y - float(y_off)
        return self.getGeoProj()(x, y, inverse=True)

    def acceleration(self, s1, s2, t1, t2):
        return (float)((s2 - s1) / (t2 - t1))

    def meanAverage(self, journeys, days):
        return (float)(journeys / days)

    def harmonicAverage(self, a):
        return (float)(len(a) / np.sum(1.0 / a))

    """
    Get the average speed between each set of points in each route, if the average speed is consistent across most of
    the routes, then return a high score, else, return a low score.
    """
    def rateAcceleration(self):
        return 0

    def rateBraking(self):
        return 0


    def rateTimeOfDriving(self, routes):
        """
        Get the time of driving for each point of each route, return a score based on the number of routes that have been
        driven during the day.
        :param Calculations self: The instance of the Calculations class
        :param list[Route] routes: A driver's routes to be evaluated
        :return int
        """
        totalTimeDriving = 0
        dayDuration = 0

        for route in routes:
            firstPoint = route.points[0]



        return False

    def getHourOfDriving(self, seconds):
        return (int)(seconds / 60) // 60 # Converts seconds to hours

    def rateBreaksTaken(self):
        return 0

    def rateAverageSpeed(self):
        return 0
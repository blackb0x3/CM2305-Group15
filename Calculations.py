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

    def acceleration(s1, s2, t1, t2):
        return (float)((s2 - s1) / (t2 - t1))

    def meanAverage(journeys, days):
        return (float)(journeys / days)

    def harmonicAverage(a):
        return (float)(len(a) / np.sum(1.0 / a))

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

    Get DBLA average brake speed / acceleration, create a normal distribution of braking / acceleration, compare this
    to the DBLA average, return score based on this comparison.
    """
    def rateAcceleration(self):
        return 0

    def rateBraking(self):
        return 0


    def rateTimeOfDriving(self, routes):
        """
        Get the time of driving for each point of each route, return a score based on the number of routes that have been
        driven during the day.
        :param Calculations self: The instance of the Calculations class.
        :param list[Route] routes: A driver's routes to be evaluated.
        :return int score: The score out of 100 for the times of day a driver drives their car.
        """

        totalTimeDriving = getTotalDrivingTime(self, routes)
        dayDuration = 0
        timeInRushHour = 0
        morningHour = 7 # Should be an integer between 4 and 8 - i.e. a morning time
        eveningHour = 19
        morningCutOff = morningHour * 60 * 60
        eveningCutOff = eveningHour * 60 * 60
        rushHourCutOffStart = 7 * 60 * 60
        rushHourCutOffEnd = 9 * 60 * 60
        rushHourPenalty = 0


        for route in routes:
            firstPoint = route.points[0].GetTimeRecorded()
            lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
            duration = lastPoint - firstPoint
            totalTimeDriving += duration

            # If the driver starts at night and ends in the day
            if morningCutOff - firstPoint >= 0 and lastPoint <= eveningCutOff:
                dayDuration += duration - (morningCutOff - firstPoint)

            # If the driver starts in the day and ends in the day
            elif morningCutOff - firstPoint < 0 and lastPoint <= eveningCutOff:
                dayDuration += duration

            # If the driver starts in the day and ends in the night
            elif morningCutOff - firstPoint < 0 and lastPoint > eveningCutOff:
                dayDuration += duration - firstPoint

            # If the driver starts in the night and ends in the night, but drives throughout the day
            # between the two cut off points for morning and evening
            elif morningCutOff - firstPoint >= 0 and lastPoint > eveningCutOff:
                dayDuration += eveningCutOff - morningCutOff

            # If a driver drives during rush hour traffic, a penalty is accumulated
            if (firstPoint < rushHourCutOffStart or firstPoint < rushHourCutOffEnd) and lastPoint > rushHourCutOffStart:
                rushHourPenalty += 1


        rushHourPenalty = rushHourPenalty / len(routes) * 0.25 # 0.25 - "1 in 4 chance of having an accident in rush hour"
        #(http://demography.cpc.unc.edu/2014/03/24/1-in-4-car-accidents-occur-during-rush-hour/)
        rushHourPenalty = 1 - rushHourPenalty
        totalTimeDriving += timeInRushHour
        score = (int)(dayDuration / totalTimeDriving) * 100 * rushHourPenalty
        return score


    def getHourOfDriving(self, seconds):
        return (seconds / 60) // 60 # Converts seconds to hours

    def getTotalDrivingTime(self, routes):
        totalTimeDriving = 0
        for route in routes:
            firstPoint = route.points[0].GetTimeRecorded()
            lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
            duration = lastPoint - firstPoint
            totalTimeDriving += duration
        return totalTimeDriving

    def rateBreaksTaken(self, routes):
        numberOfBreaks = 0
        duration = getTotalDrivingTime(self, routes)
        durationInHours = getHourOfDriving(self, duration)
        for route in routes:
            for i in range(len(route.points) - 2):
                if route.points[i].GetXCoordinate() == route.points[i + 1].GetXCoordinate() and route.points[i].GetYCoordinate() == route.points[i + 1].GetYCoordinate():
                    if route.points[i + 1].GetXCoordinate() == route.points[i + 2].GetXCoordinate() and route.points[i + 1].GetYCoordinate() == route.points[i + 2].GetYCoordinate():
                        numberOfBreaks += 1
        # Work out the score for a certain number of breaks per given time interval, i.e. every 1 hour or so

        return 0

    def rateAverageSpeed(self):
        return 0
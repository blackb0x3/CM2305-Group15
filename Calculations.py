from math import sqrt, pow, pi, cos
from haversine import haversine
import pyproj
import numpy as np

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
        for point in a[:]:
            if point.GetSpeed() > -0.01 and point.GetSpeed() < 0.01:
                a.remove(point)
                # Above lines required to eliminate 0 speeds, since 1 / 0 outputs an error
        return (float)(len(a) / np.sum([1.0 / float(point.GetSpeed()) for point in a]))

    def secondsToMinutes(self, seconds):
        return seconds / 60

    def minutesToHours(self, minutes):
        return minutes / 60

    def secondsToHours(self, seconds):
        return self.minutesToHours(self.secondsToMinutes(seconds))

    def hoursToMinutes(self, hours):
        return hours * 60

    def minutesToSeconds(self, minutes):
        return minutes * 60

    def hoursToSeconds(self, hours):
        return self.minutesToSeconds(self.hoursToMinutes(hours))

    """
    Get the average speed between each set of points in each route, if the average speed is consistent across most of
    the routes, then return a high score, else, return a low score.

    Get DVLA average brake speed / acceleration, create a normal distribution of braking / acceleration, compare this
    to the DVLA average, return score based on this comparison.
    """
    def rateAcceleration(self, routes): #incomplete, we need a globalaverageAcceleration figure

        minimumAcceleration = 2
        #function doesn't record acceleration values below 2 to prevent constant speed driving from skewing the data

        accelerations = []
        #a list containing the acceleration between each point

        count = 0
        #a count value for the average for loop

        total = 0
        #a total value for the accelerations

        for route in routes:

            for point in route.points:

                firstCoords = route.points[point]
                firstXCoord = GetXCoordinate(firstCoords)
                firstYCoord = GetYCoordinate(firstCoords)

                secondCoords = route.points[point + 1]
                secondXCoord = GetXCoordinate(secondCoords)
                secondYCoord = GetYCoordinate(secondCoords)

                pointAcceleration = acceleration(firstXCoord, secondXCoord, firstYCoord, secondYCoord)

                if pointAcceleration > minimumAcceleration:
                    accelerations.append(pointAcceleration)

        for figures in accelerations:
            total += accelerations[figures]
            count += 1

        averageAcceleration = total/count


        #if averageAcceleration <= globalaverageAcceleration:
        #    score = "Good"

        #if averageAcceleration <= globalaverageAcceleration/2:
        #    score = "Excellent"

        #if averageAcceleration > globalaverageAcceleration:
        #    score = "Bad"

        #if averageAcceleration >= globalaverageAcceleration*1.5:
        #    score = "Very Bad"

        return 0

    def rateBraking(self, routes): #incomplete for the same reasons that rateAcceleration is incomplete

        minimumDeceleration = -2
        #funtion doesn't record accelerations above -2

        brakes = []
        #list containing braking between each point

        count = 0
        #same purpose as it had in the acceleration function

        total = 0
        #same purpose as it had in the acceleration function

        for route in routes:

            for point in route.points:

                firstCoords = route.points[point]
                firstXCoord = GetXCoordinate(firstCoords)
                firstYCoord = GetYCoordinate(firstCoords)

                secondCoords = route.points[point + 1]
                secondXCoord = GetXCoordinate(secondCoords)
                secondYCoord = GetYCoordinate(secondCoords)

                pointAcceleration = acceleration(firstXCoord, secondXCoord, firstYCoord, secondYCoord)

                if pointAcceleration < minimumDeceleration:
                    brakes.append(pointAcceleration)

        for figures in brakes:
            total += brakes[figures]
            count += 1

        averageBraking = total/count

        #if averageBraking <= globalaverageBraking:
            #score = "Soft"

        #if averageBraking <= globalaveragBraking/2:
            #score = "Very Soft"

        #if averageBraking > globalaverageBraking:
            #score = "Harsh"

        #if averageBraking >= globalaverageBraking*1.5:
            #score = "Very Harsh"

        return 0


    def rateTimeOfDriving(self, routes):
        """
        Get the time of driving for each point of each route, return a score based on the number of routes that have been
        driven during the day.
        :param Calculations self: The instance of the Calculations class.
        :param list[Route] routes: A driver's routes to be evaluated.
        :return int score: The score out of 100 for the times of day a driver drives their car.
        """

        totalTimeDriving = self.getTotalDrivingTime(routes)
        dayDuration = 0
        timeInRushHour = 0
        morningHour = 7 # Should be an integer between 4 and 8 - i.e. a morning time
        eveningHour = 19
        morningCutOff = self.hoursToSeconds(morningHour)
        eveningCutOff = self.hoursToSeconds(eveningHour)
        rushHourCutOffStart = self.hoursToSeconds(7)
        rushHourCutOffEnd = self.hoursToSeconds(9)
        rushHourPenalty = 0


        for route in routes:
            firstPoint = route.points[0].GetTimeRecorded()
            lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
            duration = lastPoint - firstPoint
            print("Start Time: " + self.timeToDate(firstPoint) + "\tEnd Time: " + self.timeToDate(lastPoint))
            totalTimeDriving += duration

            # If the driver starts in the night and ends in the night, but doesn't drive throughout the day
            # e.g. between 5 and 6 o'clock, or 20 and 21 o'clock
            if (morningCutOff - firstPoint >= 0 and lastPoint < morningCutOff) or (eveningCutOff - firstPoint < 0 and lastPoint > eveningCutOff):
                dayDuration += 0

            # If the driver starts at night and ends in the day
            elif morningCutOff - firstPoint >= 0 and lastPoint <= eveningCutOff:
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
        score = int((dayDuration / totalTimeDriving) * 100 * rushHourPenalty)

        if score < 0:
            score = 0
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

    def getTotalDrivingTimeForARoute(self, route):
        firstPoint = route.points[0].GetTimeRecorded()
        lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
        duration = lastPoint - firstPoint
        return duration

    def rateBreaksTaken(self, routes):
        """
        Calculates an average for how regularly a driver takes breaks from driving for each of their journeys.
        :param Calculations self: The instance of the Calculations class.
        :param list[Route] routes: A driver's routes to be evaluated.
        :return int score: The score out of 100 for the frequency of resting from driving.
        """
        scores = list()
        for route in routes:
            numberOfBreaks = 0
            duration = self.getTotalDrivingTimeForARoute(route)
            durationInHours = self.getHourOfDriving(duration)
            trackedPoints = list()
            for i in range(len(route.points)):
                if route.points[i] not in trackedPoints:
                    if float(route.points[i].GetSpeed()) > float(-0.01) and float(route.points[i].GetSpeed()) < float(0.01):
                        j = i + 1
                        endPoint = route.points[i]
                        trackedPoints.append(route.points[i])

                        while route.points[j].GetSpeed() > -0.01 and route.points[j].GetSpeed() < 0.01:
                            endPoint = route.points[j]
                            trackedPoints.append(endPoint)
                            j += 1
                        lengthOfBreak = int(endPoint.GetTimeRecorded() - route.points[i].GetTimeRecorded())

                        if self.secondsToMinutes(lengthOfBreak) > 20:
                            numberOfBreaks += 1

            # Work out the score for a certain number of breaks per given time interval, i.e. every 1 hour or so
            score = (int) (numberOfBreaks / self.secondsToHours(duration) * 100)

            # Limits to 100 for any drivers who take very regular breaks when driving, or don't require a break because the journey doesn't take too long
            if (numberOfBreaks < 1 and self.secondsToMinutes(duration) < 60) or score > 100:
                score = 100

            scores.append(score)

        return sum(scores) / len(scores)

    def kphToMps(self, kph):
        return ((kph * 1000) / 60) / 60

    # Source: http://gogermany.about.com/od/planyourtrip/p/driving-Germany.htm
    def rateAverageSpeed(self, routes):
        """
        Calculates an average for the average speed of a driver over different types of roads.
        :param Calculations self: The instance of the Calculations class.
        :param list[Route] routes: A driver's routes to be evaluated.
        :return int score: The score out of 100 for the average driving speed of a driver.
        """
        speedLimitForCities = self.kphToMps(50) # 31 mph / 50 kph
        speedLimitForMotorways = self.kphToMps(100) # 62mph / 100 kph - i.e. the autobahn
        averageSpeedBetweenRoadTypes = speedLimitForMotorways - speedLimitForCities # Gets the average speed between the two types of roads

        speeds = [route.GetAverageSpeed() for route in routes]
        averageSpeed = sum(speeds) / len(speeds)

        score = 0
        if averageSpeed > speedLimitForCities and averageSpeed < speedLimitForMotorways:
            fraction = averageSpeed / averageSpeedBetweenRoadTypes if averageSpeed < averageSpeedBetweenRoadTypes else averageSpeedBetweenRoadTypes / averageSpeed
            score = fraction * 100

        elif averageSpeed > 0 and averageSpeed < speedLimitForCities:
            score = (averageSpeed / averageSpeedBetweenRoadTypes) * 100

        # Score should be 0 if driver has an average speed which is above the highest speed limit on a particular road type
        # Increased risk of accidents could occur at very high speeds

        return score

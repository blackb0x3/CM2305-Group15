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
        self.speedLimitForCities = self.kphToMps(50)  # 31 mph / 50 kph
        self.speedLimitForMotorways = self.kphToMps(100)  # 62mph / 100 kph - i.e. the autobahn

        # Gets the average speed between the two types of roads
        self.averageSpeedBetweenRoadTypes = self.speedLimitForMotorways - self.speedLimitForCities

    def timeToDate(self, seconds):
        """
        Convert Seconds to Hours:Minutes:Seconds (HH:MM:SS).
        :param seconds: the time in seconds to convert.
        :return: The time in HH:MM:SS format.
        """
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        return "%d:%02d:%02d" % (h, m, s)

    def pythagoreanDistance(self, x, y):
        """
        Calculate the distance between two points.
        :param x: The first point to evaluate.
        :param y: The second point to evaluate.
        :return: The distance between the two points in metres.
        """
        return sqrt(pow(x, 2) + pow(y, 2))

    def haversineDistance(self, lat1, lat2, lon1, lon2):
        """
        Calculate the distance (in km or in miles) bewteen two points on Earth, located by their latitude and longitude.
        :param lat1: The latitude of the first point.
        :param lat2: The latitude of the second point.
        :param lon1: The longitude of the first point.
        :param lon2: The longitude of the second point.
        :return: The distance between the first and second point.
        """
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
        """
        Offset to be added after converting from geo-coordinates to UTM.
        :return: The offset in the co-ordinates of each point.
        """
        return list(map(float, self._location["netOffset"].split(",")))

    def convertLonLat2XY(self, lon, lat, rawUTM=False):
        """
        Convert longitude and latitude to X and Y Positions.
        UTM: Universal Transverse Mercator co-ordinate system.
        :param lon: The longitude part of the map co-ordinate.
        :param lat: The latitude part of the map co-ordinate.
        :param rawUTM: Determines whether the data is be converted to UTM co-ordinates - as opposed to XY co-ordinates.
        :return: The (x, y) co-ordinates of the point, in the form of a 2-tuple.
        """
        x, y = self.getGeoProj()(lon, lat)
        if rawUTM:
            return x, y
        else:
            x_off, y_off = self.getLocationOffset()
            return x + x_off, y + y_off

    def convertXY2LonLat(self, x, y, rawUTM=False):
        """
        Convert X and Y Positions to longitude and latitude.
        :param x: The x co-ordinate of the Point.
        :param y: The y co-ordinate of the Point.
        :param rawUTM: Determines whether the data is be converted to UTM co-ordinates - as opposed to XY co-ordinates.
        :return: The (longitude, latitude) co-ordinates of the point.
        """
        if not rawUTM:
            x_off, y_off = self.getLocationOffset()
            x = x - float(x_off)
            y = y - float(y_off)
        return self.getGeoProj()(x, y, inverse=True)

    def acceleration(self, s1, s2, t1, t2):
        """
        Gets the change in speed between two points, recorded by the telematics box.
        :param s1: The initial velocity of the car.
        :param s2: The final velocity of the car.
        :param t1: The start time.
        :param t2: The end time.
        :return: The acceleration between the two points, measured in metres per second.
        """
        if float(s2 - s1) == 0.0 or float(t2 - t1) == 0.0:
            return 0
        else:
            return (float)((s2 - s1) / (t2 - t1))

    def meanAverage(self, journeys, days):
        """
        Gets the average number of journeys made over a certain number of days.
        :param journeys: The number of journeys made.
        :param days: The number of days the journeys were made over.
        :return: The average number of journeys made in one day.
        """
        return (float)(journeys / days)

    def harmonicAverage(self, a):
        """
        Calculate the truest average speed over a given set of points.
        :param a: The list of points to evaluate.
        :return: The average speed across all of the points in parameter a.
        """
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

    def rateAcceleration(self, routes):
        """
        Get the average speed between each set of points in each route, if the average speed is consistent across most 
        of the routes, then return a high score, else, return a low score.
        :param routes: The journeys of a specified driver.
        :return: A score for the average acceleration across all the provided routes
        """
        minimumAcceleration = 2
        #function doesn't record acceleration values below 2 to prevent constant speed driving from skewing the data

        accelerations = []
        #a list containing the acceleration between each point

        count = 0
        #a count value for the average for loop

        total = 0
        #a total value for the accelerations

        # Get the acceleration between every pair of points
        for route in routes:
            for i in range(len(route.points) - 1):
                firstCoord = route.points[i]
                secondCoord = route.points[i + 1]

                pointAcceleration = self.acceleration(firstCoord.GetSpeed(),
                                                      secondCoord.GetSpeed(),
                                                      firstCoord.GetTimeRecorded(),
                                                      secondCoord.GetTimeRecorded())

                # Check if they're accelerating, as opposed to braking - which would be a negative value
                if pointAcceleration > minimumAcceleration:
                    accelerations.append(pointAcceleration)

        # Create a list of accelerations between every pair of points
        for figures in accelerations:
            total += figures
            count += 1

        averageAccelerationForDriver = total/count

        # Get average acceleration on general road types (street roads and the autobahn)
        averageAccelerationForRoads = self.acceleration(0, self.kphToMps(self.averageSpeedBetweenRoadTypes), 1, 2)

        # Compare driver's acceleration to the average
        # The closer to the average, the higher their score.
        score = averageAccelerationForDriver / averageAccelerationForRoads

        # Corrects score if resulting fraction is greater than the highest score available
        if score > 1:
            if score > 2:
                score = 1
            else:
                score = 1 - (score - 1)

        return int(score * 100)

    def rateBraking(self, routes): #incomplete for the same reasons that rateAcceleration is incomplete

        # function doesn't record accelerations above -2
        minimumDeceleration = -2

        # list containing braking between each point
        brakes = []

        # same purpose as it had in the acceleration function
        count = 0

        # same purpose as it had in the acceleration function
        total = 0

        # Get the braking between every pair of points
        for route in routes:
            for i in range(len(route.points) - 1):
                firstCoord = route.points[i]
                secondCoord = route.points[i + 1]

                pointAcceleration = self.acceleration(firstCoord.GetSpeed(),
                                                      secondCoord.GetSpeed(),
                                                      firstCoord.GetTimeRecorded(),
                                                      secondCoord.GetTimeRecorded())

                # Check if they're braking, as opposed to accelerating - which would be a positive value
                if pointAcceleration < minimumDeceleration:
                    brakes.append(pointAcceleration)

        for figures in brakes:
            total += figures
            count += 1

        averageBrakingForDriver = total / count

        # Get average acceleration on general road types (street roads and the autobahn)
        averageBrakingForRoads = self.acceleration(self.kphToMps(self.averageSpeedBetweenRoadTypes), 0, 1, 2)

        # Compare driver's braking to the average
        # The closer to the average, the higher their score.
        score = averageBrakingForDriver / averageBrakingForRoads

        # Corrects score if resulting fraction is greater than the highest score available
        if score > 1:
            if score > 2:
                score = 1
            else:
                score = 1 - (score - 1)

        return int(score * 100)


    def rateTimeOfDriving(self, routes):
        """
        Get the time of driving for each point of each route, return a score based on the number of routes that have 
        been driven during the day.
        :param routes: A driver's routes to be evaluated.
        :return score: The score out of 100 for the times of day a driver drives their car.
        """

        totalTimeDriving = self.getTotalDrivingTime(routes) # Irrespective of whether it was during the day or night.
        dayDuration = 0 # Time driving during the day time, between the morning and evening cut off.
        timeInRushHour = 0 # Time spent in rush hour traffic.
        morningHour = 7 # Should be an integer between 4 and 8 - i.e. a morning time
        eveningHour = 19 # Should be an integer between 17 and 21 - i.e. an evening time
        morningCutOff = self.hoursToSeconds(morningHour)
        eveningCutOff = self.hoursToSeconds(eveningHour)
        rushHourCutOffStart = self.hoursToSeconds(7)
        rushHourCutOffEnd = self.hoursToSeconds(9)
        rushHourPenalty = 0 # Penalty for driving extra amount of time in rush hour.


        for route in routes:
            firstPoint = route.points[0].GetTimeRecorded()
            lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
            duration = lastPoint - firstPoint
            # print("Start Time: " + self.timeToDate(firstPoint) + "\tEnd Time: " + self.timeToDate(lastPoint))
            # Above line was used for testing purposes, to confirm the start and end times for some drivers' routes.
            totalTimeDriving += duration

            # If the driver starts in the night and ends in the night, but doesn't drive throughout the day
            # e.g. between 5 and 6 o'clock, or 20 and 21 o'clock
            if (morningCutOff - firstPoint >= 0 and lastPoint < morningCutOff) or \
                    (eveningCutOff - firstPoint < 0 and lastPoint > eveningCutOff):
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

        rushHourPenalty = rushHourPenalty / len(routes) * 0.25  # "1 in 4 chance of having an accident in rush hour"
        # Source: http://demography.cpc.unc.edu/2014/03/24/1-in-4-car-accidents-occur-during-rush-hour/
        rushHourPenalty = 1 - rushHourPenalty
        totalTimeDriving += timeInRushHour
        score = (((float(dayDuration) / float(totalTimeDriving)) * 100) * rushHourPenalty)

        if score < 0:
            score = 0
        return score

    def getTotalDrivingTime(self, routes):
        """
        Gets the total amount of time driving for all of a driver's journeys.
        :param routes: The journeys to be evaluated. 
        :return: The total time driven across all of a driver's journeys.
        """
        totalTimeDriving = 0
        for route in routes:
            firstPoint = route.points[0].GetTimeRecorded()
            lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
            duration = lastPoint - firstPoint
            totalTimeDriving += duration
        return totalTimeDriving

    def getTotalDrivingTimeForARoute(self, route):
        """
        Gets the total amount of time driving for a specific journey.
        :param route: The journey to be evaluated. 
        :return: The total time driven across the specified journey.
        """
        firstPoint = route.points[0].GetTimeRecorded()
        lastPoint = route.points[len(route.points) - 1].GetTimeRecorded()
        duration = lastPoint - firstPoint
        return duration

    def rateBreaksTaken(self, routes):
        """
        Calculates an average for how regularly a driver takes breaks from driving for each of their journeys.
        :param routes: A driver's routes to be evaluated.
        :return score: The score out of 100 for the frequency of resting from driving.
        """
        scores = list()
        for route in routes:
            numberOfBreaks = 0
            duration = self.getTotalDrivingTimeForARoute(route)
            trackedPoints = list()
            for i in range(len(route.points)):
                if route.points[i] not in trackedPoints:
                    # When we encounter a point where the car was not moving
                    if float(-0.01) < float(route.points[i].GetSpeed()) < float(0.01):
                        j = i + 1
                        endPoint = route.points[i]
                        trackedPoints.append(route.points[i])  # Prevents same breaks from being re-added.

                        while -0.01 < route.points[j].GetSpeed() < 0.01:
                            endPoint = route.points[j]
                            trackedPoints.append(endPoint)  # Prevents same breaks from being re-added.
                            j += 1

                        # Calculate the length of time between the start and end of this assumed 'break'
                        lengthOfBreak = int(endPoint.GetTimeRecorded() - route.points[i].GetTimeRecorded())

                        # Counts if it's longer than 20 minutes.
                        if self.secondsToMinutes(lengthOfBreak) > 20:
                            numberOfBreaks += 1

            # Work out the score for a certain number of breaks per given time interval, i.e. every 1 hour or so
            timeHours = self.secondsToHours(duration)

            # Prevents a score of 0 being created if a break wasn't necessary for shorter journeys.
            if timeHours == 0:
                timeHours = 1

            score = int(numberOfBreaks / timeHours * 100)

            # Limits to 100 for any drivers who take very regular breaks when driving, or don't require a break because
            # the journey doesn't take too long
            if (numberOfBreaks < 1 and self.secondsToMinutes(duration) < 60) or score > 100:
                score = 100

            scores.append(score)

        return sum(scores) / len(scores)  # An average evaluation across all driver breaks over all routes.

    def kphToMps(self, kph):
        """
        Converts Kilometres per hour to metres per second
        :param kph: the speed to convert - in KPH
        :return: The converted speed - in MPS
        """
        return ((kph * 1000) / 60) / 60

    # Source: http://gogermany.about.com/od/planyourtrip/p/driving-Germany.htm
    def rateAverageSpeed(self, routes):
        """
        Calculates an average for the average speed of a driver over different types of roads.
        :param routes: A driver's routes to be evaluated.
        :return score: The score out of 100 for the average driving speed of a driver.
        """
        speeds = [route.GetAverageSpeed() for route in routes]
        averageSpeed = sum(speeds) / len(speeds)

        score = 0
        if self.speedLimitForCities < averageSpeed < self.speedLimitForMotorways:
            if averageSpeed < self.averageSpeedBetweenRoadTypes:
                fraction = averageSpeed / self.averageSpeedBetweenRoadTypes
            else:
                fraction = self.averageSpeedBetweenRoadTypes / averageSpeed
            score = fraction * 100

        elif 0 < averageSpeed < self.speedLimitForCities:
            score = (averageSpeed / self.averageSpeedBetweenRoadTypes) * 100

        # Score should be 0 if driver has an average speed which is above the highest speed limit on a particular road
        # type. Increased risk of accidents could occur at very high speeds.

        return score

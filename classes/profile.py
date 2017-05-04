from models import Drivers

class Profile:
    def __init__(self, Drivers):
        self.accelerationScore = 0
        self.brakingScore = 0
        self.timeScore = 0
        self.breaksScore = 0
        self.speedScore = 0

    def GetAccelerationScore(self):
        """
        Get the acceleration score for this driver.
        :return: The driver's acceleration score.
        """
        return self.accelerationScore

    def GetBrakingScore(self):
        """
        Get the braking score for this driver.
        :return: The driver's braking score. 
        """
        return self.brakingScore

    def GetTimeScore(self):
        """
        Get the time of day score for this driver.
        :return: The driver's time of day score. 
        """
        return self.timeScore

    def GetBreakCountScore(self):
        """
        Get the breaks count score for this driver.
        :return: The driver's breaks count score. 
        """
        return self.breaksScore

    def GetAverageSpeedScore(self):
        """
        Get the average speed score for this driver.
        :return: The driver's average speed score. 
        """
        return self.speedScore

    def UpdateAccelerationScore(self, newScore):
        """
        Updates the driver's acceleration score.
        :param newScore: The score which will replace the current score.
        :return: Nothing - the score for this driving evaluation will be updated.
        """
        self.accelerationScore = newScore

    def UpdateBrakingScore(self, newScore):
        """
        Updates the driver's braking score.
        :param newScore: The score which will replace the current score.
        :return: Nothing - the score for this driving evaluation will be updated.
        """
        self.brakingScore = newScore

    def UpdateTimeScore(self, newScore):
        """
        Updates the driver's time of day score.
        :param newScore: The score which will replace the current score.
        :return: Nothing - the score for this driving evaluation will be updated.
        """
        self.timeScore = newScore

    def UpdateBreakCountScore(self, newScore):
        """
        Updates the driver's breaks count score.
        :param newScore: The score which will replace the current score.
        :return: Nothing - the score for this driving evaluation will be updated.
        """
        self.breaksScore = newScore

    def UpdateAverageSpeedScore(self, newScore):
        """
        Updates the driver's average speed score.
        :param newScore: The score which will replace the current score.
        :return: Nothing - the score for this driving evaluation will be updated.
        """
        self.speedScore = newScore

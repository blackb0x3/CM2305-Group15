from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drivers(db.Model):
    """
    A class that represents a driver currently registered with the app.
    """

    # Pulls the columns from the Driver table in the database
    __tablename__ = 'Drivers'
    Driver_ID = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.String(500))
    email = db.Column(db.String(45))
    Client_ID = db.Column(db.BigInteger)

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

    def GetID(self):
        """
        Gets the driver's ID - not to be confused with their login username.
        :return: The driver's ID.
        """
        return self.Driver_ID

    def GetForename(self):
        """
        Gets the forename of the driver.
        :return: The driver's forename.
        """
        return self.first_name

    def GetSurname(self):
        """
        Gets the surname of the driver.
        :return: The driver's surname.
        """
        return self.last_name

    def GetEmailAddress(self):
        """
        Gets the email address of the driver.
        :return: The driver's email address.
        """
        return self.email

    def ChangePassword(self, newPassword):
        """
        Changes the driver's password in the database.
        :param newPassword: The driver's new password.
        :return: Nothing.
        """
        self.password = newPassword

    def GetClientID(self):
        """
        Gets the ID of the insurer the driver is associated with.
        :return: The insurer ID of a driver.
        """
        return self.Client_ID

    def CheckPassword(self, password):
        """
        Checks whether the user's entered password is the same as their current password.
        :param password: The current password the user entered on the Change Password dialog (account.html).
        :return: Boolean value (True or False) determining whether the user entered their old password correctly.
        """
        return (password == self.password)

class Client(db.Model):
    """
    A class that represents an insurer for a set of drivers.
    """

    # Pulls the associated columns from the Client table in the database.
    __tablename__ = 'Client'
    Client_ID = db.Column(db.BigInteger, primary_key=True)
    Client_Name = db.Column(db.String(255))
    Client_Number = db.Column(db.String(14))
    Password = db.Column(db.String(500))

    def __init__(self, name, number, password):
        self.Client_Name = name
        self.Client_Number = number
        self.Password = password

    def GetClientName(self):
        """
        Gets the name of the client. (e.g. Drive Safe Insurers, Got Your Back Insurance, The Car Insurers etc.)
        :return: The name of the client.
        """
        return self.Client_Name

class Data(db.Model):
    """
    A class that represents a driving point recorded by the telematics box.
    """

    # Pulls the columns from the Data table in the database.
    # Each argument specifies the data type of each column, plus whether that column is a primary key for that table.
    __tablename__ = 'Data'
    Point_ID = db.Column(db.Integer, primary_key=True)
    Route_ID = db.Column(db.BigInteger, primary_key=True)
    time = db.Column(db.Integer)
    X_Coord = db.Column(db.Numeric(32,16))
    Y_Coord = db.Column(db.Numeric(32,16))
    speed = db.Column(db.Numeric(16,8))

    def __init__(self, Route_ID, time, X_Coord, Y_Coord, speed):
        self.Route_ID = Route_ID
        self.time = time
        self.X_Coord = X_Coord
        self.Y_Coord = Y_Coord
        self.speed = float(speed)

    def GetID(self):
        """
        Gets the ID of the route that the point belongs to.
        :return: The ID of the route this point belongs to.
        """
        return self.Route_ID

    def GetXCoordinate(self):
        """
        Gets the longitude co-ordinate of this point.
        :return: The longitude co-ordinate of the recorded point.
        """
        return self.X_Coord

    def GetYCoordinate(self):
        """
        Gets the latitude co-ordinate of this point.
        :return: The latitude co-ordinate of the recorded point.
        """
        return self.Y_Coord

    def GetTimeRecorded(self):
        """
        Gets the time when the point was recorded.
        :return: The time of the recording of this point, measured in seconds.
        """
        return self.time

    def GetSpeed(self):
        """
        Gets the velocity of the vehicle at the time of recording this point.
        :return: The velocity of the vehicle at this point, measured in metres per second.
        """
        return self.speed

class Journey(db.Model):
    """
    A class that represents a method of getting from one point to another.
    Differs from the Route class, which is an actual method of getting from one point to another.
    """

    # Pulls the columns from te Journey table in the database.
    __tablename__ = 'Journey'
    Journey_ID = db.Column(db.Integer, primary_key=True)
    Route_ID = db.Column(db.BigInteger, db.ForeignKey('Data.Route_ID'))
    Driver_ID = db.Column(db.BigInteger, db.ForeignKey('Drivers.Driver_ID'))

    def __init__(self, Route_ID, Driver_ID):
        self.Route_ID = Route_ID
        self.Driver_ID = Driver_ID

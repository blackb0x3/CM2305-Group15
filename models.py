from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Drivers(db.Model):
    __tablename__ = 'Drivers'
    Driver_ID = db.Column(db.BigInteger, primary_key=True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    username = db.Column(db.String(45), unique=True)
    password = db.Column(db.Integer)
    email = db.Column(db.String(45))
    Client_ID = db.Column(db.BigInteger)

    def __init__(self, first_name, last_name, username, password, email):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.password = password
        self.email = email

class Client(db.Model):
    __tablename__ = 'Client'
    Client_ID = db.Column(db.BigInteger, primary_key=True)
    Client_Name = db.Column(db.String(255))
    Client_Number = db.Column(db.String(14))
    Password = db.Column(db.String(500))

    def __init__(self, name, number, password):
        self.Client_Name = name
        self.Client_Number = number
        self.Password = password

class Data(db.Model):
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
        self.speed = speed

class Journeys(db.Model):
    __tablename__ = 'Journeys'
    Journey_ID = db.Column(db.Integer, primary_key=True)
    Route_ID = db.Column(db.BigInteger, db.ForeignKey('Data.Route_ID'))
    Driver_ID = db.Column(db.BigInteger, db.ForeignKey('Drivers.Driver_ID'))

    def __init__(self, Route_ID, Driver_ID):
        self.Route_ID = Route_ID
        self.Driver_ID = Driver_ID

class User(object):
    def __init__(self, ID, forename, surname, email):
        self.id = ID
        self.forenames = forename
        self.surname = surname
        self.email = email
    
# Functions moved from Driver to models.py for simplicity
class Administrator(User):
    def __init__(self, ID, forename, surname, email):
        User.__init__(self, ID, forename, surname, email)
        
    # If you're wondering why there's no user functions, see User
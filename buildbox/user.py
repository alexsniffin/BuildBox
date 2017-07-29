class User(object):

    def __init__(self, id, name, attempts, succeeds, fails):
        self.id = id
        self.name = name
        self.attempts = attempts
        self.succeeds = succeeds
        self.fails = fails
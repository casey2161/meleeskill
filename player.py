from trueskill import Rating
class Player:
    def __init__(self, userid, name, tag, rating=Rating(), games=0, isHere=False):
        self.rating = rating
        self.games = games
        self.name = name
        self.tag = tag
        self.isHere = isHere
        self.userid = userid 
    
    def getRating(self):
        return self.rating
    
    def getGamesPlayed(self):
        return self.games

    def getName(self):
        return self.name
    
    def getTag(self):
        return self.tag

    def updateRating(self, rating):
        self.rating = rating
    
    def gamePlayed(self, rating):
        self.games += 1
        self.rating = rating
    
    def toggleHere(self):
        self.isHere = not self.isHere

    def asTuple(self):
        return (self.name, self.tag, self.rating.mu, self.rating.sigma, self.games, self.userid)

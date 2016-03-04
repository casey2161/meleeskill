from trueskill import Rating
class Player:
    def __init__(self, rating=Rating(), games=0, name, tag)
        self.rating = rating
        self.games = games
        self.name = name
        self.tag = tag
    
    def getRating(self):
        return rating
    
    def getGamesPlayed(self):
        return self.games

    def getName(self):
        return self.name
    
    def getTag(self):
        return self.tag

    def updateRating(self, rating):
        self.rating = rating
    
    def gameplayed(self, rating)
        self.games += 1
        self.rating = rating
    

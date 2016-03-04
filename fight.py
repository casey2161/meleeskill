import sqlite3
import sys
import trueskill
from player import Player

def createList(conn):
    cursor = conn.cursor()
    rows = cursor.execute('''SELECT * FROM players''').fetchall()
    return [Player(userid=row[0], name=row[1], tag=row[2], rating=trueskill.Rating(mu=row[3], sigma=row[4]), games=row[5], isHere=True) for row in rows]

def writeDB(conn, players):
    cursor = conn.cursor()
    for player in players:
        cursor.execute('''UPDATE players SET name=?, tag=?, mu=?, sigma=?, games=? WHERE id=?''', player.asTuple())
    conn.commit()

def createDB(conn):
    conn.execute('''CREATE TABLE PLAYERS (ID INTEGER PRIMARY KEY, NAME TEXT NOT NULL, TAG TEXT NOT NULL, MU REAL NOT NULL, SIGMA REAL NOT NULL, GAMES INT NOT NULL);''')

def createPlayer(name, tag, trueskills, conn):
    checker =  conn.cursor().execute('''SELECT id FROM players where tag=?''', (tag,)).fetchone()
    if checker==None:
        userid = conn.cursor().execute('''SELECT max(id) FROM players''').fetchone()[0]
        trueskills.append(Player(name=name, tag=tag, isHere=True, userid=userid))
        conn.cursor().execute('''INSERT INTO players(name,tag,mu,sigma,games) VALUES(?,?,?,?,?)''', (name, tag, trueskill.Rating().mu, trueskill.Rating().sigma, 0))
        conn.commit()
    else:
        print("Player with that tag already exists")
def loop(conn):
    trueskills = createList(conn) 
    env = trueskill.setup()
    done = False
    while(not done):
        option = input("\nEnter menu option:\n1) Report Match\n2) Suggest Match\n3) Add player\n4) Quit\n")
        if option == "1":
            winner = input("Enter the winners tag: ").lower()
            loser = input("Enter the losers tag: ").lower()
            winnerPlayer = None
            loserPlayer = None
            if winner == loser:
                print("Winner can't be the same player as loser")
                continue
            for player in trueskills:
                if player.getTag() == winner:
                    winnerPlayer = player
                elif player.getTag() == loser:
                    loserPlayer = player
            if winnerPlayer == None and loserPlayer == None:
                print("Neither player not found")
                continue
            elif winnerPlayer == None:
                print("Winning player not found")
                continue
            elif loserPlayer == None:
                print("Losing player not found")
                continue
            print("Match quality was {:.1%}".format(trueskill.quality_1vs1(winnerPlayer.getRating(), loserPlayer.getRating())))
            newRating = trueskill.rate_1vs1(winnerPlayer.getRating(), loserPlayer.getRating())
            winnerPlayer.gamePlayed(newRating[0])
            loserPlayer.gamePlayed(newRating[1])
        elif option == "2":
            print("Not currently supported")
        elif option == "3":
            name = input("Input the players first and last name: ").lower()
            tag = input("Input the players tag: ").lower()
            createPlayer(name, tag, trueskills, conn)
        elif option == "4":
            done = True
    writeDB(conn, trueskills)

if __name__ == "__main__":
    conn = sqlite3.connect('melee.db')
    try:
        conn.execute('''SELECT * FROM players''')
    except Exception as e:
        print("No player data found creating...")
        createDB(conn)
    loop(conn)
    conn.close()

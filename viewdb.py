import sqlite3

if __name__=="__main__":
    conn=sqlite3.connect("melee.db")
    print(conn.execute('''SELECT * FROM players''').fetchall())
    print(conn.execute('''SELECT * FROM history''').fetchall())

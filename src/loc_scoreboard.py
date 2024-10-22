import sqlite3

# creates the database lel
def create_database():
    conn = sqlite3.connect('scoreboard.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            score INTEGER NOT NULL
        )
    ''')

    conn.commit()
    conn.close()

def update_scoreboard(username, points):
    conn = sqlite3.connect('scoreboard.db')
    cursor = conn.cursor()

    # Check if database and table exist; create if not
    create_database()

    # check if user already exists
    cursor.execute('SELECT * FROM Users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        new_score = existing_user[2] + points
        cursor.execute('UPDATE Users SET score = ? WHERE username = ?', (new_score, username))
    else:
        cursor.execute('INSERT INTO Users (username, score) VALUES (?, ?)', (username, points))

    # insert data from function parameters

    conn.commit()
    conn.close()

def print_scoreboard():
    conn = sqlite3.connect('scoreboard.db')
    cursor = conn.cursor()

    cursor.execute('SELECT username, score from Users ORDER BY score DESC LIMIT 5')
    top_users = cursor.fetchall()

    max_username_length = max(len(user[0]) for user in top_users) if top_users else 0

    print()
    print("**************************************")
    print("          LOCAL LEADERBOARD           ")
    print("**************************************")
    for index, user in enumerate(top_users, start = 1):
        username = user[0]
        score = user[1]
        print(f'{index}. {username.ljust(max_username_length)}                  {score}')
    print("**************************************")
    print("login with same username to save score")
    print("**************************************")
    print()
    conn.close()

def get_local_scores():
    conn = sqlite3.connect('scoreboard.db')
    cursor = conn.cursor()    

    # Check if database and table exist; create if not
    create_database()

    cursor.execute('SELECT username, score from Users ORDER BY score DESC LIMIT 10')
    top_users = cursor.fetchall() 

    conn.close()
    return top_users

def reset_scoreboard():
    pass
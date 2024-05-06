import sqlite3

def connect():
    return sqlite3.connect('scheduler/files/scheduler.db')


def create_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS scheduled_users (
            user_id INTEGER PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()



def get_users():
    with connect() as conn:
        conn = connect()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM scheduled_users
        ''')
        users = cursor.fetchall()
    
    return users


def create_user(user_id: int):
    with connect() as conn:
        cursor = conn.cursor()
        if not cursor.execute('''
            SELECT * FROM scheduled_users WHERE user_id = ?
        ''', (user_id,)).fetchone():
            cursor.execute('''
                INSERT INTO scheduled_users (user_id)
                VALUES (?)
            ''', (user_id,))
            conn.commit()


print(get_users())
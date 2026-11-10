import sqlite3

create_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL
    );"""

def connect_db(connection):
    # connection = sqlite3.connect("test-db.db")
    cursor = connection.cursor()
    print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

    cursor.execute(create_table)


def add_user(connection, task):
    username = task[0]
    security_sql = """
    SELECT user_id FROM users WHERE user_name = ?"""
    register_sql = """INSERT INTO users (user_name, password) VALUES(?, ?)"""

    cursor = connection.cursor()

    cursor.execute(security_sql, (username, ))

    if cursor.fetchone() is not None:
        print("jest juz taki uzytkownik!!!!!")
        return False
    cursor.execute(register_sql, task)
    connection.commit()
    return True

def get_user_id(connection, login, password):
    get_sql = """
    SELECT user_id FROM users WHERE user_name = ? AND password = ?"""

    cursor = connection.cursor()
    cursor.execute(get_sql, (login, password))

    result = cursor.fetchone()

    return result[0] if result else None
def login_user(connection, login, password):
    login_sql = """
        SELECT password FROM users WHERE user_name = ?"""

    cursor = connection.cursor()
    cursor.execute(login_sql, (login,))

    result = cursor.fetchone()

    if result is None:
        print("Taki skurwiel nie istnieje")
        return False

    db_password = result[0]

    if db_password == password:
        print("zalogowano pomyslnie")
        return True
    else:
        print("zle haslo")
        return False


def close_db(connection):
    connection.close()
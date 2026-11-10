import sqlite3

create_table = """
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        user_name TEXT NOT NULL,
        password TEXT NOT NULL
    );"""


def register_task(_connection, _task):
    register_sql = """INSERT INTO users (user_name, password) VALUES(?, ?)"""

    _cursor = connection.cursor()
    _cursor.execute(register_sql, _task)
    _connection.commit()

    return _cursor.lastrowid

def login_task(_connection, _login, _password):
    login_sql = """
    SELECT password FROM users WHERE user_name = ?"""

    _cursor = _connection.cursor()
    _cursor.execute(login_sql, (_login,))

    result = _cursor.fetchone()

    if result is None:
        print("nie ma takoej osoby")
        return False

    db_password = result[0]

    if db_password == password:
        print("zalogowano pomyslnie")
        return True
    else:
        print("zle haslo")
        return False

with sqlite3.connect("test-db.db") as connection:
    cursor = connection.cursor()
    print(f"Opened SQLite database with version {sqlite3.sqlite_version} successfully.")

    cursor.execute(create_table)

    choice = input("login or register")

    choice = choice.lower()

    if choice == "register":
        login = input("login: ")
        password = input("password: ")

        task = (login, password)

        task_id = register_task(connection, task)
        print(f"jebany task: {task_id}")

        connection.commit()

    if choice == "login":
        login = input("login: ")
        password = input("password: ")

        task = (login, password)
        task_id = login_task(connection, login, password)
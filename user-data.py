import sqlite3


def create_db():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute(
        """CREATE TABLE IF NOT EXISTS userdata
                   (id INTEGER PRIMARY KEY,
                   username TEXT,
                   experience TEXT,
                   personal TEXT)"""
    )
    conn.commit()
    print("User Database Created ")
    conn.close()


def take_input():
    username = str(input("Enter your name: "))
    experience = str(input("Enter your experience (Job/Internship briefly): "))
    personal = str(input("Enter any personal accolades if any: "))
    conn = sqlite3.connect("user.db")
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO userdata (username, experience, personal) VALUES (?, ?, ?)",
        (username, experience, personal),
    )
    print("Created record")
    cursor.execute("SELECT * FROM userdata")
    conn.commit()


def show_records():
    conn = sqlite3.connect("user_data.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM userdata")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

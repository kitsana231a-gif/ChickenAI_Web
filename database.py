import sqlite3

DB_NAME = "egg_count.db"


def init_db():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    CREATE TABLE IF NOT EXISTS history(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        time TEXT,

        egg_count INTEGER,

        confidence REAL,

        fps REAL

    )

    """)

    conn.commit()

    conn.close()


def save_data(time_now, count, conf, fps):

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    INSERT INTO history(time, egg_count, confidence, fps)

    VALUES(?,?,?,?)

    """, (time_now, count, conf, fps))

    conn.commit()

    conn.close()


def get_history():

    conn = sqlite3.connect(DB_NAME)

    cursor = conn.cursor()

    cursor.execute("""

    SELECT * FROM history

    ORDER BY id DESC

    LIMIT 20

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
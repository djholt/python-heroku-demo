import os
import psycopg2
import psycopg2.extras
import urllib.parse

class SquirrelDB:

    def __init__(self):
        urllib.parse.uses_netloc.append("postgres")
        url = urllib.parse.urlparse(os.environ["DATABASE_URL"])

        self.connection = psycopg2.connect(
            cursor_factory=psycopg2.extras.RealDictCursor,
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )

        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()

    def createSquirrelsTable(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS squirrels (id SERIAL PRIMARY KEY, name VARCHAR(255), size VARCHAR(255))")
        self.connection.commit()

    def getSquirrels(self):
        self.cursor.execute("SELECT * FROM squirrels ORDER BY id")
        return self.cursor.fetchall()

    def getSquirrel(self, squirrelId):
        self.cursor.execute("SELECT * FROM squirrels WHERE id = %s", (squirrelId,))
        return self.cursor.fetchone()

    def createSquirrel(self, data):
        self.cursor.execute("INSERT INTO squirrels (name, size) VALUES (%s, %s)", (data["name"], data["size"]))
        self.connection.commit()
        return None

    def updateSquirrel(self, squirrelId, data):
        self.cursor.execute("UPDATE squirrels SET name = %s, size = %s WHERE id = %s", (data["name"], data["size"], squirrelId))
        self.connection.commit()
        return None

    def deleteSquirrel(self, squirrelId):
        self.cursor.execute("DELETE FROM squirrels WHERE id = %s", (squirrelId,))
        self.connection.commit()
        return None

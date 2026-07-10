from db.db import database

class usermanager():
    def __init__(self):
        self.db=database()

    def create_user(self,username:str):
        self.db.cursor.execute(
            """ SELECT * FROM users WHERE  username=?""",(username,)
        )
        row=self.db.cursor.fetchone()
        if row:
            return row["id"]
        

        self.db.cursor.execute(
            """INSERT INTO users (username) VALUES (?)""",(username,)


        )

        self.db.conn.commit()
        return self.db.cursor.lastrowid
    

    def get_user(self,username:str):
        self.db.cursor.execute(
            """SELECT * FROM users WHERE username= ?""",(username,)

        )

        rows=self.db.cursor.fetchone()
        if rows:
            return dict(rows)
        return None


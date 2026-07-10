from db.db import database

class memorymanager():
    def __init__(self):
        self.db=database()


    def save_memory(self,user_id:str,memory:str,importance:int):
        self.db.cursor.execute(
            """ SELECT * FROM memories WHERE user_id=?""",(user_id,)
        )
        if self.db.cursor.fetchall():
            return False






        self.db.cursor.execute(
            """INSERT INTO memories (user_id,memory,importance) VALUES (?,?,?)""",(user_id,memory,importance,)


        

        )
        self.db.conn.commit()


    def get_memory(self,user_id):
        self.db.cursor.execute(
            """SELECT * FROM memories WHERE user_id = ?""",(user_id,)
        )

        rows=self.db.cursor.fetchall()
        return[dict(row) for row in rows]
    

    

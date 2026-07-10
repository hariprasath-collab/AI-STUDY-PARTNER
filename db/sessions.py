from db.db import database
from uuid import uuid4

class sessionmanager():
    def __init__(self):
        self.db=database()




    def create_session(self,user_id:int,title:str="new chat"):

        session_id=str(uuid4())
        self.db.cursor.execute(
            """ INSERT INTO sessions(user_id,session_id,title) VALUES (?,?,?)""",(user_id,session_id,title,)
            
        )

        self.db.conn.commit()

        return session_id
    

    def get_all_sessions(self,user_id:str):
        self.db.cursor.execute(
            """SELECT * FROM sessions WHERE user_id= ? 
            ORDER BY created_at DESC""",(user_id,)
        )
        rows=self.db.cursor.fetchall()
        return [dict(row) for row in rows]
    


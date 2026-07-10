from db.db import database

class messagemanager():
    def __init__(self):
        self.db=database() 
    def save_message(self,session_id:str,message:str,role:str,model:str):
        self.db.cursor.execute(
            """ INSERT INTO messages (session_id,message,role,model) VALUES (?,?,?,?)"""


        ,(session_id,message,role,model))

        self.db.conn.commit()
        return self.db.cursor.lastrowid
    

    def get_messages(self,session_id:str):
        self.db.cursor.execute(
            """SELECT * FROM messages WHERE session_id=?""",(session_id,)
        )

        rows=self.db.cursor.fetchall()
        return [dict(row) for row in rows]
    

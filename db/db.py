import sqlite3
from pathlib import Path

class database:
    def __init__(self,db_name="database/memory.db"):
        Path("database").mkdir(exist_ok=True)

        self.conn=sqlite3.connect(
            db_name,
            check_same_thread=False
        )
        self.conn.row_factory=sqlite3.Row
        self.cursor=self.conn.cursor()
        self.create_table()


    def create_table(self):
        self.cursor.execute(
            """CREATE TABLE IF NOT EXISTS users(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"""
        )


        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS sessions(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            session_id TEXT UNIQUE NOT NULL,
            title TEXT DEFAULT 'new chat',
            is_fav INTEGER DEFAULT 0 ,
             created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

             FOREIGN KEY(user_id)
             REFERENCES users(id)
             ON DELETE CASCADE)"""
        )

        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT NOT NULL,
            message TEXT NOT NULL,
            role TEXT NOT NULL,
            model TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

            )"""
        )
        self.cursor.execute(
            """ CREATE TABLE IF NOT EXISTS memories(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            memory TEXT NOT NULL,
            importance INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
             
              
            FOREIGN KEY(user_id)
            REFERENCES users(id)
            ON DELETE CASCADE )"""
        )
    
        
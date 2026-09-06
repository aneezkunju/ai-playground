from contextlib import asynccontextmanager
import sqlite3
from fastapi import FastAPI

DB_FILE ="movies.db"

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database...")
    db= sqlite3.connect(DB_FILE)

    db.execute("""
     CREATE TABLE IF NOT EXISTS  movie_directors (
     id INTEGER PRIMARY KEY AUTOINCREMENT,
     name TEXT NOT NULL,
     movie TEXT NOT NULL
     )
     """)
    db.commit()
    app.state.db=db
    yield
    print ("closing db")
    db.close()
    
app = FastAPI(lifespan=lifespan)
@app.get("/")
async def root():
    return {"message":"movie search api"}

@app.post("/directors")
async def add_director(name:str, movie: str) :
    db = app.state.db
    cursor = db.execute(
        """
        INSERT INTO movie_directors ( name, movie)
        VALUES (?,?)
        """,
        (name,movie)
    )
    db.commit()
    return {
        "id":cursor.lastrowid,
        "name": name,
        "movie": movie
    }
@app.get("/directors")
async def get_directors():
    db = app.state.db
    cursor = db.execute(
        "SELECT  id, name, movie  FROM movie_directors"
    )
    rows = cursor.fetchall()
    return [
        {
            "id":row[0],
            "name": row[1],
            "movie": row[2]
        }
        for row in rows
    ]
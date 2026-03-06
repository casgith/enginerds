from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2

app = FastAPI()

# Enable CORS to allow requests from your frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE_URL = os.getenv("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def read_root():
    return {"message": "Backend is running!"}

@app.post("/start")
def start_quiz(nickname: str = Query(...)):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        nickname TEXT PRIMARY KEY,
        counter INT
    )
    """)

    cur.execute("SELECT counter FROM users WHERE nickname=%s", (nickname,))
    result = cur.fetchone()

    if result:
        counter = result[0] + 1
        cur.execute("UPDATE users SET counter=%s WHERE nickname=%s", (counter, nickname))
    else:
        counter = 1
        cur.execute("INSERT INTO users VALUES (%s,%s)", (nickname, counter))

    conn.commit()
    cur.close()
    conn.close()

    return {"nickname": nickname, "counter": counter}
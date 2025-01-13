from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

app = FastAPI()

# Update CORS settings with the correct URL
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://zealous-stone-02173020f.4.azurestaticapps.net"  # Your actual Azure Static Web App URL
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db_connection():
    max_retries = 3
    for attempt in range(max_retries):
        try:
            return psycopg2.connect(
                host=os.getenv('PGHOST'),
                database=os.getenv('PGDATABASE'),
                user=os.getenv('PGUSER'),
                password=os.getenv('PGPASSWORD'),
                port=os.getenv('PGPORT', '5432'),
                connect_timeout=30,
                cursor_factory=RealDictCursor
            )
        except psycopg2.OperationalError as e:
            if attempt == max_retries - 1:
                print(f"Failed to connect after {max_retries} attempts: {e}")
                raise HTTPException(status_code=500, detail="Database connection failed")
            print(f"Connection attempt {attempt + 1} failed, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff

@app.get("/")
async def root():
    return {"message": "F1 API is running"}

@app.get("/api/standings")
async def get_standings():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM f1_driver_standing ")
        results = cur.fetchall()
        cur.close()
        conn.close()
        return list(results)
    except Exception as e:
        print(f"Error fetching standings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
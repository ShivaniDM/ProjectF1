from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from dotenv import load_dotenv
import time
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

app = FastAPI()

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "https://zealous-stone-02173020f.4.azurestaticapps.net"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

def get_db_connection():
    """Create a database connection with retry logic"""
    max_retries = 3
    retry_delay = 2  # seconds
    
    # Log environment variables (excluding password)
    logger.info(f"Attempting connection to: {os.getenv('PGHOST')}:{os.getenv('PGPORT', '5432')}")
    logger.info(f"Database: {os.getenv('PGDATABASE')}")
    logger.info(f"User: {os.getenv('PGUSER')}")

    for attempt in range(max_retries):
        try:
            connection = psycopg2.connect(
                host=os.getenv('PGHOST'),
                database=os.getenv('PGDATABASE'),
                user=os.getenv('PGUSER'),
                password=os.getenv('PGPASSWORD'),
                port=os.getenv('PGPORT', '5432'),
                connect_timeout=30,
                cursor_factory=RealDictCursor
            )
            logger.info("Database connection successful")
            return connection
        except psycopg2.OperationalError as e:
            if attempt == max_retries - 1:
                logger.error(f"Failed to connect after {max_retries} attempts: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail=f"Database connection failed after {max_retries} attempts"
                )
            logger.warning(f"Connection attempt {attempt + 1} failed, retrying in {retry_delay} seconds")
            time.sleep(retry_delay * (attempt + 1))  # Exponential backoff

@app.get("/")
async def root():
    return {"message": "F1 API is running"}

@app.get("/api/standings")
async def get_standings():
    """Get F1 standings from database"""
    try:
        logger.info("Processing /api/standings request")
        conn = get_db_connection()
        cur = conn.cursor()
        
        logger.info("Executing standings query")
        cur.execute("SELECT * FROM f1_driver_standing")
        results = cur.fetchall()
        
        logger.info(f"Query returned {len(results)} results")
        return list(results)
    
    except Exception as e:
        logger.error(f"Error in get_standings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if 'cur' in locals():
            cur.close()
        if 'conn' in locals():
            conn.close()
            logger.info("Database connection closed")

@app.get("/api/test-connection")
async def test_connection():
    """Test database connectivity"""
    try:
        conn = get_db_connection()
        conn.close()
        return {"status": "success", "message": "Database connection test successful"}
    except Exception as e:
        logger.error(f"Connection test failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
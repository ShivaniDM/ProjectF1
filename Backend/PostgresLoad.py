from Extract import *
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Access environment variables with defaults for development
pg_host = os.getenv('PGHOST', 'your-server.postgres.database.azure.com')
pg_user = os.getenv('PGUSER', 'your-username')
pg_password = os.getenv('PGPASSWORD', 'your-password')
pg_database = os.getenv('PGDATABASE', 'your-database')
pg_port = os.getenv('PGPORT', '5432')

# List of functions to process and upload
functions = [f1_driver_standing]

def create_connection_string(host, user, password, database, port):
    # Create a safe connection string without need for additional encoding
    return f'postgresql://{user}:{password}@{host}:{port}/{database}'

try:
    # Create connection string
    conn_string = create_connection_string(pg_host, pg_user, pg_password, pg_database, pg_port)
    
    # Create database engine
    print("Creating database engine...")
    db = create_engine(conn_string)
    
    # Establish database connection
    print("Connecting to database...")
    conn = db.connect()
    
    # Loop through functions and push data
    for fun in functions:
        function_name = fun.__name__
        print(f"Executing {function_name}...")
        result_df = fun()
        
        print(f"Pushing data for {function_name}...")
        result_df.to_sql(function_name, con=conn, if_exists='replace', index=False)
        print(f'Successfully pushed data for {function_name}')
    
except Exception as e:
    print(f"Error occurred: {str(e)}")
    raise
finally:
    if 'conn' in locals():
        conn.close()
        print("Database connection closed")
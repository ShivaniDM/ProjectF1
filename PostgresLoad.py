from Extract import *
import pandas as pd
from sqlalchemy import create_engine
import psycopg2
import os


# Access environment variables
pg_host = os.getenv('PGHOST')
pg_user = os.getenv('PGUSER')
pg_password = os.getenv('PGPASSWORD')
pg_database = os.getenv('PGDATABASE')

# List of functions to process and upload
functions = [f1_driver_standing]
# Retrieve the database connection string from environment variables
conn_string = f'postgresql://{pg_user}:{pg_password}@{pg_host}:5432/{pg_database}'

# Create a database engine
db = create_engine(conn_string)

# Establish a database connection
conn = db.connect()

# Loop through the list of functions and push data to the database
for fun in functions:
    # Get the name of the current function
    function_name = fun.__name__
    
    # Call the function to get the DataFrame
    result_df = fun()
    
    # Push the DataFrame to the database table with the function name as the table name
    result_df.to_sql(function_name, con=conn, if_exists='replace', index=False)
    
    # Print a message indicating data has been pushed for the current function
    print(f'Pushed data for {function_name}')

# Close the database connection
conn.close()

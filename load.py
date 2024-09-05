from Extract import *  # Imports functions from extract.py
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from io import BytesIO
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from dotenv import load_dotenv
import os

# Load environment variables from a .env file
load_dotenv()

# List of functions to process and upload
functions = [f1_driver_standing]

# Function to upload data to Azure Blob Storage
def to_blob(func):
    """ Converts the output of a given function to Parquet format and uploads it to Azure Blob Storage.
    Args:
        func (function): The function that retrieves data to be processed and uploaded.
    Returns:
        None
    """
    # Getting the name of the function
    file_name = func.__name__

    # Calling the function to retrieve data
    df = func()

    # Converting DataFrame to Arrow Table
    table = pa.Table.from_pandas(df)

    # Creating a buffer to store Parquet data
    parquet_buffer = BytesIO()

    # Writing the Arrow Table data to the buffer in Parquet format
    pq.write_table(table, parquet_buffer)

    # Retrieving Azure Blob Storage connection string and container name from environment variables
    connection_string = os.getenv('AZURE_STORAGE_CONNECTION_STRING')
    container_name = os.getenv('AZURE_CONTAINER_NAME')

    # Creating a Blob Service Client
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)

    # Specifying blob name
    blob_name = f"{file_name}.parquet"

    # Creating a Container Client
    container_client = blob_service_client.get_container_client(container_name)

    # Creating a Blob Client
    blob_client = container_client.get_blob_client(blob_name)

    # Uploading Parquet data to Azure Blob Storage
    parquet_buffer.seek(0)  # Ensure buffer's cursor is at the beginning
    blob_client.upload_blob(parquet_buffer, overwrite=True)

    # Printing a success message
    print(f"{blob_name} successfully uploaded")

# Loop through the list of functions and upload data
for item in functions:
    to_blob(item)

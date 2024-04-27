import os
import boto3
from botocore.exceptions import ClientError
import time
import concurrent.futures

# Example usage parameters
bucket_name = 'mp3project-bucket'  # S3 bucket name
s3_folder = 'audio/test'  # Folder in the S3 bucket to download files from
local_folder_path = '../../data/download_s3_directory'  # Local directory to save downloaded files
aws_region = 'us-east-2'  # AWS region of the S3 bucket
max_workers = min(50, os.cpu_count() + 4)  # Maximum number of concurrent download threads

# AWS Credentials - Ping me for the KEY, please do not commit the key to github
aws_access_key_id = 'YOUR_ACCESS_KEY'
aws_secret_access_key = 'YOUR_SECRET_KEY' 

def download_file(s3_client, bucket_name, s3_key, local_path):
    try:
        s3_client.download_file(bucket_name, s3_key, local_path)
        print(f"Successfully downloaded {s3_key} to {local_path}.")
    except Exception as e:
        print(f"Failed to download {s3_key}. Error: {e}")

def download_files(bucket_name, s3_folder, local_folder_path, aws_region):
    print("Starting download...")
    
    # Start timing
    start_time = time.time()
    
    # Ensure the local folder exists
    os.makedirs(local_folder_path, exist_ok=True)
    
    # Create an S3 client with the specified region and credentials
    s3 = boto3.client('s3', region_name=aws_region, 
                      aws_access_key_id=aws_access_key_id, 
                      aws_secret_access_key=aws_secret_access_key)

    # List objects in the specified S3 folder
    objects = s3.list_objects_v2(Bucket=bucket_name, Prefix=s3_folder)

    # Use ThreadPoolExecutor to download files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures = []
        if 'Contents' in objects:
            for obj in objects['Contents']:
                s3_key = obj['Key']
                local_file_name = os.path.basename(s3_key)
                local_path = os.path.join(local_folder_path, local_file_name)
                # Schedule the file to be downloaded using a thread
                futures.append(executor.submit(download_file, s3, bucket_name, s3_key, local_path))
            
            # Wait for all futures to complete
            for future in concurrent.futures.as_completed(futures):
                future.result()  # This will re-raise any exceptions caught

    # End timing
    end_time = time.time()
    print(f"Finished downloading. Time taken: {end_time - start_time:.2f} seconds.")

download_files(bucket_name, s3_folder, local_folder_path, aws_region)

import os
import boto3
from botocore.exceptions import ClientError
import time
import concurrent.futures

# Example usage
folder_path = '/Users/bach/Documents/MP3-Project/test/archive (1)'  # Update this to your folder path
s3_folder = 'audio/test'  # Folder within the S3 bucket
bucket_name = 'mp3project-bucket'  # Update this to your S3 bucket name
aws_region = os.environ.get('AWS_REGION', 'us-east-2')  # Use AWS_REGION environment variable if set, else default
max_workers = min(50, os.cpu_count() + 4)

def upload_file(s3_client, bucket_name, s3_key, full_path):
    try:
        s3_client.upload_file(full_path, bucket_name, s3_key)
        print(f"Successfully uploaded {full_path} to {bucket_name}/{s3_key}.")
    except Exception as e:
        print(f"Failed to upload {full_path}. Error: {e}")

def upload_files(folder_path, bucket_name, aws_region, s3_folder):
    print("Starting upload...")
    
    # Start timing
    start_time = time.time()
    
    # Create an S3 client with the region
    s3 = boto3.client('s3', region_name=aws_region)

    # Use ThreadPoolExecutor to upload files in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers) as executor:
        futures = []
        for subdir, dirs, files in os.walk(folder_path):
            for file in files:
                full_path = os.path.join(subdir, file)
                s3_key = os.path.join(s3_folder, os.path.relpath(full_path, folder_path))
                # Schedule the file to be uploaded using a thread
                futures.append(executor.submit(upload_file, s3, bucket_name, s3_key, full_path))
        
        # Wait for all futures to complete
        for future in concurrent.futures.as_completed(futures):
            future.result()  # This will re-raise any exceptions caught

    # End timing
    end_time = time.time()
    print(f"Finished uploading. Time taken: {end_time - start_time:.2f} seconds.")

upload_files(folder_path, bucket_name, aws_region, s3_folder)

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import csv


def upload_file(api_base_url, file_path, upload_path):
    """
    Upload a single MP3 file to an S3 bucket through an API Gateway using HTTP PUT requests.
    Returns a tuple (file_name, response_status_code, response_text, file_size).
    """
    file_name = os.path.basename(file_path)
    key = f"{upload_path}%2F{file_name}"
    api_url = f"{api_base_url}?key={key}"
    file_size = os.path.getsize(file_path)  # Get file size

    with open(file_path, 'rb') as file:
        headers = {'Content-Type': 'audio/mpeg'}
        response = requests.put(api_url, headers=headers, data=file)
        return file_name, response.status_code, response.text, file_size

def upload_files_concurrently(api_base_url, folder_path, upload_path, max_workers=10):
    """
    Uploads all MP3 files from a specified folder and its subfolders to an S3 bucket through an API Gateway using concurrent uploads.
    Measures total upload time and size.
    Additionally, creates a CSV file listing all successfully uploaded files.
    """
    start_time = time.time()  # Start timer
    total_size = 0  # Initialize total size
    futures = []
    uploaded_files = []  # List to store names of successfully uploaded files

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for root, _, files in os.walk(folder_path):
            for file_name in files:
                if file_name.endswith('.mp3'):
                    file_path = os.path.join(root, file_name)
                    futures.append(executor.submit(upload_file, api_base_url, file_path, upload_path))

        for future in as_completed(futures):
            file_name, status_code, response_text, file_size = future.result()
            if status_code == 200:
                print(f"Uploaded {file_name} successfully.")
                total_size += file_size  # Accumulate successful upload sizes
                uploaded_files.append(file_name)  # Add file name to the list of uploaded files
            else:
                print(f"Failed to upload {file_name}. Status code: {status_code}, Response: {response_text}")

    elapsed_time = time.time() - start_time  # Calculate elapsed time
    print(f"Total upload time: {elapsed_time:.2f} seconds")
    print(f"Total size uploaded: {total_size / (1024 * 1024):.2f} MB")
    
    # After uploading, create a CSV file with the names of uploaded files
    csv_file_path = os.path.join(folder_path, 'listing.csv')
    with open(csv_file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        for file_name in uploaded_files:
            writer.writerow([file_name])
    
    # Optionally, upload the CSV file to the S3 bucket
    csv_key = f"{upload_path}"  # Adjust as needed
    upload_file(api_base_url, csv_file_path, csv_key)

if __name__ == "__main__":
    api_base_url = 'Ping Bach For the URL'
    folder_path = './test'  # Adjust this path as needed
    upload_path = 'mp3project-bucket/audio/test'  # Your specific folder in the S3 bucket
    upload_files_concurrently(api_base_url, folder_path, upload_path, max_workers=15)
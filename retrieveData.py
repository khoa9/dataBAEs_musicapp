#bach Download script

# /data /
#It downloads to download_s3_directory

import csv
import requests
import os
import time
from concurrent.futures import ThreadPoolExecutor, as_completed


def download_file(api_base_url, download_path, local_folder_path, file_name):
    """
    Downloads a single file from an S3 bucket through an API Gateway using HTTP GET requests.
    Returns the size of the downloaded file in bytes.
    
    Parameters:
    - api_base_url: The base URL of the API Gateway endpoint.
    - download_path: The path in the S3 bucket where the file is located.
    - local_folder_path: The local folder path where the file will be saved.
    - file_name: The name of the file to download.
    """
    key = f"{download_path}%2F{file_name}"
    api_url = f"{api_base_url}?key={key}"
    local_file_path = os.path.join(local_folder_path, file_name)

    response = requests.get(api_url, stream=True)
    if response.status_code == 200:
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Downloaded {file_name} successfully.")
        return os.path.getsize(local_file_path)  # Return the size of the downloaded file
    else:
        print(f"Failed to download {file_name}. Status code: {response.status_code}")
        return 0  # Return 0 if the download failed

def download_files_from_listing(api_base_url, download_path, local_folder_path, listing_file_name='listing.csv'):
    """
    Downloads files listed in a CSV from an S3 bucket to a local folder.
    Prints the total download time and the total size of the files downloaded.
    
    Parameters:
    - api_base_url: The base URL of the API Gateway endpoint.
    - download_path: The path in the S3 bucket where the files are located.
    - local_folder_path: The local folder path where files will be saved.
    - listing_file_name: The name of the CSV file that lists the files to download.
    """
    start_time = time.time()  # Start the timer
    total_size = 0  # Initialize the total size of the files downloaded
    # Determine the optimal number of threads for parallel downloading
    max_workers = 10

    # First, download the listing.csv file
    listing_file_path = os.path.join(local_folder_path, listing_file_name)
    total_size += download_file(api_base_url, download_path, local_folder_path, listing_file_name)

    # Read the listing.csv file to get the list of files
    with open(listing_file_path, mode='r', newline='') as file:
        reader = csv.reader(file)
        file_names = [row[0] for row in reader]

    # Download each file listed in the CSV using concurrent requests
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {executor.submit(download_file, api_base_url, download_path, local_folder_path, name): name for name in file_names}
        for future in as_completed(futures):
            file_size = future.result()
            total_size += file_size  # Accumulate the size of each file downloaded

    elapsed_time = time.time() - start_time
    print(f"Total download time: {elapsed_time:.2f} seconds")
    print(f"Total size downloaded: {total_size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    api_base_url = 'Ping Bach for API'
    download_path = 'mp3project-bucket/audio/test'  # Path in the S3 bucket
    local_folder_path = './data'  # Local folder path

    # Ensure the local directory exists
    if not os.path.exists(local_folder_path):
        os.makedirs(local_folder_path)

    # Download files listed in the CSV and measure download time and size
    download_files_from_listing(api_base_url, download_path, local_folder_path)

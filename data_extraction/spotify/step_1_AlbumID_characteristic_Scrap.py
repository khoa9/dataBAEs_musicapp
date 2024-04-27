import csv
import json
import os
from bs4 import BeautifulSoup

# Use this code to get all Album ID from a folder set of HTML. Basically webscrapping. 
# Will need a folder of html saved from Rateyourmusic.com (Chart). For example, https://rateyourmusic.com/charts/top/album/all-time/g:hip%2dhop/
# Folder Structure should be: HTML/subfolder(s)
# Paths
directory_path = '/Users/bach/Documents/MP3-Project/ID-Scrap/html_dump/diversity'
output_csv_path = '/Users/bach/Documents/MP3-Project/ID-Scrap/Album_ID_Dump/extracted_spotify_ids_diversity.csv'

def extract_spotify_ids_and_characteristics(html_content, genre):
    soup = BeautifulSoup(html_content, 'lxml')
    media_links = soup.find_all('div', class_="page_charts_section_charts_item")

    spotify_ids = []  # Use a list to maintain order

    for item in media_links:
        data_links = item.find('div', id=lambda x: x and 'media_link_button_container_charts' in x)
        if data_links:
            data_links = data_links.get('data-links', '').replace('&quot;', '"')
            try:
                media_links_json = json.loads(data_links)
                if 'spotify' in media_links_json:
                    for spotify_id in media_links_json['spotify'].keys():
                        # Extract characteristics
                        characteristics_div = item.find('div', class_='page_charts_section_charts_item_genre_descriptors')
                        if characteristics_div:
                            characteristics = [span.text for span in characteristics_div.find_all('span', class_='comma_separated')]
                        else:
                            characteristics = []
                        spotify_ids.append((spotify_id, genre, characteristics))  # Pair ID with genre and characteristics
            except json.JSONDecodeError:
                print("Error decoding JSON from data-links.")
    return spotify_ids

# Dictionary to keep track of Spotify IDs with their first associated genre and characteristics
spotify_ids_with_genres_characteristics = {}

# Process each HTML file in the directory
for filename in sorted(os.listdir(directory_path)):
    if filename.endswith(".html"):
        genre = " ".join(filename.split("_")[:-1]).strip()  # Extract genre from the filename
        file_path = os.path.join(directory_path, filename)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                html_content = file.read()
                ids_with_genres_characteristics = extract_spotify_ids_and_characteristics(html_content, genre)
                for spotify_id, genre, characteristics in ids_with_genres_characteristics:
                    if spotify_id not in spotify_ids_with_genres_characteristics:
                        spotify_ids_with_genres_characteristics[spotify_id] = (genre, characteristics)
                        print(f'Spotify ID {spotify_id} with genre {genre} and characteristics {characteristics} extracted from {filename}.')
                else:
                    print(f"No Spotify IDs extracted from {filename}.")
        except FileNotFoundError:
            print(f"File not found: {file_path}")
        except Exception as e:
            print(f"An unexpected error occurred while processing {filename}: {e}")

# Write the collected Spotify IDs to a CSV file, including genre and characteristics
with open(output_csv_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Spotify ID', 'Genre', 'Characteristics'])  # Writing header row
    for spotify_id, (genre, characteristics) in spotify_ids_with_genres_characteristics.items():
        # Convert characteristics list to string
        characteristics_str = ', '.join(characteristics)
        writer.writerow([spotify_id, genre, characteristics_str])  # Write each unique ID with genre and characteristics as a string

print(f"Unique Spotify IDs with genres and characteristics have been saved to {output_csv_path}.")

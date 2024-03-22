import pandas as pd
import shutil
import os

books = pd.read_csv("./data/bookReadsInput/goodreads_book.csv")
genre = pd.read_csv("./data/bookReadsInput/description + genre.csv")
ratings_book = pd.read_csv("./data/bookReadsInput/ratings_book.csv")
items = pd.read_csv("./data/bookReadsInput/items_movie.csv")
ratings =  pd.read_csv("./data/bookReadsInput/ratings_movie.csv")
new_image_urls = pd.read_csv("./data/bookReadsInput/image_urls.csv")

ratings_2024 = pd.read_csv("./data/bookReadsInput/rating_2024.csv")
ratings_2024 = ratings_2024.drop(columns=['goodreads_book_id'])


ratings_book = ratings_book._append(ratings_2024, ignore_index=True)

#num_rows = books.shape[0]
#print("Number of rows:", num_rows)

#common_rows_count = books['book_id'].isin(ratings_book['book_id']).sum()
#print("Number of common rows based on ID:", common_rows_count)

genre.rename(columns={'main genre': 'main_genre'}, inplace=True)

merged_df = pd.merge(genre, books, on='goodreads_book_id', how='inner')

#get correct urls
url_mapping = dict(zip(new_image_urls['goodreads_book_id'], new_image_urls['image']))
merged_df['image_url'] = merged_df['goodreads_book_id'].map(url_mapping).fillna(merged_df['image_url'])

#num_rows = merged_df.shape[0]
#print("Number of rows:", num_rows)

#Function to remove brackets and extract filename
'''def extract_filename(url1):
    #url_without_brackets = url_with_brackets[1:-1]
    filename = os.path.basename(url1)
    return filename

# Apply the function to the entire 'URL' column
merged_df['image_url'] = merged_df['image_url'].apply(lambda x: extract_filename(x))
#books['imageURLHighRes'] = books['imageURLHighRes'].apply(lambda x: extract_filename(x))
'''
'''
def extract_after_last_two_slashes(url):
    return '/'.join(url.rsplit('/', 2)[-2:])


merged_df['image_url'] = merged_df['image_url'].apply(extract_after_last_two_slashes)
'''

merged_df = merged_df.dropna()
merged_df['publication_year'] = merged_df['publication_year'].astype(int)


# Get the column names
#column_names = merged_df.columns.tolist()
#c_names = items.columns.to_list()
# Print the column names
#print(c_names)
#print(column_names)

items['id'] = merged_df['book_id']
items['tmdb_id'] = merged_df['goodreads_book_id']
items['vote_average'] = merged_df['average_rating']
items['vote_count'] = merged_df['ratings_count']
items['overview']=merged_df['description']
items['genres'] = merged_df['main_genre']
items['title'] = merged_df['original_title']
items['youtubeId']= merged_df['image_url']
items['poster_path']= merged_df['image_url']
items['year']=merged_df['publication_year']

items['vote_count'] = items['vote_count'].str.replace(',','')

#column_names1 = ratings_book.columns.tolist()
#c_names1 = ratings.columns.to_list()
# Print the column names
#print(c_names1)
#print(column_names1)



ratings['movie_id'] = ratings_book['book_id']
ratings['rating'] = ratings_book['rating']


items.to_csv('./data/bookReadsInput/items.csv', index=False)  # Set index=False if you don't want to write row indices to the file

# Convert df2 to CSV
ratings.to_csv('./data/bookReadsInput/ratings.csv', index=False)



# Source and destination file paths
items_file = './data/bookReadsInput/items.csv'
ratings_file = './data/bookReadsInput/ratings.csv'
destination_folder = './data/'

# Copy the file
shutil.copy(items_file, destination_folder)
shutil.copy(ratings_file, destination_folder)



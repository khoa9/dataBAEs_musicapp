import os
import mp3_to_vector_transformation

def create_input(completed_df):
    output_folder = 'data/'
    file_name = f'{output_folder}/music_vector_metadata.json'  
    # Create the output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True) 
    # Convert DataFrame to JSON and save each row as a separate file
    '''for index, row in completed_df.iterrows():     
        json_data = row.to_json()     
    # You can customize the file name as needed'''
    json_data = completed_df.to_json(orient='records')
    with open(file_name, 'w') as f:
        f.write(json_data)
    #End A json file - store to data folder
    
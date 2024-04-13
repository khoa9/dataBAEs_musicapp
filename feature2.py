import numpy as np
from tensorflow.keras.models import load_model # type: ignore

def characteristic_predict(music_vector, model_name):
    loaded_model = load_model(model_name)

    labels =['Calm/Peaceful', 'Dark/Intense', 'Energetic/Excited', 'Happy/Positive', 'Mysterious/Abstract', 'Romantic/Emotional', 'Sad/Negative', 'Thoughtful/Contemplative']
    
    music_vector = np.array(music_vector)
    test_data = music_vector.reshape(1,-1)
    
    predictions = loaded_model.predict(test_data)
    flattened_array = (predictions.flatten() > 0.5).astype(int)  # Assuming sigmoid output
    
    indices_with_ones = [index for index, value in enumerate(flattened_array) if value == 1]
    selected_labels = [labels[index] for index in indices_with_ones]
    
    moodless =['neutral', 'ambient']
    
    return selected_labels if selected_labels else moodless

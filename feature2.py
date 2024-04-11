import pickle
import numpy as np

def characteristic_predict(music_vector, model_name):
    '''
    This function is use to predict all the characteristics of a song based on its vector
    
    Parameters:
    - music_vector: music file after being embedded into flat vector
    - model_name: name of the classifier model
    '''
    
    with open(model_name, 'rb') as file:
        loaded_model = pickle.load(file)

    labels = ['aggressive', 'angry', 'anxious', 'bittersweet', 'calm',
       'chaotic', 'cold', 'conscious', 'dark', 'depressive', 'eclectic',
       'energetic', 'epic', 'ethereal', 'existential', 'happy', 'heavy',
       'hypnotic', 'introspective', 'lethargic', 'lonely', 'longing', 'love',
       'lush', 'manic', 'meditative', 'melancholic', 'mellow', 'mysterious',
       'noisy', 'ominous', 'optimistic', 'passionate', 'peaceful',
       'pessimistic', 'playful', 'romantic', 'sad', 'scary', 'sensual',
       'sentimental', 'sexual', 'soft', 'sombre', 'soothing', 'surreal',
       'suspenseful', 'uplifting', 'warm']
    
    test_data = music_vector.reshape(1,-1)
    
    predictions = loaded_model.predict(test_data)
    
    flattened_array=predictions.toarray().flatten()
    
    indices_with_ones = [index for index, value in enumerate(flattened_array) if value == 1]

    # Map indices to labels
    selected_labels = [labels[index] for index in indices_with_ones]
    
    moodless =['neutral',' ambient']
    
    if len(selected_labels) > 0:
        return selected_labels
    else:
        return moodless



"""import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import joblib

# Load the KMeans model
kmeans = joblib.load('kmeans_model.pkl')

def predict_cluster(user_input, kmeans_model):
    # Assuming user_input is a dictionary containing input data
    input_data = np.array([[
        user_input['Danceability'],
        user_input['Energy'],
        user_input['Key'],
        user_input['Loudness'],
        user_input['Mode'],
        user_input['Speechiness'],
        user_input['Acousticness'],
        user_input['Instrumentalness'],
        user_input['Liveness'],
        user_input['Valence'],
        user_input['Tempo']
    ]])
    
    # Predict the cluster for the input data
    predicted_cluster = kmeans.predict(input_data)
    
    # Return the predicted cluster
    return predicted_cluster[0]

"""

import numpy as np
import joblib

# Load the KMeans model
kmeans = joblib.load('kmeans_model.pkl')

def predict_cluster(user_input, kmeans_model):
    # Assuming user_input is a dictionary containing input data
    input_data = np.array([
        user_input['Danceability'],
        user_input['Energy'],
        user_input['Key'],
        user_input['Loudness'],
        user_input['Mode'],
        user_input['Speechiness'],
        user_input['Acousticness'],
        user_input['Instrumentalness'],
        user_input['Liveness'],
        user_input['Valence'],
        user_input['Tempo']
    ]).reshape(1, -1)  # Reshape the input data to 2D array

    # Predict the cluster for the input data
    predicted_cluster = kmeans.predict(input_data)

    # Return the predicted cluster
    return predicted_cluster[0]

"""import streamlit as st
import pandas as pd
from kmeans_predict import predict_cluster
from kmeans_model import kmeans
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set your Spotify API credentials
client_id = "5e6f15d0c5de4bfa97265277b9e4c4f4"
client_secret = "120e71d99cb14996a9f7758b7ceba586"


client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Load your trained KMeans model and your dataset here
# kmeans = load_your_kmeans_model()
# tracks_df = load_your_dataset()

st.title('Music Cluster Predictor')

# User input section
st.sidebar.header('User Input')
artist_name = st.sidebar.text_input('Enter Artist Name')
track_name = st.sidebar.text_input('Enter Track Name')
# Add other input fields for Track ID, Danceability, Energy, etc., as needed

results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track', limit=1)

# Extract track ID from search results
if results['tracks']['items']:
    track_id = results['tracks']['items'][0]['id']

    # Get audio analysis for the track
    audio_analysis = sp.audio_analysis(track_id)

    # Print the audio analysis data
    print(audio_analysis)

else:
    print("Track not found.")

if st.sidebar.button('Predict Cluster'):
    if artist_name and track_name:  # Check if both fields are filled out
        # Prepare user input as a DataFrame (similar to how you prepared your initial dataset)
        user_input = pd.DataFrame({
            'Artist Name': [artist_name],
            'Track Name': [track_name],
            # Add other columns and their corresponding user input values here
        })

        # Assuming you have a function 'predict_cluster' to predict cluster for user input
        predicted_cluster = "predict_cluster(user_input, kmeans)"  # Call your function to predict cluster

        st.write('Predicted Cluster:', predicted_cluster)
    else:
        st.write('Please enter both Artist Name and Track Name.')
"""

import streamlit as st
import pandas as pd
from kmeans_predict import predict_cluster
from kmeans_model import kmeans
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Set your Spotify API credentials
client_id = "YOUR_CLIENT_ID"
client_secret = "YOUR_CLIENT_SECRET"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

st.title('Music Cluster Predictor')

# User input section
st.sidebar.header('User Input')
artist_name = st.sidebar.text_input('Enter Artist Name')
track_name = st.sidebar.text_input('Enter Track Name')

if st.sidebar.button('Predict Cluster'):
    if artist_name and track_name:  # Check if both fields are filled out
        # Search for the track using Spotipy
        results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track', limit=1)
        
        # Extract track ID from search results
        if results['tracks']['items']:
            track_id = results['tracks']['items'][0]['id']

            # Get audio features for the track
            audio_features = sp.audio_features(track_id)[0]

            # Prepare user input as a DataFrame
            user_input = pd.DataFrame({
                'Danceability': [audio_features['danceability']],
                'Energy': [audio_features['energy']],
                'Key': [audio_features['key']],
                'Loudness': [audio_features['loudness']],
                'Mode': [audio_features['mode']],
                'Speechiness': [audio_features['speechiness']],
                'Acousticness': [audio_features['acousticness']],
                'Instrumentalness': [audio_features['instrumentalness']],
                'Liveness': [audio_features['liveness']],
                'Valence': [audio_features['valence']],
                'Tempo': [audio_features['tempo']]
            })
            st.write('Audio features:', user_input)
            # Predict cluster using the KMeans model
            predicted_cluster = predict_cluster(user_input, kmeans)

            st.write('Predicted Cluster:', predicted_cluster)
        else:
            st.write('Track not found.')
    else:
        st.write('Please enter both Artist Name and Track Name.')

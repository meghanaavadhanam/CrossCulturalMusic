"""import streamlit as st
Network link: http://10.0.0.175:8501
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
from sklearn.neighbors import NearestNeighbors

# Set your Spotify API credentials
client_id = "5e6f15d0c5de4bfa97265277b9e4c4f4"
client_secret = "120e71d99cb14996a9f7758b7ceba586"

client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)



st.title('Cross Cultural Music Recommendation System 🎵')

tracks_df = pd.read_csv("filled_tracks.csv")
features = tracks_df[['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness',
            'Instrumentalness', 'Liveness', 'Valence', 'Tempo','Cluster']]

# User input section
st.sidebar.header('Explore your musical horizons here!')
artist_name = st.sidebar.text_input('Enter Artist Name')
track_name = st.sidebar.text_input('Enter Track Name')


if st.sidebar.button('Give me interesting recommendations!'):
    if artist_name and track_name:  # Check if both fields are filled out
        # Search for the track using Spotipy
        results = sp.search(q=f"track:{track_name} artist:{artist_name}", type='track', limit=1)
        
        artist_results = sp.search(q=f"artist:{artist_name}", type='artist', limit=1)
        artist = artist_results['artists']['items'][0]
        artist_image_url = artist['images'][0]['url'] if artist['images'] else None

        music_image_url = artist_image_url

        # Display the music-related image
        st.image(music_image_url, caption='Artist Icon', use_column_width=True)  

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

            st.write('\n\nPredicted Cluster:', predicted_cluster)

            # Filter tracks in the same cluster
            #cluster_tracks = tracks_df[tracks_df['Cluster'] == predicted_cluster]

            data_scaled=tracks_df.copy(deep=True)

            k = 6  # Number of nearest neighbors
            model = NearestNeighbors(n_neighbors=k)
            model.fit(data_scaled[data_scaled['Cluster'] == predicted_cluster].iloc[:,8:-1])

            test_data_scaled = user_input

            distances, indices = model.kneighbors(test_data_scaled)


            row_indices = indices[0]  # Assuming you're working with a single test data point

            #list_of_indices = [int(indices[0])]
            list_of_indices = indices[0].tolist()
            #print(list_of_indices)
            # recommended_songs=[]
            # for i in list_of_indices:

            #     recommended_song_info = tracks_df[tracks_df['Cluster'] == predicted_cluster].iloc[i][["Artist Name", "Track Name", "Track Link"]]
            #     artist_in_dataset = recommended_song_info["Artist Name"]
            #     track_in_dataset = recommended_song_info["Track Name"]

            #     if (artist_in_dataset != artist_name) or (track_in_dataset != track_name):
            #         recommended_songs.append(recommended_song_info)
            recommended_songs=[]
            for i in list_of_indices:
                    recommended_song = tracks_df[tracks_df['Cluster'] == predicted_cluster].iloc[i][["Artist Name", "Track Name", "Track Link"]]
                    recommended_songs.append(recommended_song)


            # Print top songs in the cluster
            st.write('\n\nSimilar Songs:')
            # for i, row in enumerate(recommended_song):
            st.write(f"**1. Artist:** {recommended_songs[1][0]}, **Track:** {recommended_songs[1][1]}, \n\nOpen with Spotify:{recommended_songs[1][2]}")
            st.write(f"**2. Artist:** {recommended_songs[2][0]}, **Track:** {recommended_songs[2][1]}, \n\nOpen with Spotify:{recommended_songs[2][2]}")
            st.write(f"**3. Artist:** {recommended_songs[3][0]}, **Track:** {recommended_songs[3][1]}, \n\nOpen with Spotify:{recommended_songs[3][2]}")
            st.write(f"**4. Artist:** {recommended_songs[4][0]}, **Track:** {recommended_songs[4][1]}, \n\nOpen with Spotify:{recommended_songs[4][2]}")
            st.write(f"**5. Artist:** {recommended_songs[5][0]}, **Track:** {recommended_songs[5][1]}, \n\nOpen with Spotify:{recommended_songs[5][2]}")

        else:
            st.write('Track not found.')
    else:
        st.write('Please enter both Artist Name and Track Name.')

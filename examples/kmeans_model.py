import pandas as pd
from sklearn.cluster import KMeans
import numpy as np
import matplotlib.pyplot as plt
import joblib



filled_tracks_df = pd.read_csv("/Users/meghanaavadhanam/Documents/filled_tracks.csv", encoding='utf-8')

features = filled_tracks_df[['Danceability', 'Energy', 'Key', 'Loudness', 'Mode', 'Speechiness', 'Acousticness',
            'Instrumentalness', 'Liveness', 'Valence', 'Tempo','Cluster']]

# Number of clusters (you can adjust this based on your preference)
num_clusters = 10


data_scaled = filled_tracks_df.copy()
kmeans = KMeans(n_clusters=num_clusters, random_state=24)

kmeans.fit(features.iloc[:,:-1])

#filled_tracks_df['Cluster'] = kmeans.fit_predict(features)

#filled_tracks_df.to_csv("/Users/meghanaavadhanam/Documents/filled_tracks.csv", encoding='utf-8')

#predicted_cluster = kmeans.predict([user_input_features])[0]
joblib.dump(kmeans, 'kmeans_model.pkl')



import joblib
import numpy as np
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
from fuzzywuzzy import process
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.neighbors import NearestNeighbors
import json

app = Flask(__name__)

# Load the trained models and data
cv = joblib.load("count_vectorizer.joblib")
svd = joblib.load("svd.joblib")
ann_model = joblib.load("ann_model.joblib")
indices = joblib.load("indices.joblib")
game_dict = pickle.load(open("game_dict.pkl", "rb"))

df1 = pd.DataFrame(game_dict)

# Function to recommend games
def recommend(game_name, about_game):
    # Check if the game exists in the dataset
    best_match = process.extractOne(game_name, df1['Name'].tolist(), score_cutoff=80) if game_name else None
    
    if best_match:
        matched_game = best_match[0]
        game_index = df1[df1['Name'] == matched_game].index[0]
        similar_games_indices = indices[game_index, 1:6]  # Get top 5 recommendations
        return [df1.iloc[idx].Name for idx in similar_games_indices]
    
    # If game is not found, generate recommendations based on 'about_game'
    if about_game.strip():  # Ensure it's not empty
        input_vector = cv.transform([about_game]).toarray()
        reduced_vector = svd.transform(input_vector)
        distances, nearest_indices = ann_model.kneighbors(reduced_vector)
        return [df1.iloc[idx].Name for idx in nearest_indices[0]]

    return []  # Return empty list if no valid input

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

@app.route('/About')
def about():
    return render_template('about.html')

@app.route("/predict", methods=['POST'])
def predict():
    features = request.json

    game_name = features.get("name", "").strip()
    age = features.get("age", "").strip()
    genres = features.get("genres", [])  # Ensure it's treated as a list
    categories = features.get("category", "").strip()
    developers = features.get("developers", "").strip()
    about_game = features.get("about", "").strip()

    # Construct the 'about_game' feature for similarity matching
    about_game = " ".join(filter(None, [", ".join(genres), categories, developers, about_game]))

    if not game_name and not about_game:
        return jsonify({"error": "No game name or description provided!"}), 400

    recommended_games = recommend(game_name, about_game)

    if not recommended_games:
        return jsonify({"error": "No recommendations found!"}), 400

    return jsonify({"recommendations": recommended_games})

@app.route("/after")
def after():
    games = request.args.get("games", "[]")  # Get the games from URL
    try:
        games = json.loads(games)  # Convert string back to list
    except json.JSONDecodeError:
        games = []  # If parsing fails, set an empty list
    return render_template("after.html", recommendations=games)

if __name__ == "__main__":
    app.run(debug=True)
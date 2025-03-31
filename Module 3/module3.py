import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import MinMaxScaler

def load_json(file_path):
    data = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            try:
                data.append(json.loads(line))
            except json.JSONDecodeError:
                continue  # Skip lines that aren't valid JSON
    return pd.DataFrame(data)

def preprocess_data(df):
    df = df[['title', 'genres', 'rating']].dropna()
    df['genres'] = df['genres'].apply(lambda x: ' '.join(x) if isinstance(x, list) else '')
    df['imdb_rating'] = df['rating'].apply(lambda x: x.get('avg', 0) if isinstance(x, dict) else 0)
    df['features'] = df['genres']
    return df

def compute_similarity(df):
    vectorizer = TfidfVectorizer()
    feature_matrix = vectorizer.fit_transform(df['features'])
    rating_scaler = MinMaxScaler()
    scaled_ratings = rating_scaler.fit_transform(df[['imdb_rating']])
    
    similarity_matrix = cosine_similarity(feature_matrix) * 0.8 + scaled_ratings * 0.2
    return similarity_matrix

def get_similar_movies(df, similarity_matrix, movie_title, top_n=10):
    if movie_title not in df['title'].values:
        return "Movie not found in database."
    
    movie_index = df.index[df['title'] == movie_title].tolist()
    if not movie_index:
        return "Movie not found in database."
    
    movie_index = movie_index[0]
    similarity_scores = list(enumerate(similarity_matrix[movie_index]))
    sorted_movies = sorted(similarity_scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
    
    return df.iloc[[i[0] for i in sorted_movies]][['title', 'genres', 'imdb_rating']]

if __name__ == "__main__":
    file_path = "imdb_movies_2000to2022.prolific copy.json"  
    df = load_json(file_path)
    df = preprocess_data(df)
    similarity_matrix = compute_similarity(df)
    
    movie_title = "Kate & Leopold"
    similar_movies = get_similar_movies(df, similarity_matrix, movie_title)
    print(f"Top similar movies to {movie_title}:")
    print(similar_movies)
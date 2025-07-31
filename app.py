import streamlit as st
import pickle
import requests

# TMDb API key
API_KEY = "8fdd1b859b3fcab1831cd99e107ed4e4"

# Load the movie list and similarity matrix
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))

# Fetch poster from TMDb
def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "application/json"
        }
        response = requests.get(url, headers=headers, timeout=5)

        if response.status_code != 200:
            print(f"TMDb API Error: {response.status_code}")
            return "https://via.placeholder.com/500x750?text=Error"

        data = response.json()
        if data['results']:
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
        return "https://via.placeholder.com/500x750?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print("Network error:", e)
        return "https://via.placeholder.com/500x750?text=Network+Error"

# Recommend movies and fetch their posters
def recommend(movie_title):
    index = movies[movies['title'] == movie_title].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movies = []
    recommended_posters = []

    for i in distances[1:6]:  # Skip the first (it's the same movie)
        movie_name = movies.iloc[i[0]].title
        recommended_movies.append(movie_name)
        recommended_posters.append(fetch_poster(movie_name))

    return recommended_movies, recommended_posters

# Streamlit app UI
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title(" Movie Recommender System with Posters")

selected_movie = st.selectbox("Search for a movie", movies['title'].values)

if st.button("Show Recommendations"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])

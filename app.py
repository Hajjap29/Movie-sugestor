
import streamlit as st
import requests

# Replace with your TMDb API key
API_KEY = 'your_tmdb_api_key'
BASE_URL = 'https://api.themoviedb.org/3'

# Define the genres (or fetch dynamically from API)
genres = {
    'Action': 28,
    'Comedy': 35,
    'Drama': 18,
    'Horror': 27,
    'Sci-Fi': 878,
    'Romance': 10749
}

# Function to get movies by genre
def get_movies_by_genre(genre_id):
    url = f"{BASE_URL}/discover/movie?with_genres={genre_id}&api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    return response.json()['results']

# Streamlit interface
st.title("Movie Recommendation Bot")
st.subheader("Select your preferred genre")

genre = st.selectbox("Pick a genre:", options=list(genres.keys()))

if genre:
    genre_id = genres[genre]
    movies = get_movies_by_genre(genre_id)
    
    if movies:
        st.write(f"Here are some {genre} movies you might like:")
        for movie in movies[:5]:  # Display top 5 results
            st.write(f"- {movie['title']} ({movie['release_date']})")
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=150)
            st.write(f"Overview: {movie['overview']}")
    else:
        st.write("Sorry, no movies found.")

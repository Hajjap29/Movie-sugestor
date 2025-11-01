import streamlit as st
import requests

# Page configuration
st.set_page_config(
    page_title="Movie Recommendation Bot",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .movie-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# Replace with your TMDb API key
API_KEY = 'a5e8107417cd31e23594cd68d17f6815'
BASE_URL = 'https://api.themoviedb.org/3'

# Define the genres
genres = {
    'Action': 28,
    'Adventure': 12,
    'Animation': 16,
    'Comedy': 35,
    'Crime': 80,
    'Documentary': 99,
    'Drama': 18,
    'Family': 10751,
    'Fantasy': 14,
    'History': 36,
    'Horror': 27,
    'Music': 10402,
    'Mystery': 9648,
    'Romance': 10749,
    'Science Fiction': 878,
    'Thriller': 53,
    'War': 10752,
    'Western': 37
}

# Function to get movies by genre
def get_movies_by_genre(genre_id, page=1):
    try:
        url = f"{BASE_URL}/discover/movie"
        params = {
            'with_genres': genre_id,
            'api_key': API_KEY,
            'language': 'en-US',
            'sort_by': 'popularity.desc',
            'page': page
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()['results']
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching movies: {e}")
        return []
    except KeyError:
        st.error("Invalid API key or response format. Please check your TMDb API key.")
        return []

# Function to get movie details
def get_movie_details(movie_id):
    try:
        url = f"{BASE_URL}/movie/{movie_id}"
        params = {
            'api_key': API_KEY,
            'language': 'en-US'
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except:
        return None

# Title and description
st.title("🎬 Movie Recommendation Bot")
st.markdown("Discover amazing movies based on your favorite genres!")

st.divider()

# Sidebar for filters
with st.sidebar:
    st.header("🎯 Filters")
    
    # Genre selection
    selected_genre = st.selectbox(
        "Select Genre:",
        options=list(genres.keys()),
        index=0
    )
    
    # Number of movies to display
    num_movies = st.slider(
        "Number of movies to show:",
        min_value=3,
        max_value=20,
        value=5,
        step=1
    )
    
    st.divider()
    
    st.markdown("""
    ### 📖 About
    This app uses [The Movie Database (TMDb)](https://www.themoviedb.org/) API 
    to suggest movies based on your preferred genre.
    
    **Get your free API key:**
    1. Sign up at [TMDb](https://www.themoviedb.org/)
    2. Go to Settings → API
    3. Request an API key
    """)

# Main content
if selected_genre:
    genre_id = genres[selected_genre]
    
    # Add a search button
    if st.button("🔍 Get Recommendations", type="primary", use_container_width=True):
        with st.spinner(f"Finding {selected_genre} movies..."):
            movies = get_movies_by_genre(genre_id)
        
        if movies:
            st.success(f"Found {len(movies)} {selected_genre} movies!")
            st.markdown(f"### Top {min(num_movies, len(movies))} {selected_genre} Movies")
            
            # Display movies
            for idx, movie in enumerate(movies[:num_movies], 1):
                col1, col2 = st.columns([1, 3])
                
                with col1:
                    # Display poster
                    if movie.get('poster_path'):
                        poster_url = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"
                        st.image(poster_url, use_container_width=True)
                    else:
                        st.info("No poster available")
                
                with col2:
                    # Movie title and year
                    release_year = movie.get('release_date', 'N/A')[:4] if movie.get('release_date') else 'N/A'
                    st.markdown(f"### {idx}. {movie['title']} ({release_year})")
                    
                    # Rating
                    rating = movie.get('vote_average', 0)
                    st.markdown(f"⭐ **Rating:** {rating}/10 ({movie.get('vote_count', 0)} votes)")
                    
                    # Overview
                    overview = movie.get('overview', 'No overview available.')
                    st.markdown(f"**Overview:** {overview}")
                    
                    # Link to TMDb
                    movie_id = movie.get('id')
                    if movie_id:
                        tmdb_link = f"https://www.themoviedb.org/movie/{movie_id}"
                        st.markdown(f"[View on TMDb]({tmdb_link})")
                
                st.divider()
        else:
            st.warning(f"No {selected_genre} movies found. Please check your API key.")
else:
    st.info("👈 Select a genre from the sidebar and click 'Get Recommendations' to start!")

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>Powered by <a href='https://www.themoviedb.org/'>The Movie Database (TMDb)</a></p>
    </div>
""", unsafe_allow_html=True)

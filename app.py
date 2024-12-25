import streamlit as st
import requests
import pickle
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
base_url = "https://api.themoviedb.org/3/search/movie"


movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    for i in movies_list:
        recommend_movies.append(movies.iloc[i[0]].title)
    return recommend_movies

def get_movie_poster(query):
    params = {
        "api_key": api_key,
        "query": query,
        "language": "en-US",
    }
    response = requests.get(base_url, params=params)
    data = response.json()

    if data['results']:
        movie = data['results'][0]
        title = movie['title']
        poster_path = movie['poster_path']
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return title, poster_url
    else:
        return None, None

st.markdown("""
    <h1 style='text-align: center; color: green;'>
        Movie Recommendation System
    </h1>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        .stButton button {
            border: 2px solid green;  /* Change border color to green */
            color: green;  /* Button text color */
        }
        .stButton button:hover {
            background-color: #e6ffe6;  /* Light green background on hover */
        }
    </style>
""", unsafe_allow_html=True)

movies_list = movies['title'].values
movie_option = st.selectbox("Select a movie to get recommendations:", movies_list)

if st.button("Recommend"):
    recommendations = recommend(movie_option)
    st.write(f"Recommended Movies based on '{movie_option}':")
    columns = st.columns(5)
    for idx, movie in enumerate(recommendations):
        title, poster_url = get_movie_poster(movie)
        if title and poster_url:
            with columns[idx % 5]:
                st.image(poster_url, caption=title, use_container_width=True)
        else:
            with columns[idx % 5]:
                st.error(f"Could not fetch poster for {movie}")

st.markdown("""
    <style>
        .footer {
            position: fixed;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100%;
            background-color: #f8f9fa;
            color: #212529;
            text-align: center;
            padding: 10px 0;
            font-size: 14px;
        }
        .footer a {
            color: #007bff;
            text-decoration: none;
        }
        .footer a:hover {
            text-decoration: underline;
        }
        @media screen and (max-width: 600px) {
            .footer {
                font-size: 16px;
                padding: 8px 0;
            }
        }
    </style>
    <div class="footer">
        This Website Developed by <b>Ahmad Husain</b> ❤️ | <a href="https://github.com/Ahmad007Designer" target="_blank">GitHub</a>
    </div>
""", unsafe_allow_html=True)

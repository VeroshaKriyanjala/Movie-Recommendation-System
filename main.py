import streamlit as st
import pickle
import requests

# Load movies and similarity matrices
movies = pickle.load(open("movies_list.pkl", 'rb'))
similarity = pickle.load(open("similarity.pkl", 'rb'))
movies_list = movies["title"].values

st.header("Movie Recommender System")
select_value = st.selectbox("Select a movie", movies_list)

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=0739c163f44ac6051b4a97a7f4470ba3"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return None

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda vector: vector[1])
    recommend_movie = []
    recommend_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommend_movie.append(movies.iloc[i[0]].title)
        recommend_poster.append(fetch_poster(movie_id))
    return recommend_movie, recommend_poster

if st.button("Recommend"):
    movie_name, movie_poster = recommend(select_value)
    cols = st.columns(5)
    for col, name, poster in zip(cols, movie_name, movie_poster):
        with col:
            st.text(name)
            st.image(poster if poster else "https://via.placeholder.com/150")  # Placeholder if no poster

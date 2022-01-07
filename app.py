import pickle
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = 'https://api.themoviedb.org/3/movie/{}?api_key=1d9d3bf949730339fae27ff846aecffc&language=en-US'.format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = 'https://image.tmdb.org/t/p/w500/' + poster_path
    return full_path


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names_ = []
    recommended_movie_posters_ = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters_.append(fetch_poster(movie_id))
        recommended_movie_names_.append(movies.iloc[i[0]].title)
    return recommended_movie_names_, recommended_movie_posters_


st.title('Movie Recommendation System')
st.text('~ by Sakib Chonka')

movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = tuple(movies['title'].values)

selected_movie = st.selectbox(
    'Type or Select a Movie',
    movie_list
)
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    i = 0
    for col in st.columns(5):
        with col:
            st.write(recommended_movie_names[i])
            st.image(recommended_movie_posters[i])
        i += 1

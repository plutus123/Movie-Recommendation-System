import streamlit as st
import pickle
import pandas as pd
import numpy as np
import requests


url = "https://api.themoviedb.org/3/trending/movie/day?language=en-US"

mov = pickle.load(open("movies_overview.pkl", "rb"))
m = pd.DataFrame(mov)


def fetch_poster(movie_id):

    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=353e5fee8ad23a873c3205bf9174b018&language=en-US".format(movie_id))
    data=response.json()
    print(data)
    return "https://image.tmdb.org/t/p/original" + data["poster_path"]
def recommend(movie):
    movie_index = movies[movies["title"] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:

        movie_id=movies.iloc[i[0]].id

        recommended_movies.append((movies.iloc[i[0]]).title)
        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movie_id))


    return recommended_movies , recommended_movies_posters

movies_dict = pickle.load(open("movies_list.pkl", "rb"))
movies = pd.DataFrame(movies_dict)


def download_file_from_drive():
    try:
        
        response = requests.get("https://drive.google.com/file/d/1muMzugjmHpQcMxNS0Wn-_V4kiY4DH0Dg/view?usp=sharing")
        response.raise_for_status()  # This will raise an HTTPError if the request returns an unsuccessful status code

        with open('similarity.pkl', 'wb') as f:
            f.write(response.content)

    except Exception as e:
        st.error(f"An error occurred while downloading the file: {e}")

download_file_from_drive()


similarity = None
try:
    similarity = pickle.load(open("similarity.pkl", "rb"))
except Exception as e:
    st.error(f"An error occurred while loading the similarity data: {e}")


# similarity = pickle.load(open("similarity.pkl", "rb"))

st.title("Movie Recommendation System")

import streamlit.components.v1 as components

imageCarouselComponent = components.declare_component("image-carousel-component", path="frontend/public")

imageUrls = [
    fetch_poster(1632),
    fetch_poster(299536),
    fetch_poster(17455),
    fetch_poster(2830),
    fetch_poster(429422),
    fetch_poster(9722),
    fetch_poster(13972),
    fetch_poster(240),
    fetch_poster(155),
    fetch_poster(598),
    fetch_poster(914),
    fetch_poster(255709),
    fetch_poster(572154)

]

imageCarouselComponent(imageUrls=imageUrls, height=200)
selected_movie_name = st.selectbox(
':red[Movies similar to]',
(movies["title"].values)
)

m_list=movies["title"].to_list()

st.header('''
    :red[Movie Name]''')


st.markdown(f'*{selected_movie_name}*')

movie_index=m_list.index(selected_movie_name)


st.header('''
    :red[Genre]''')

st.markdown(f'*{m["genre"][movie_index]}*')


st.header('''
    :red[Overview]''')

st.markdown(f'*{m["overview"][movie_index]}* ')



if st.button('Recommend'):
    names , posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])

        st.image(posters[0])

    with col2:
        st.text(names[1])

        st.image(posters[1])

    with col3:
        st.text(names[2])

        st.image(posters[2])
    with col4:
        st.text(names[3])

        st.image(posters[3])
    with col5:
        st.text(names[4])

        st.image(posters[4])






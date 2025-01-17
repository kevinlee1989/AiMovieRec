import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '9e0299fe9f84bae0698cb802144778b1'

# getting the recommendations movie_list function
def get_recommendations(title):
    # Getting the index of movie based on the movie title
    idx = movies[movies['title'] == title].index[0]

    # Getting the data corresponding to the cosin_similarity as (idx, cosine_sim)
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Make descending order 
    sim_scores = sorted(sim_scores, key = lambda x:x[1], reverse=True)

    # Slicing the recommendation movie without itself
    sim_scores = sim_scores[1:11]

    # Extract the 10 recommendation movie's index 
    movie_indices = [i[0] for i in sim_scores]

    # Extract the movie title by index information
    images = []
    titles = []
    for i in movie_indices:
        id = movies['id'].iloc[i]
        details = movie.details(id) # There are a lot of detail information


        # Check if poster_path is valid
        image_path = details['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else: # if there is no image_path
            image_path = '이재우 여권사진.jpg'

        images.append(image_path)
        titles.append(details['title'])

    return images, titles


movies = pickle.load(open('movies.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

# Build the web
st.set_page_config(layout = 'wide')
st.header('Welcome to the Movie Recommendation Web')

movie_list = movies['title'].values
title = st.selectbox('Choose a movie you love', movie_list)
if st.button('Recommendation'):
    # make the progress bar for visualization
    with st.spinner('Please wait...'):
        images, titles = get_recommendations(title)

        # Show on the web application
        idx = 0
        for i in range(0, 2):
            cols = st.columns(5) # making 5 columns
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1

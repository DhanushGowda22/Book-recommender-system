import pickle
import streamlit as st
import numpy as np
import requests

def fetch_poster(book_name):
    url = f"http://www.omdbapi.com/?t={book_name}&apikey=YOUR_API_KEY"
    data = requests.get(url).json()
    return data.get('Poster', '')
st.markdown("""
<style>
img {
    border-radius: 12px;
    transition: transform 0.2s;
}

img:hover {
    transform: scale(1.08);
}
</style>
""", unsafe_allow_html=True)
st.markdown("<h1 style='text-align:center;'>Book Recommender System </h1>", unsafe_allow_html=True)
st.write("")
st.markdown(
    "<h2 style='text-align:center;'>This system recommends books using collaborative filtering based on user ratings.</h2>",
    unsafe_allow_html=True
)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = pickle.load(open(os.path.join(BASE_DIR, 'artifacts/model.pkl'), 'rb'))
book_names = pickle.load(open(os.path.join(BASE_DIR, 'artifacts/book_names.pkl'), 'rb'))
final_rating = pickle.load(open(os.path.join(BASE_DIR, 'artifacts/final_rating.pkl'), 'rb'))
book_pivot = pickle.load(open(os.path.join(BASE_DIR, 'artifacts/book_pivot.pkl'), 'rb'))

def fetch_poster(suggestion):

    book_name = []
    ids_index = []
    poster_url = []

    for book_id in suggestion[0]:
        book_name.append(book_pivot.index[book_id])

    for name in book_name:
        ids = np.where(final_rating['Book-Title'] == name)[0][0]
        ids_index.append(ids)

    for idx in ids_index:
        url = final_rating.iloc[idx]['Image-URL-L']
        poster_url.append(url)

    return poster_url


def recommend_book(book_name):

    books_list = []

    book_id = np.where(book_pivot.index == book_name)[0][0]

    distance, suggestion = model.kneighbors(
        book_pivot.iloc[book_id,:].values.reshape(1,-1),
        n_neighbors=6
    )

    poster_url = fetch_poster(suggestion)

    for i in suggestion[0]:
        books_list.append(book_pivot.index[i])

    return books_list, poster_url


selected_books = st.selectbox(
    "Type or select a book from the dropdown",
    book_names
)

if st.button('Show Recommendation'):
    st.subheader("Recommended Books")

    recommended_books, poster_url = recommend_book(selected_books)

    for book in recommended_books:
        st.write(book)

st.markdown("---")
st.markdown(
    "<div style='text-align:center'>Built by <b>Dhanush</b> | Machine Learning Project </div>",
    unsafe_allow_html=True
)

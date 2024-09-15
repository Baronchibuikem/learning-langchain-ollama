# import components.generate_pet_name as gpn
# import streamlit as st

# st.title('Pet Name Generator')

# animal_type = st.sidebar.selectbox("What is your pet?", ("Cat", "Dog", "Cow", "Hampter"))

# if animal_type == "Cat":
#     pet_color = st.sidebar.text_area(label="What color is your cat?",  max_chars=15)

# if animal_type == "Dog":
#     pet_color = st.sidebar.text_area(label="What color is your dog?",  max_chars=15)

# if animal_type == "Cow":
#     pet_color = st.sidebar.text_area(label="What color is your cow?",  max_chars=15)

# if animal_type == "Hampter":
#     pet_color = st.sidebar.text_area(label="What color is your hamster?",  max_chars=15)

# if pet_color:
#     reponse = gpn.generate_pet_name(animal_type=animal_type, pet_color=pet_color)
#     st.text(reponse)

import streamlit as st
import agents_tutorial.youtube_analyzer as lch
import textwrap

st.title("YouTube Assistant")

with st.sidebar:
    with st.form(key='my_form'):
        youtube_url = st.sidebar.text_area(
            label="What is the YouTube video URL?",
            max_chars=50
            )
        query = st.sidebar.text_area(
            label="Ask me about the video?",
            max_chars=50,
            key="query"
            )
        "[View the source code](https://github.com/Baronchibuikem/learning-langchain-ollama/)"
        submit_button = st.form_submit_button(label='Submit')

if query and youtube_url:
    if not youtube_url or not query:
        st.info("Please add a youtube url and search query.")
        st.stop()
    else:
        db = lch.create_db_from_youtube_video_url(youtube_url)
        response, docs = lch.get_response_from_query(db, query)
        st.subheader("Answer:")
        st.text(textwrap.fill(response, width=85))
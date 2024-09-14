import components.generate_pet_name as gpn
import streamlit as st

st.title('Pet Name Generator')

animal_type = st.sidebar.selectbox("What is your pet?", ("Cat", "Dog", "Cow", "Hampter"))

if animal_type == "Cat":
    pet_color = st.sidebar.text_area(label="What color is your cat?",  max_chars=15)

if animal_type == "Dog":
    pet_color = st.sidebar.text_area(label="What color is your dog?",  max_chars=15)

if animal_type == "Cow":
    pet_color = st.sidebar.text_area(label="What color is your cow?",  max_chars=15)

if animal_type == "Hampter":
    pet_color = st.sidebar.text_area(label="What color is your hamster?",  max_chars=15)

if pet_color:
    reponse = gpn.generate_pet_name(animal_type=animal_type, pet_color=pet_color)
    st.text(reponse)
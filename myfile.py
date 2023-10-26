import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

st.title ("Heating Consumption of Trams in Zürich")

st.header("How many trams do you have? Would you sell any because I need one for personal use!")
st.divider()
number_trams = st.slider('Number of trams', 0, 130, 25)
st.write("I have that many trams. ", number_trams)

st.write("How many would you give me?")

number = st.number_input("Insert a number", value=None, placeholder="Type a number...")
st.write('The current number is ', number)

image = Image.open('Tram.jpeg')

st.image(image, caption='Tram in Zürich')


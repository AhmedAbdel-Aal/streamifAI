"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from aws import get_data_2
from recommender import recommendation
from PIL import Image



#opening the image
image = Image.open('./logo-black.png')

#displaying the image on streamlit app
st.image(image, caption='Enter any caption here')




picture = st.camera_input("Take a picture")

vector = None
rec = None 
msg = None

if picture:
    st.image(picture)    
    with open ('some_image.jpg','wb') as file:
          file.write(picture.getbuffer())
    vector = get_data_2()
    try:
        pubinput=[['the lord of the rings: the two towers',0.2],['the lord of the rings: the two towers',0.7],['the lord of the rings: the two towers',0.1]]
        rec=recommendation(vector,'')   
    except :
        msg = "problem with recommender"


vector, rec
    


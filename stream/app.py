"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from aws import get_data_2

picture = st.camera_input("Take a picture")

vector = None

if picture:
    st.image(picture)    
    with open ('some_image.jpg','wb') as file:
          file.write(picture.getbuffer())
    vector = get_data_2()

vector
    


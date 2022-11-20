"""
# My first app
Here's our first attempt at using data to create a table:
"""

import streamlit as st
import pandas as pd
from aws import get_data_2
from recommender import recommendation
from PIL import Image
from pathlib import Path


#opening the image
logo = "https://raw.githubusercontent.com/AhmedAbdel-Aal/streamifAI/main/stream/logo-black.png"

#displaying the image on streamlit app
st.image(logo)




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
    except Exception as e:
        msg = "problem with recommender" + str(e)

base_path = Path(__file__).parent
file1 = Path(base_path, "clean_data.csv")
file2 = Path(base_path, "clean_numerical_data.csv")
file3= Path(base_path, "clean_no_rating_data.csv")

base_path,Path(base_path, "clean_data.csv"),Path(base_path, "clean_data.csv").is_file(), vector, rec, msg
    


import boto3
import base64
import streamlit as st

def save_img(base):
    #open text file
    text_file = open("./file_base.txt", "w")

    #write string to file
    text_file.write(base)

    #close file
    text_file.close()

    file = open('file_base.txt', 'rb')
    encoded_data = file.read()
    file.close()

    imgdata = base64.b64decode((encoded_data))
    #print(imgdata)
    filename = 'some_image.jpg'  # I assume you have a way of picking unique filenames
    with open(filename, 'wb') as f:
        f.write(imgdata)

def recognize():
    rekognition = boto3.client('rekognition',aws_access_key_id=st.secrets["keys"]["aws_access_key_id"],
                 aws_secret_access_key=st.secrets["keys"]["aws_secret_access_key"], region_name=st.secrets["keys"]["region_name"])

    with open('some_image.jpg', 'rb') as image_data:
         response_content = image_data.read()
    return  rekognition.detect_faces(Image={'Bytes':response_content}, Attributes=['ALL'])

def get_emotion_type(emotion_vector):
    most_probable_emotion = None
    temp_conf = 0
    for emotion in emotion_vector['Emotions']:
        if emotion['Confidence'] > temp_conf:
            most_probable_emotion = emotion['Type']
            temp_conf = emotion['Confidence'] 
    return most_probable_emotion


def get_vector_from_face(face):
    vector = {
    "age_range_low": face['AgeRange']['Low'],
    "age_range_high": face['AgeRange']['High'],
    "smile": face['Smile']['Value'],
    "gender": face['Gender']['Value'],
    "emotion": get_emotion_type(face)
    }
    return vector

def get_all_vectors(rekognition_response):
    faces_vectors = []
    for face in rekognition_response['FaceDetails']:
        faces_vectors.append(get_vector_from_face(face))
    return faces_vectors



def get_data(base):
    print('----------------------------------------------------------------')
    save_img(base)
    rekognition_response = recognize()
    return   get_all_vectors(rekognition_response)

def get_data_2():
    rekognition_response = recognize()
    return   get_all_vectors(rekognition_response)

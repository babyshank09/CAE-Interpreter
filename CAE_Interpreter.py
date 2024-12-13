import os 
import dotenv  
from dotenv import load_dotenv
import google.generativeai as genai  
import streamlit as st
from PIL import Image

load_dotenv('api.env') 
gemini_api_key= os.getenv("GEMINI_PRO")

genai.configure(api_key= gemini_api_key) 
llm= genai.GenerativeModel("gemini-1.5-flash") 

st.set_page_config(page_title="CAE Image Interpretation Application") 
st.title("CAE Image Interpreter") 
st.subheader("An Application to Analyse and Interpret CAE Images")  

st.sidebar.title("Settings")
uploaded_images= st.sidebar.file_uploader("Upload your images", type=["jpg", "jpeg", "png"], accept_multiple_files=True) 


if uploaded_images is not None:  
    images=[]
    for image in uploaded_images:  
        img= Image.open(image) 
        images.append(img)  

    st.image(images, caption=["Uploaded Image"]*len(images), use_column_width=True)  


system_prompt= '''
You are an expert Mechanical Engineer especailly in domains like structural and thermal engineering. Answer the query to 
the best of your abilities. Dont provide general information. The information should be relevant to the picture given. Query: 
'''
query= st.text_input("Ask me anything", placeholder="Describe the image") 
final_prompt= [system_prompt+query]

def generate_response(llm, prompt, input_images):    
    prompt.extend(input_images)
    response= llm.generate_content(prompt)  
    return response.text

if st.button("Analyse"):  
    if query !="":  
        res= generate_response(llm= llm, prompt= final_prompt, input_images=images) 
        st.write(res) 
    else: 
        st.write("Please provide your query")
























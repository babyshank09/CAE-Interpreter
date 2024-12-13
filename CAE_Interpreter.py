import os 
import dotenv  
from dotenv import load_dotenv
import google.generativeai as genai  
import streamlit as st
from PIL import Image

load_dotenv('api.env') 

st.set_page_config(page_title="CAE Image Interpretation Application") 
st.title("CAE Image Interpreter") 
st.subheader("An Application to Analyse and Interpret CAE Images")  

st.sidebar.title("Settings") 
gemini_api_key= st.sidebar.text_input("Enter your API key", type="password")
uploaded_images= st.sidebar.file_uploader("Upload your images", type=["jpg", "jpeg", "png"], accept_multiple_files=True) 

genai.configure(api_key= gemini_api_key) 
llm= genai.GenerativeModel("gemini-1.5-flash") 


if uploaded_images is not None:  
    images=[]
    for image in uploaded_images:  
        img= Image.open(image)  
        #resized_img= img.resize((500,500))
        images.append(img)  

    st.image(images, caption=["Uploaded Image"]*len(images), use_container_width=True )  


system_prompt= '''
You are an expert Mechanical Engineer especailly in the domain of structural engineering.The user will provide you certain images 
of certain geometries. Analyse the geometry by calculating the number of pixels for each geometric parameter. You dont need to give the 
value of the geometric dimension but rather just use it to compare the dimensions and sizes of the geometric parameters. After comparing them, 
answer the query to the best of your abilities. Dont provide general information. Be specific and technical. Query: 
'''
query= st.text_area("Ask me anything", placeholder="Describe the image") 
final_prompt= [system_prompt+query]

def generate_response(llm, prompt, input_images):    
    prompt.extend(input_images)
    response= llm.generate_content(prompt)  
    return response.text

if st.button("Generate Response"):  
    if query !="":  
        res= generate_response(llm= llm, prompt= final_prompt, input_images=images) 
        st.write(res) 
    else: 
        st.write("Please provide your query")




























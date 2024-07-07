import streamlit as st
from openai import OpenAI
from streamlit_pdf_viewer import pdf_viewer
from api import api
from example import example
from pypdf import PdfReader 
import re
from streamlit_navigation_bar import st_navbar

#-----------------------------------------------------------CSS-----------------------------------------------------------------------------

st.set_page_config(page_title="Resume Analyzer", page_icon="📃", layout="wide")

def MyBG_colour(wch_colour): 
    my_colour = f"<style> .stApp {{background-color: {wch_colour};}} </style>"
    st.markdown(my_colour, unsafe_allow_html=True)

MyBG_colour("#DEDDFD")  # or pass in the hex code: Eg. MyBG_colour("#90CAF9")


pages =["","","","","","","","",""]
styles = {
    "nav": {
        "background-color": "#DEDDFD",
    }}
page = st_navbar(pages, styles=styles)
st.write(page)


#-----------------------------------------------------------CSS-----------------------------------------------------------------------------




st.header(":blue[Resume Analyser]", divider='violet')


file , info = st.columns([1.5,1])

with file:
    st.subheader(":grey[Get your resume score now,]")
    st.write(":gray[Get your resume reviewed in an instant. Scan your resume for issues and receive detailed pointers on how to improve it instantly. Compare your resume against others in our database and identify areas for enhancement.]")
 
    input = st.text_area(":grey[Enter your job description]")
    if not input:
        st.info(":grey[Enter the job description]")


    pdf_file = st.file_uploader(":grey[Upload PDF file]", type=('pdf'))


with info: 

    if input and pdf_file:
        binary_data = pdf_file.getvalue()
        pdf_viewer(input=binary_data,
                    width=400,
                    pages_to_render=[1])
    else:
    
        st.image("img.png",use_column_width=True,)



    def pdf_to_text(pdf_file) :
        if pdf_file:
            reader = PdfReader(pdf_file)
            print(len(reader.pages)) 
            page = reader.pages[0] 
            text = page.extract_text()
            return text


    text = pdf_to_text(pdf_file)

    def clean_text(text):
        if pdf_file:
            # Remove non-ASCII characters
            text = re.sub(r'[^\x00-\x7F]+', ' ', text)
            # Remove newlines and tabs
            text = re.sub(r'[\r|\n|\r\n]+', ' ', text)
            text = re.sub(r'\s+', ' ', text).strip()
            return text

    text = clean_text(text)


    response = None

    client = OpenAI(
    api_key=api['key'],
    )

    if input and pdf_file:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": """You are an expert HR Manager skilled in analyzing resumes, especially in calculating ATS (Applicant Tracking System) scores based on given job descriptions. Your task is to read the provided resume and 
                                            1. Provide accurate ATS score for the given resume out of 100 in bold letters.
                                            2. Also provide all the suggetions to improve first then under a different heading explain your suggetions with example."""},
                {"role": "user", "content": f"This is the job description {input}, And this is the content of the resume {text}"}
            ],
            temperature=1,
            top_p = 0.3,

        )
        response = completion.choices[0].message.content
                              
    if input and pdf_file :  
        st.write(response)

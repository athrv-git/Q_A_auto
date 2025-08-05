import pandas as pd
import streamlit as st
from io import BytesIO

@st.cache_data
def read_questions_from_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    
    if df.empty or 'label' not in df.columns:
        raise ValueError("Excel file does not contain a 'label' column.")
    
    questions = df['label'].dropna().astype(str).tolist()
    return questions

def save_answers_to_excel(questions, answers):
    df = pd.DataFrame({"Question": questions, "Answer": answers})
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Q&A")
    output.seek(0)
    return output


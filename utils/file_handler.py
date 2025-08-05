import pandas as pd
import streamlit as st
from io import BytesIO

@st.cache_data
def read_questions_from_excel(file):
    df = pd.read_excel(file, engine="openpyxl")
    if df.empty or df.shape[1] == 0:
        raise ValueError("Excel file does not contain any columns.")
    questions = df.iloc[:, 0].dropna().astype(str).tolist()
    return questions

def save_answers_to_excel(questions, answers):
    df = pd.DataFrame({"Question": questions, "Answer": answers})
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Q&A")
    output.seek(0)
    return output

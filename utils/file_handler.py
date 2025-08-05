import pandas as pd
import streamlit as st

@st.cache_data
def read_questions_from_excel(file):
    df = pd.read_excel(file)
    if df.empty or df.shape[1] == 0:
        raise ValueError("Excel file does not contain any columns.")
    questions = df.iloc[:, 0].dropna().tolist()
    return questions

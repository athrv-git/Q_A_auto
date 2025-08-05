import streamlit as st
from utils.file_handler import read_questions_from_excel

st.set_page_config(page_title="Excel Q&A App", layout="wide")
st.title("📄 Excel-Based Question Answer Form")

# Upload Section
uploaded_file = st.file_uploader("Upload an Excel file (questions in the first column)", type=["xlsx"])

if uploaded_file:
    with st.spinner("Reading questions..."):
        try:
            questions = read_questions_from_excel(uploaded_file)

            if not questions:
                st.warning("No questions found in the first column.")
            else:
                st.success(f"{len(questions)} questions loaded.")

                if "answers" not in st.session_state:
                    st.session_state.answers = [""] * len(questions)

                st.markdown("### 📝 Fill in your answers:")

                for i, q in enumerate(questions):
                    with st.container():
                        col1, col2 = st.columns([1, 2])
                        with col1:
                            st.markdown(f"**Q{i+1}. {q}**")
                        with col2:
                            st.session_state.answers[i] = st.text_area(
                                label=f"Answer {i+1}",
                                value=st.session_state.answers[i],
                                key=f"answer_{i}",
                                label_visibility="collapsed",
                                height=80
                            )

        except Exception as e:
            st.error(f"Error reading file: {e}")

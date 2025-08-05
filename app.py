import streamlit as st
from utils.file_handler import read_questions_from_excel, save_answers_to_excel
from utils.api_client import generate_answer_from_api

st.set_page_config(page_title="Excel Q&A App", layout="wide")
st.title("📄 Excel-Based Question Answer Form")

uploaded_file = st.file_uploader(
    "Upload an Excel file (.xlsx) with questions in the first column",
    type=["xlsx"]
)

if uploaded_file:
    try:
        questions = read_questions_from_excel(uploaded_file)

        if not questions:
            st.warning("No questions found in the first column.")
        else:
            st.success(f"{len(questions)} questions loaded.")

            if "answers" not in st.session_state or len(st.session_state.answers) != len(questions):
                st.session_state.answers = [""] * len(questions)

            st.markdown("### ✍️ Answer the following questions:")

            for idx, question in enumerate(questions):
                with st.container():
                    col1, col2, col3 = st.columns([1.5, 3, 0.5])
                    with col1:
                        st.markdown(f"**Q{idx+1}. {question}**")
                    with col2:
                        st.session_state.answers[idx] = st.text_area(
                            label=f"Answer {idx+1}",
                            value=st.session_state.answers[idx],
                            key=f"answer_{idx}",
                            label_visibility="collapsed",
                            height=80
                        )
                    with col3:
                        if st.button("✨", key=f"gen_btn_{idx}"):
                            with st.spinner(f"Generating answer for Q{idx+1}..."):
                                generated = generate_answer_from_api(question)
                                st.session_state.answers[idx] = generated
                                st.rerun()


            st.markdown("---")
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button("🚀 Generate All Answers", type="primary"):
                    with st.spinner("Generating answers for all questions..."):
                        for idx, question in enumerate(questions):
                            generated = generate_answer_from_api(question)
                            st.session_state.answers[idx] = generated
                        st.success("✅ All answers generated!")

            st.markdown("---")
            st.subheader("📥 Download your answers")
            excel_file = save_answers_to_excel(questions, st.session_state.answers)

            st.download_button(
                label="📄 Download Q&A Excel",
                data=excel_file,
                file_name="answered_questions.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    except Exception as e:
        st.error(f"❌ Error reading file: {e}")

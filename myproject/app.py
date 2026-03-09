import streamlit as st
import requests
API_URL = "https://api-inference.huggingface.co/models/google/flan-t5-large"
API_TOKEN = "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"

headers = {"Authorization": f"Bearer {API_TOKEN}"}

st.title("AI Curriculum Generator")

skill = st.text_input("Skill")
level = st.selectbox("Education Level",["Diploma","BTech","Masters"])
semesters = st.slider("Semesters",1,8)

if st.button("Generate Curriculum"):

    prompt = f"""
    Create a {semesters} semester curriculum for {skill} at {level} level.
    Include course names and topics.
    """

    response = requests.post(API_URL,
        headers=headers,
        json={"inputs": prompt}
    )

    result = response.json()

    st.write(result[0]["generated_text"])
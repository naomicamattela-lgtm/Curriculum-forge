import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv
from utils import generate_timetable

# Load environment variables
load_dotenv()

def main():
    st.set_page_config(page_title="Circulam - AI Timetable Generator", page_icon="📅", layout="wide")

    st.title("📅 Circulam: AI Timetable Generator")
    st.markdown("Generate a structured timetable for your subjects using AI.")

    with st.sidebar:
        st.header("Settings")
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            st.success("Hugging Face API Token loaded from environment.")
        else:
            st.error("HF_TOKEN not found in .env file. Please add it to generate timetables.")
        st.info("The generator uses Qwen2.5-7B via Hugging Face Inference API.")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Curriculum Parameters")
        course_name = st.text_input("Course Name / Subject", placeholder="e.g., Data Science, Introduction to Philosophy")
        
        education_level = st.selectbox("Education Level", ["Primary School", "High School", "Undergraduate", "Postgraduate", "Professional Certification"])
        
        duration = st.text_input("Duration", placeholder="e.g., 8 weeks, 1 semester")
        
        focus = st.text_area("Specific Focus / Topics", placeholder="e.g., Focus on Python and Machine Learning, include a final project.")

        if st.button("Generate Curriculum", type="primary"):
            if not hf_token:
                st.error("Please ensure HF_TOKEN is set in your .env file.")
            elif not course_name.strip():
                st.warning("Please enter a course name.")
            else:
                with st.spinner("Generating your curriculum..."):
                    result = generate_timetable(course_name, education_level, duration, focus, hf_token)
                    
                    if result:
                        st.session_state['curriculum'] = result
                        st.success("Curriculum generated successfully!")
                    else:
                        st.error("Failed to generate curriculum. Check your API token or constraints.")

    with col2:
        st.subheader("Generated Curriculum")
        if 'curriculum' in st.session_state:
            st.markdown(st.session_state['curriculum'])
            
            # Download option
            st.download_button(
                label="Download as Text",
                data=st.session_state['curriculum'],
                file_name="curriculum.md",
                mime="text/markdown",
            )
        else:
            st.info("Fill in the parameters and click 'Generate Curriculum' to see the result here.")

if __name__ == "__main__":
    main()

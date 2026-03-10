import requests
import json
import streamlit as st

def generate_timetable(subjects, days, slots_per_day, constraints, hf_token):
    """
    Calls Hugging Face Inference API to generate a timetable.
    """
    API_URL = "https://router.huggingface.co/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {hf_token}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Generate a detailed curriculum for the following:
    Course/Subject: {subjects}
    Education Level: {days} (e.g., Undergraduate, High School)
    Duration: {slots_per_day} (e.g., semesters or weeks)
    Specific Focus: {constraints}

    Please provide a comprehensive curriculum including:
    1. Course Description.
    2. Learning Objectives.
    3. Topic-wise breakdown for the given duration.
    4. Recommended resources or projects.

    Format the output in clean Markdown.
    """

    payload = {
        "model": "Qwen/Qwen2.5-7B-Instruct",
        "messages": [
            {"role": "system", "content": "You are a professional educational curriculum designer. Output your response in well-formatted Markdown."},
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 1500,
        "temperature": 0.7
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        
        if response.status_code != 200:
            st.error(f"API Error: {response.status_code} - {response.text}")
            return None

        output = response.json()
        
        # Extract response text from Chat Completion format
        try:
            raw_text = output['choices'][0]['message']['content'].strip()
        except (KeyError, IndexError):
            st.error("Unexpected response format from API.")
            st.text(str(output))
            return None

        # Return the raw text as Markdown
        return raw_text

    except Exception as e:
        st.error(f"Request Error: {e}")
        return None

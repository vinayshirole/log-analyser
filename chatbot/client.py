# File: chatbot/client.py
import streamlit as st
import requests

# Load environment variables
from dotenv import load_dotenv
load_dotenv()


API_URL = "http://localhost:8000"

# Log Analyser Agent
def get_log_analysis(logs):
    response = requests.post(f"{API_URL}/analyze_logs/invoke", json={"logs": logs})
    return response.json()['output']['content']

# Code Validator Agent
def get_code_validation(code):
    response = requests.post(f"{API_URL}/validate_code/invoke", json={"code": code})
    return response.json()['output']['content']


if __name__ == "__main__": 
    st.title("AI Debugging Assistant")
    col1, col2 = st.columns(2)

    with col1:
        st.header("Log Analyser")
        logs = st.text_area("Enter logs to analyze:")
        if st.button("Analyze Logs"):
            if logs:
                analysis = get_log_analysis(logs)
                st.subheader("Analysis Result:")
                st.write(analysis)
            else:
                st.warning("Please enter logs to analyze.")

    with col2:
        st.header("Code Validator")
        code = st.text_area("Enter Python code to validate:")
        if st.button("Validate Code"):
            if code:
                validation = get_code_validation(code)
                st.subheader("Validation Result:")
                st.write(validation)
            else:
                st.warning("Please enter Python code to validate.")




# File: Chatbot/main.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.chat_models import ChatOllama

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# ---------------- PROMPT ----------------

system_prompt = """
    You are an AI Debugging Assistant.

    Analyze the following logs and return a JSON response.

    Response format (MANDATORY):
    {{
    "error_summary": "Short description",
    "error_type": "RuntimeError | SyntaxError | ConfigurationError | DependencyError | Unknown",
    "root_cause": "Why the error happened",
    "suggested_fixes": ["List of fixes"]
    }}
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "The error message is as follows:\n{logs}"),
    ]
)

# ---------------- STREAMLIT UI ----------------

st.title("AI Debugging Assistant")
st.write("Paste your application logs and error messages below.")

input_text = st.text_area("Application Logs and Error Messages", height=300)

# ---------------- LLM ----------------

llm = ChatOllama(
    model="mistral",   
    temperature=0.3
)

parser = StrOutputParser()

chain = prompt | llm | parser

# ---------------- RUN ----------------

if st.button("Analyze Logs") and input_text:
    with st.spinner("Analyzing logs..."):
        response = chain.invoke({"logs": input_text})

    st.subheader("Debugging Analysis")
    st.code(response, language="json")

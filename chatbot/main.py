# File: Chatbot/main.py
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Streamlit app
import streamlit as st

# Load environment variables from .env file
import os
from dotenv import load_dotenv

load_dotenv()

# Set environment variables
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_TRACING_V2_PROJECT_NAME"] = os.getenv("LANGCHAIN_TRACING_V2_PROJECT_NAME")
os.environ["LANGSMTIH_API_KEY"] = os.getenv("LANGSMTIH_API_KEY")
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# prompt template
system_prompt =    """
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
# Define prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system_prompt),
        ("user", "The error message is as follows:\n{logs}"),
    ]
)

st.title("AI Debugging Assistant")
st.write("Paste your application logs and error messages below to get debugging assistance.")
input_text = st.text_area("Application Logs and Error Messages", height=300)

# Initialize LLM and output parser
llm_model = ChatOpenAI(
    model="gpt-4o-mini", 
    temperature=0.5, 
    max_tokens=1000
)

output_parser = StrOutputParser()

# Define the chain by combining prompt, LLM, and output parser
chain = prompt | llm_model | output_parser

# Run the chain when input is provided
if input_text:
    with st.spinner("Analyzing logs..."):
        response = chain.invoke({"logs": input_text})
    st.subheader("Debugging Analysis")
    st.code(response, language="json")




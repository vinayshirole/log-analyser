"""
FastAPI server for AI Debugging Assistant using LangChain + LangServe
"""

import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import ChatOllama
from langserve import add_routes

# Load environment variables
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="AI Debugging Assistant",
    description="LangServe-based multi-agent debugging platform",
    version="1.0.0",
)

# Log Analyser Agent
log_analyser_prompt_text = """
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

log_analyser_prompt = ChatPromptTemplate.from_messages([
    ("system", log_analyser_prompt_text),
    ("user", "The error message is as follows:\n{logs}")
])


log_analyser_llm = ChatOpenAI(
    model="gpt-4",
    temperature=0.3
)

log_analyser_chain = log_analyser_prompt | log_analyser_llm

# Code Validator Agent
code_validator_prompt_text = """
You are a Python Code Validator.

Analyze the given Python code and return a JSON response.

Response format (MANDATORY):
{{
  "is_valid": true | false,
  "issues": [
    {{
      "type": "Bug | Security | Performance | Style",
      "description": "Short explanation of the issue",
      "line": "Line number if applicable",
      "severity": "high | medium | low"
    }}
  ],
  "suggested_improvements": ["List of improvements"]
}}
"""

code_validator_prompt = ChatPromptTemplate.from_messages([
    ("system", code_validator_prompt_text),
    ("user", "The code is as follows:\n{code}")
])

code_validator_llm = ChatOllama(
    model="mistral",
    temperature=0.3
)

code_validator_chain = code_validator_prompt | code_validator_llm

# Register routes
add_routes(app, log_analyser_chain, path="/analyze_logs")
add_routes(app, code_validator_chain, path="/validate_code")

# Run the server
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)

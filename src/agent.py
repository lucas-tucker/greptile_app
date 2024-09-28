import os
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from langgraph.prebuilt import create_react_agent
from tools import load_repo_tool, query_repo_tool, generate_diagram_tool

# Initialize the OpenAI chat model
llm = ChatOpenAI(model="gpt-3.5-turbo")

# Define your tools
tools = [load_repo_tool.load_repo_tool, 
        query_repo_tool.query_repo_tool, 
        generate_diagram_tool.generate_diagram_tool]

# Create the agent
agent_executor = create_react_agent(llm, tools)
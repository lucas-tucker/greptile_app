from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import os
import requests

class LoadRepoInput(BaseModel):
    repo_name: str = Field(..., description="GitHub repository name.")
    repo_owner: str = Field(..., description="GitHub repository owner or organization.")
    github_token: str = Field(..., description="The 'token' field from user input")
    
@tool
def load_repo_tool(input: LoadRepoInput) -> str:
    """
    Load the user's repository of choice using the Greptile API. Use the response in the
    'token' field of the user's input for the x-github-token. Only ever call this tool once,
    and do so only if the repository has not been loaded.
    
    Args:
        input (LoadRepoInput): The input object containing the repository information. 
    
    Returns:
        str: a report on whether the request was made successfully. 
    """
    GREPTILE_API_KEY = os.getenv("GREPTILE_API_KEY")

    # Define the headers and data for the request
    headers = {
        "Authorization": f"Bearer {GREPTILE_API_KEY}",
        "X-Github-Token": input.github_token,
        "Content-Type": "application/json"
    }

    data = {
        "remote": "github",
        "repository": input.repo_owner + "/" + input.repo_name,
        "branch": "main"
    }

    # Make the POST request
    try:
        response = requests.post("https://api.greptile.com/v2/repositories", headers=headers, json=data)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Encountered error {e} loading the repository into Greptile. input was {input}"
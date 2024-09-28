from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import os
import requests

class QueryRepoInput(BaseModel):
    repo_name: str = Field(..., description="GitHub repository name.")
    repo_owner: str = Field(..., description="GitHub repository owner or organization.")
    query: str = Field(..., description="Query about the GitHub repository")
    github_token: str = Field(..., description="X-GitHub-Token from the user's query")

@tool
def query_repo_tool(input: QueryRepoInput) -> str:
    """
    Query the user's loaded repository using the Greptile API. Ask the user
    for repository information and load the repo prior to invoking this tool. Only
    ever invoke this tool once, and only if the user wants to know more about the 
    repo. Ask the user if they would like to generate a diagram after returning
    the query results.
    
    Args:
        input (QueryRepoInput): The input object containing the repository link. 
    
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
      "messages": [
          {
              "id": "some-id-1",
              "content": input.query,
              "role": "user"
          }
      ],
      "repositories": [
          {
              "remote": "github",
              "repository": input.repo_owner + "/" + input.repo_name,
              "branch": "main"
          }
      ],
      "sessionId": "test-session-id" # optional
    }

    # Make the POST request
    try:
        response = requests.post("https://api.greptile.com/v2/query", headers=headers, json=data)
        response.raise_for_status() 
        return response.json()
    except requests.exceptions.RequestException as e:
        return f"Encountered error {e} querying the repository via Greptile"
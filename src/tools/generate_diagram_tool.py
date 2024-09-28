from typing import List, Optional
from pydantic import BaseModel, Field
from langchain_core.tools import tool
import os
import requests

class GenerateDiagramInput(BaseModel):
    diagram_desc: str = Field(..., description="Description of repo diagram divined from context")  

def upload_image_to_imgur(image_content):
    """Uploads an image to Imgur and returns the image link."""
    client_id = 'YOUR_IMGUR_CLIENT_ID'
    headers = {
        'Authorization': f'Client-ID {client_id}',
    }
    files = {
        'image': image_content,
    }
    response = requests.post('https://api.imgur.com/3/image', headers=headers, files=files)
    response.raise_for_status()  # Raises an exception for HTTP error responses
    return response.json()['data']['link']

@tool
def generate_diagram_tool(input: GenerateDiagramInput) -> str:
    """
    Invoke this tool only if the user explicitly requests a diagram of their repository.
    Pass the relevant respose about the repo as a diagram description to this tool. 
    Never invoke this tool multiple times.
    
    Args:
        input (QueryRepoInput): The input object containing the repository link. 
    
    Returns:
        str: a report on whether the request was made successfully. 
    """
    ERASER_API_KEY = os.getenv("ERASER_API_KEY")

    # Define the headers and data for the request
    headers = {
        "Authorization": f"Bearer {ERASER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "text": input.diagram_desc,
        "diagramType": "sequence-diagram",
        "background": True,
        "theme": "light",
        "scale": "1",
        "returnFile": True
    }

    # In your try block, replace the file saving logic with the following:
    try:
        print(f"Making POST request to Eraser API")
        response = requests.post("https://app.eraser.io/api/render/prompt", headers=headers, json=data)
        response.raise_for_status()

        # Upload the diagram to Imgur and get the image link
        image_link = upload_image_to_imgur(response.content)
        print(f"Diagram successfully generated and available at {image_link}")
        return f"Diagram successfully generated and available at {image_link}"
    except requests.exceptions.HTTPError as e:
        print(f"Encountered error {e} generating a diagram via Eraser with input {input}")
    except Exception as e:
        print(f"Encountered a general error {e} with input {input}")
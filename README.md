### Demo
https://www.youtube.com/watch?v=MVITcmzU2Gs

### Summary 
This is an endpoint for a ChatGPT agent equipped with the following tools:
- load_repo_tool.py: loads repository via Greptile API call
- query_repo_tool.py: queries the repository via Greptile API call
- generate_diagram_tool.py: generates a diagram using Eraser.io's DiagramGPT based on conversation context
The agent uses these tools at its discretion to index, query, and diagram repositories both you and your
GitHub App can access.

### How to run
1. Clone this repo
2. Create an ngrok link (or other link exposing your localhost) for port 5000
3. Set your Copilot App's endpoint URL to this ngrok link with an additional `/stream` at the end
4. Ensure your Copilot App has repository permissions
5. Navigate to the `greptile_app` directory
6. Create a `.env` file in the directory with `OPENAI_API_KEY`, `GREPTILE_API_KEY` and `ERASER_API_KEY` all set
7. Run `make start-server` from the `greptile_app` directory
8. Chat with the agent using its @ slug

### Key Points
- The agent parses POST requests sent from the GitHub App in `src/agent_server.py` and formats agent responses when sending return requests
- Links to diagrams and the status of repository loading are variably clickable (due to GitHub App formatting)

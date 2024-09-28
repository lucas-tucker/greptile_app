# Default .env file
ENV_FILE := .env

# Load environment variables from the .env file
include $(ENV_FILE)
export $(shell sed 's/=.*//' $(ENV_FILE))

# Target to run the Flask app
start-server:
	@echo "Starting the Flask server with environment variables from $(ENV_FILE)..."
	python3 src/agent_server.py
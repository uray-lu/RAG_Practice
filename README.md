# GTW-RAG-ChatBot


GTW-RAG-ChatBot is a Flask-based application that hosts a chatbot endpoint to respond to queries using a specified reference in a vector database.

# Outline

1. [Endpoint](#endpoint)
2. [Example Usages](#example-usages)
3. [Request Body](#request-body)
4. [Makefile](#makefile)

## Endpoint

The API endpoint for the GTW-RAG-Document-System is accessible at:

`{base_url}/chat/v1`

### Example Usages:
- **Base URL:** `http://dev.example.com`
- **Endpoint:** `http://dev.example.com/chat/v1`


Replace `{base_url}` with the actual base URL of your respective environment.

## Request Body

The API expects a JSON payload in the request body with the following structure:

```json
{
   "query": "Your question here",
   "vector_db": "Name of the vector database to reference"
}
```

## Makefile

### Deploy Info
- `HOME_DIR`: C:/Users/{ueser}
- `DOCKER_IMAGE_NAME`: GTW-RAG-Doument-System
- `DOCKER_IMAGE_VERSION`: 0.0.0
- `DOCKER_CONTAINER_NAME`: GTW-RAG-Doument-System-test
- `AWS_CONFIG_PATH`: $(HOME_DIR)/.aws
- `AWS_S3_profile`: default
- `AWS_Bedrock_profile`: bedrock

### Available Targets:
- `build`: Build the Docker image for the Flask app.
- `run`: Run the Flask app in a Docker container with .aws volume mount.
- `test`: Run unit tests from unit_test.py.
- `clean`: Stop and remove the Docker container, and remove the Docker image.
- `help`: Show available targets and their descriptions.

### Usage:
- `make build`: Build the Docker image.
- `make run`: Run the Flask app in a Docker container with AWS configuration.
- `make test`: Run unit tests.
- `make clean`: Stop the container and remove both the container and image.


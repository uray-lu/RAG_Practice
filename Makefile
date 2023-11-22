#=================================================================#
# Please do not make any change except you know what you're doing.# 
# The only thing you need to Chang is the Deploy Info Below.      #
#=================================================================#
#TODO:AWS deploy
# Deploy info 
HOME_DIR = C:/Users/raylu
DOCKER_IMAGE_NAME = gama-chat
DOCKER_IMAGE_VERSION = 0.0.0
DOCKER_CONTAINER_NAME = gama-chat-test
AWS_CONFIG_PATH = $(HOME_DIR)/.aws

.PHONY: help
help:
	@echo "Available targets:"
	@echo "  build          - Build the Docker image for the Flask app"
	@echo "  run            - Run the Flask app in a Docker container with .aws volume mount"
	@echo "  test           - Run unit tests from unit_test.py"
	@echo "  clean          - Stop and remove the Docker container, and remove the Docker image"
	@echo "  help           - Show this help message"

# Build the Docker image for the Flask app
build:
	docker build -t $(DOCKER_IMAGE_NAME):$(DOCKER_IMAGE_VERSION) .

# Run the Flask app in a Docker container with .aws volume mount
run:
	docker run -d -p 5000:5000 --name $(DOCKER_CONTAINER_NAME) -v $(AWS_CONFIG_PATH):/root/.aws $(DOCKER_IMAGE_NAME)

# Run unit tests from unit_test.py
test:
	python -m unittest unit_test

# Stop and remove the Docker container, and remove the Docker image
clean:
	-docker stop $(DOCKER_CONTAINER_NAME)
	-docker rm $(DOCKER_CONTAINER_NAME)
	-docker rmi $(DOCKER_IMAGE_NAME)

# The default target when you just run 'make' is 'help'
.DEFAULT_GOAL := help
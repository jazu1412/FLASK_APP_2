#!/bin/bash

# Set variables
IMAGE_NAME="software-platforms"
IMAGE_TAG="V1"
REGISTRY="jazu1412"

# Build the Docker image
echo "Building Docker image..."
docker build -t $REGISTRY/$IMAGE_NAME:$IMAGE_TAG .

# Run tests in a container
echo "Running tests..."
docker run --rm $REGISTRY/$IMAGE_NAME:$IMAGE_TAG pytest

# If tests pass, push the image to the registry
if [ $? -eq 0 ]; then
    echo "Tests passed. Pushing image to registry..."
    docker push $REGISTRY/$IMAGE_NAME:$IMAGE_TAG
    echo "Image pushed successfully."

    # Run the container
    echo "Running the container..."
    docker run -d -p 1455:1455 --name flask-blog $REGISTRY/$IMAGE_NAME:$IMAGE_TAG

    echo "Container is now running. Access the application at http://localhost:1399"
else
    echo "Tests failed. Image will not be pushed."
    exit 1
fi
# Flask Blog Application

This is a simple Flask blog application containerized using Docker.

## Building the Docker Image

To build the Docker image, run the following command from the `flask_blog` directory:

```
docker build -t flask-blog-app .
```

## Running Tests

To run the tests in a Docker container, use the following command:

```
docker run --rm flask-blog-app pytest
```

## Pushing the Image to a Registry

To push the image to a container registry (e.g., Docker Hub), follow these steps:

1. Tag the image with your registry username:

```
docker tag flask-blog-app YOUR_USERNAME/flask-blog-app:latest
```

Replace `YOUR_USERNAME` with your Docker Hub username or the appropriate registry path.

2. Log in to your container registry:

```
docker login
```

3. Push the image to the registry:

```
docker push YOUR_USERNAME/flask-blog-app:latest
```

Again, replace `YOUR_USERNAME` with your actual username or registry path.

Note: Make sure you have the necessary permissions to push to the chosen registry.

## Running the Application

To run the application locally, use the following command:

```
docker run -p 1400:1399 flask-blog-app
```

The application will be available at http://localhost:1400.
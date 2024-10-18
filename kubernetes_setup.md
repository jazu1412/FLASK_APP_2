# Kubernetes Setup for Flask Blog Application

This document outlines the process of setting up and deploying our Flask blog application using Kubernetes with Kind (Kubernetes in Docker).

## 1. Setting up Kind

Kind (Kubernetes in Docker) is a tool for running local Kubernetes clusters using Docker container "nodes". It's designed for testing Kubernetes and local development.

To set up Kind:

1. Install Kind:
   ```
   brew install kind
   ```

2. Create a Kind cluster:
   ```
   kind create cluster --name flask-blog-cluster
   ```

## 2. Building and Loading the Docker Image

1. Build the Docker image for the Flask application:
   ```
   docker build -t flask_blog:latest .
   ```

2. Load the image into the Kind cluster:
   ```
   kind load docker-image flask_blog:latest --name flask-blog-cluster
   ```

## 3. Deploying the Application

1. Create a deployment YAML file (deployment.yaml):
   ```yaml
   apiVersion: apps/v1
   kind: Deployment
   metadata:
     name: flask-blog
   spec:
     replicas: 1
     selector:
       matchLabels:
         app: flask-blog
     template:
       metadata:
         labels:
           app: flask-blog
       spec:
         containers:
         - name: flask-blog
           image: flask_blog:latest
           imagePullPolicy: Never
           ports:
           - containerPort: 5009
   ---
   apiVersion: v1
   kind: Service
   metadata:
     name: flask-blog-service
   spec:
     selector:
       app: flask-blog
     ports:
       - protocol: TCP
         port: 80
         targetPort: 5009
     type: ClusterIP
   ```

2. Apply the deployment:
   ```
   kubectl apply -f deployment.yaml
   ```

## 4. Verifying the Deployment

1. Check the pods:
   ```
   kubectl get pods
   ```

2. Check the services:
   ```
   kubectl get services
   ```

3. Check the deployments:
   ```
   kubectl get deployments
   ```

4. Check the replicasets:
   ```
   kubectl get replicasets
   ```

## 5. Accessing the Application

Since we're using ClusterIP as the Service type, we need to use port-forwarding to access our application:

```
kubectl port-forward service/flask-blog-service 8080:80
```

Now you can access the application at `http://localhost:8080`.

## 6. Cleaning Up

To delete the Kind cluster when you're done:

```
kind delete cluster --name flask-blog-cluster
```

This process allows us to develop, test, and run our Flask blog application in a local Kubernetes environment using Kind, providing a setup that closely mimics a production Kubernetes deployment.
# Flask Blog Application Architecture

## Before: Monolithic Architecture

The original Flask Blog application was built as a monolithic architecture where all components were tightly coupled within a single application.

```
[User] <--> [Flask Web App]
              |
              v
         [Database]
```

In this architecture, the Flask application handled all aspects of the blog, including post creation, viewing, editing, and deletion. The application didn't have explicit user authentication.

## After: Microservices Architecture

We've broken down the application into the following microservices:

1. Auth Service: Handles user authentication and authorization
2. Post Service: Manages blog post creation, editing, viewing, and deletion
3. Frontend Service: Serves the user interface

```
                   +-------------+
                   |   API       |
[User] <--> [UI] <-+   Gateway   |
                   |             |
                   +-------------+
                         |
                 +-------+-------+
                 |               |
         +-------v-----+ +-------v-----+
         | Auth Service| | Post Service|
         |             | |             |
         +-------+-----+ +------+------+
                 |              |
         +-------v--------------v------+
         |         Database            |
         +------------------------------+
```

In this new architecture:
- The Frontend Service serves the user interface.
- The API Gateway routes requests to appropriate microservices.
- The Auth Service handles user authentication and authorization.
- The Post Service manages all post-related operations.
- Each service has its own database (not shown in diagram for simplicity).
- Services communicate with each other through the API Gateway when necessary.

## API Endpoints

1. Auth Service:
   - POST /auth/register: Register a new user
   - POST /auth/login: User login
   - POST /auth/logout: User logout

2. Post Service:
   - GET /posts: Get all posts (index page)
   - GET /posts/{id}: Get a specific post
   - POST /posts: Create a new post
   - PUT /posts/{id}: Edit a post
   - DELETE /posts/{id}: Delete a post

3. Frontend Service:
   - Serves the React/Vue.js application that interacts with the backend services

This architecture allows for better scalability, easier maintenance, and independent deployment of services. It also introduces proper authentication to the application, enhancing its security.
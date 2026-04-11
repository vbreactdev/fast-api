# Laboratory Manual: Developing and Deploying a Microservice Architecture with FastAPI and Docker

## 1. Introduction and Objectives

The goal of this laboratory work is to learn the basics of microservice architecture (SOA/Microservices) by deploying and testing a simple project with two interacting services written in Python (FastAPI).
Students will learn how to:

- Understand basic microservice concepts.
- Review a Dockerized project structure.
- Build and run services using Docker Compose.
- Test service interaction via REST API.

## 2. Prerequisites

Before starting this laboratory work, ensure you have the following installed on your local machine:

- **Docker** and **Docker Compose** (Docker Desktop is recommended for Windows/Mac).
- **Git** (optional, to clone the repository if not downloaded as a ZIP).
- A terminal with `curl` installed (e.g., Git Bash, WSL, Linux/Mac terminal) for CLI testing.

## 3. Architecture Overview

This project consists of two independent microservices:

1. **Auth Service (`service_auth`)**: Responsible for user authentication. It issues standard JWT (JSON Web Token) access tokens and provides an introspection endpoint for internal validation.
2. **Data Service (`service_data`)**: A protected service that manages data (CRUD operations for "items"). It does not issue tokens, but rather validates the incoming Bearer tokens by communicating with the Auth Service.

_Both services have a `/health/ready` endpoint used by Docker to check if the service is up and running._

![UML architecture diagram](screenshots/uml.png)

## 4. Project Structure Review

Extract the project archive or clone the repository to your local machine. Open the folder in a code editor (like VS Code) or just navigate through the directories to familiarize yourself.

```text
.
|-- .env.example            # Environment variables template
|-- architecture.puml       # UML diagram source
|-- docker-compose.yml      # Orchestration file for Docker
|-- service_auth/           # First microservice directory
|   |-- Dockerfile          # Instructions to build the auth container
|   `-- app/                # Python Web App codebase
`-- service_data/           # Second microservice directory
    |-- Dockerfile          # Instructions to build the data container
    `-- app/                # Python Web App codebase
```

## 5. Step-by-step Execution

### Step 1: Starting the Services

1. Open your Terminal (If you are on Windows, standard Command Prompt or PowerShell is fine here).
2. Navigate to the root directory of the project (where `docker-compose.yml` is located).
3. Run the following command to build the images and start the containers in the background:
   ```bash
   docker compose up --build -d
   ```
4. Check if the containers are successfully running by executing:
   ```bash
   docker compose ps
   ```
   _You should see both `service_auth` and `service_data` with a status of "Up" (or "healthy")._

![Running containers](screenshots/01-compose-ps.png)

### Step 2: Checking Service Health

Microservices typically expose a health endpoint so orchestration tools (like Docker) know they are fully running. You can verify this manually:

1. Try performing a `curl` request in your terminal:
   ```bash
   curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8001/health/ready
   curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8002/health/ready
   ```
2. You should receive `200` back from both services, which means they are ready to accept connections.

![Health checks](screenshots/02-health-checks.png)

### Step 3: Testing Authentication (Obtaining a Token)

To interact with the Data Service, we first need to identify ourselves. We will request a token from the Auth service.

> 💡 **Cross-OS Compatibility Note:** If you are using Windows, please run the following `curl` commands in **Git Bash** or **WSL**. Standard PowerShell or Command Prompt processes JSON quotes differently and may result in a `JSON decode error`.

1. Run the following command in your terminal:
   ```bash
   curl -X POST "http://localhost:8001/api/v1/auth/token" \
     -H "Content-Type: application/json" \
     -d "{\"username\":\"admin\",\"password\":\"changeit\"}"
   ```
2. **Copy the output `access_token` string `<jwt>`** (without the quotes). You will need this for the next step.

![Token issuance](screenshots/03-token.png)

### Step 4: Accessing Protected Data (CRUD Operations)

Now we will use the acquired token (referred to as `<jwt>`) to manage items in our Data Service by authenticating our requests with `Authorization: Bearer <jwt>`.

1. **Create an item:**

   ```bash
   curl -X POST "http://localhost:8002/api/v1/items" \
     -H "Authorization: Bearer <jwt>" \
     -H "Content-Type: application/json" \
     -d "{\"name\":\"sample-item\",\"description\":\"created through the data service\"}"
   ```

2. **Retrieve the items list:**

   ```bash
   curl "http://localhost:8002/api/v1/items" \
     -H "Authorization: Bearer <jwt>"
   ```

3. **Delete an item (replace `<item_id>` with the ID you received):**
   ```bash
   curl -X DELETE "http://localhost:8002/api/v1/items/<item_id>" \
     -H "Authorization: Bearer <jwt>"
   ```

![CRUD flow](screenshots/04-crud-flow.png)

### Step 5: Cleaning Up

After you have finished testing, you should always stop and remove your containers to free up system resources.

1. Return to your Terminal.
2. Execute the following command:
   ```bash
   docker compose down
   ```

_Make sure all containers have been successfully stopped and removed!_

## 6. Conclusion

In this laboratory work, we successfully deployed a microservice architecture locally using Docker. We learned how services are isolated but can communicate with each other (Data service validating the Auth service's token) and verified the functionality using standard terminal tools like `curl`.

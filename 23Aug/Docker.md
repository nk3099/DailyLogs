# Docker Guide — Airflow + FastAPI

## 1. Docker Container

A **container** is an isolated environment in which an application runs.

```text
Docker
│
├── Airflow containers
│   ├── airflow-apiserver
│   ├── airflow-scheduler
│   ├── airflow-triggerer
│   ├── airflow-postgres
│   ├── airflow-redis
│   └── ...
│
└── FastAPI
    └── fastapi-app
```

A container is **not the same thing as an application/project**.

One application can require multiple containers.

---

## 2. Docker Compose

Docker Compose lets you define and manage multiple containers/services using a YAML file.

```yaml
services:
  api:
    build: .
    container_name: fastapi-app
    ports:
      - "5001:5000"
```

Start the services:

```bash
docker compose up -d
```

### What does `-d` mean?

`-d` means **detached mode**.

It starts the containers in the background.

Without `-d`:

```bash
docker compose up
```

the terminal remains attached to the container logs.

---

## 3. Docker Compose Projects

Example:

```text
airflow/
└── docker-compose.yml

api_code/
└── docker-compose.yml
```

These can be two separate Compose projects:

```text
Airflow Compose Project
│
├── PostgreSQL
├── Redis
├── API Server
├── Scheduler
└── Triggerer

FastAPI Compose Project
│
└── fastapi-app
```

Each Compose project can have its own Docker network.

---

## 4. Docker Network

A Docker network allows containers to communicate with each other.

List networks:

```bash
docker network ls
```

Inspect a network:

```bash
docker network inspect airflow_default
```

The inspect command shows which containers are connected to the network.

---

## 5. Why `localhost` Failed

Initially:

```python
url = "http://localhost:5001/getAll"
```

The Python code was running **inside an Airflow container**.

Inside a container:

```text
localhost
```

means:

> This same container.

So:

```text
Airflow container
      │
      │ localhost:5001
      ▼
Airflow container itself
      │
      └── Nothing listening on port 5001
```

Result:

```text
Connection refused
```

---

## 6. Container-to-Container Communication

Containers need to be connected to the same Docker network for this setup.

```text
              airflow_default
        ┌─────────────────────────┐
        │                         │
        │  Airflow            FastAPI
        │  container          container
        │      │                  │
        │      └────── HTTP ──────┤
        │                         │
        └─────────────────────────┘
```

Airflow can then call:

```text
http://fastapi-app:5000
```

---

## 7. `container_name`

FastAPI Compose:

```yaml
container_name: fastapi-app
```

Therefore the container is named:

```text
fastapi-app
```

Another container on the same network can use:

```text
http://fastapi-app:5000
```

---

## 8. Port Mapping

FastAPI Compose:

```yaml
ports:
  - "5001:5000"
```

Format:

```text
HOST PORT : CONTAINER PORT
     5001 : 5000
```

Therefore:

```text
Your Mac
localhost:5001
      │
      │ Docker port mapping
      ▼
fastapi-app
container:5000
      │
      ▼
FastAPI/Uvicorn
```

### From your Mac

```text
http://localhost:5001
```

### From another Docker container

```text
http://fastapi-app:5000
```

Not:

```text
http://fastapi-app:5001
```

because `5001` is the host port.

---

## 9. Why `5001:5000`?

Think:

```text
5001 → 5000
```

Docker forwards:

```text
Mac:5001
     ↓
Container:5000
```

Uvicorn runs inside the container:

```bash
uvicorn main:app --host 0.0.0.0 --port 5000
```

Therefore:

```text
Mac
localhost:5001
     ↓
Docker
     ↓
Container
0.0.0.0:5000
     ↓
FastAPI
```

---

## 10. `0.0.0.0` vs `localhost`

Use:

```bash
--host 0.0.0.0
```

inside the container.

Avoid:

```bash
--host 127.0.0.1
```

because:

```text
127.0.0.1
    ↓
Only this container
```

whereas:

```text
0.0.0.0
    ↓
All network interfaces of the container
```

---

## 11. `external: true`

FastAPI Compose:

```yaml
networks:
  airflow_default:
    external: true
```

This means:

> Use an already existing Docker network called `airflow_default`.

It does not create a new network.

Airflow already created:

```text
airflow_default
```

FastAPI joins that existing network.

---

## 12. Final FastAPI Compose Configuration

```yaml
services:
  api:
    build: .
    container_name: fastapi-app
    ports:
      - "5001:5000"
    networks:
      - airflow_default
    restart: unless-stopped

networks:
  airflow_default:
    external: true
```

Architecture:

```text
                 airflow_default
                       │
          ┌────────────┴────────────┐
          │                         │
       Airflow                  fastapi-app
          │                         │
          └────── HTTP request ─────┘
                    │
                    ▼
             FastAPI :5000
```

---

## 13. Correct URL in the Airflow DAG

Wrong:

```python
url = "http://localhost:5001/getAll"
```

Correct:

```python
url = "http://fastapi-app:5000/getAll"
```

Request flow:

```text
Airflow
   │
   │ http://fastapi-app:5000
   ▼
fastapi-app
   │
   ▼
FastAPI /getAll
```

---

## 14. Python `requests`

Import:

```python
import requests
```

POST request:

```python
response = requests.post(
    url,
    headers=headers,
    json=payload
)
```

Python is case-sensitive.

Correct:

```python
requests.post()
```

Incorrect:

```python
requests.POST()
```

Common methods:

```python
requests.get()
requests.post()
requests.put()
requests.patch()
requests.delete()
```

---

## 15. `json=` vs `data=`

Instead of:

```python
import json

payload = json.dumps({
    "start_date": "2026-08-23",
    "end_date": "2026-08-24"
})

response = requests.post(
    url,
    headers=headers,
    data=payload
)
```

Prefer:

```python
payload = {
    "start_date": "2026-08-23",
    "end_date": "2026-08-24"
}

response = requests.post(
    url,
    headers=headers,
    json=payload
)
```

`requests` handles JSON serialization automatically.

---

## 16. Airflow Operator

An **Operator** defines the type of work an Airflow task performs.

### PythonOperator

```python
PythonOperator
```

Executes Python code.

### BashOperator

```python
BashOperator
```

Executes Bash commands.

Conceptually:

```text
Operator
   ↓
Defines type of work
   ↓
Task
```

Example:

```python
pull_data = PythonOperator(
    task_id="pull_data",
    python_callable=fetch_python_api
)
```

Here:

```text
PythonOperator    → Operator
pull_data         → Task
fetch_python_api  → Python function
```

---

## 17. `op_args`

`op_args` means **operator arguments**.

It passes positional arguments to the Python function.

Function:

```python
def fetch_python_api(url, start_date, end_date):
    ...
```

Operator:

```python
PythonOperator(
    task_id="pull_data",
    python_callable=fetch_python_api,
    op_args=[
        "http://fastapi-app:5000/getAll",
        "2026-08-23",
        "2026-08-24"
    ]
)
```

Airflow effectively executes:

```python
fetch_python_api(
    "http://fastapi-app:5000/getAll",
    "2026-08-23",
    "2026-08-24"
)
```

Remember:

```text
op_args   → positional arguments
op_kwargs → keyword/named arguments
```

---

## 18. Airflow Variables

Example error:

```text
VARIABLE_NOT_FOUND:
Variable API_AUTH_HEADER not found
```

This means the DAG tried to retrieve:

```python
Variable.get("API_AUTH_HEADER")
```

but the variable does not exist in Airflow.

Conceptually:

```text
DAG
 │
 │ Variable.get()
 ▼
Airflow Variable Store
 │
 └── API_AUTH_HEADER
```

Airflow Variables are useful for storing configuration values.

---

## 19. Docker Commands

### Start containers

```bash
docker compose up -d
```

### Stop containers

```bash
docker compose down
```

### List running containers

```bash
docker ps
```

### List all containers

```bash
docker ps -a
```

### List Docker networks

```bash
docker network ls
```

### Inspect a network

```bash
docker network inspect airflow_default
```

### Connect a container to a network

```bash
docker network connect airflow_default fastapi-app
```

### View logs

```bash
docker compose logs
```

### Follow logs

```bash
docker compose logs -f
```

### View FastAPI logs

```bash
docker logs fastapi-app
```

---

## 20. Troubleshooting Checklist

If Airflow cannot call FastAPI:

### Step 1 — Check containers

```bash
docker ps
```

### Step 2 — Check networks

```bash
docker network ls
```

### Step 3 — Inspect Airflow network

```bash
docker network inspect airflow_default
```

Look for:

```text
fastapi-app
```

### Step 4 — Check FastAPI logs

```bash
docker logs fastapi-app
```

### Step 5 — Check port mapping

```yaml
ports:
  - "5001:5000"
```

Means:

```text
Mac              → localhost:5001
Docker network   → fastapi-app:5000
```

### Step 6 — Check Uvicorn

It should listen on:

```text
0.0.0.0:5000
```

### Step 7 — Check Airflow URL

Use:

```python
url = "http://fastapi-app:5000/getAll"
```

Not:

```python
url = "http://localhost:5001/getAll"
```

---

# 21. Five Important Docker Concepts

## 1. Container

Runs an application/process.

```text
Container → Running instance of an image
```

## 2. Image

A blueprint/template used to create containers.

```text
Image
  │
  └── creates → Container
```

## 3. Compose

Defines and manages multiple services/containers.

```text
docker-compose.yml
       │
       ├── service 1
       ├── service 2
       └── service 3
```

## 4. Network

Allows containers to communicate.

```text
Container A ─── Docker Network ─── Container B
```

## 5. Port Mapping

Connects a host port to a container port.

```text
HOST:5001 → CONTAINER:5000
```

---

# 22. Golden Rule: `localhost` vs Container Name

This is the most important lesson.

### From your Mac

```text
localhost:5001
```

because:

```text
5001 → 5000
```

### From an Airflow container

```text
fastapi-app:5000
```

because Airflow and FastAPI communicate through the Docker network.

```text
             YOUR MAC
                │
                │ localhost:5001
                ▼
          ┌─────────────┐
          │ fastapi-app │
          │    :5000    │
          └─────────────┘
                ▲
                │
                │ fastapi-app:5000
                │
          ┌─────────────┐
          │   Airflow   │
          │  container  │
          └─────────────┘
```

### Remember

```text
localhost
   ↓
"This machine/container"

Container-to-container
   ↓
"Use the container/service name"

Example:
http://fastapi-app:5000
```

---

# 23. Final Mental Model

```text
                 Docker Host / Mac
                         │
             ┌───────────┴───────────┐
             │                       │
        Host Port
       localhost:5001
             │
             ▼
      ┌──────────────┐
      │  fastapi-app │
      │    :5000     │
      └──────┬───────┘
             │
       airflow_default
             │
             ▼
      ┌──────────────┐
      │   Airflow    │
      │  containers  │
      └──────────────┘
```

## Key distinction

```text
Outside Docker:
    localhost:5001

Inside Docker network:
    fastapi-app:5000
```

> **Rule of thumb:** `localhost` refers to the current machine/container. For container-to-container communication, use the Docker service/container name and the **container's internal port**.

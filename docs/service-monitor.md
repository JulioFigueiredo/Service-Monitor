# Service Monitor

A lightweight uptime and performance monitoring platform designed to monitor services, detect incidents, collect performance metrics, and demonstrate production-oriented backend and infrastructure practices.

The project is primarily a learning and portfolio project focused on backend engineering, asynchronous processing, distributed systems, cloud infrastructure, networking, DevOps, and observability.

> **Language Convention**
>
> All code and technical artifacts in this project must be written in **English**.
>
> This includes:
>
> * Source code
> * Variable and function names
> * Classes and modules
> * Database tables and columns
> * API endpoints and parameters
> * API responses and error messages
> * Logs
> * Commit messages
> * Configuration names
> * Tests
> * Technical documentation
> * UI text

---

# Objectives

The main objectives of the project are:

* Monitor URLs and services
* Perform periodic health checks
* Measure response latency
* Detect service failures
* Detect service recovery
* Track incidents
* Store historical check results
* Display monitoring data through a web dashboard
* Process checks asynchronously
* Implement authentication and authorization
* Containerize the application
* Deploy the system to AWS
* Configure Nginx as a reverse proxy
* Implement CI/CD
* Implement application observability

---

# Architecture

```text
                         Internet
                            │
                          Nginx
                     ┌──────┴──────┐
                     │             │
                  Next.js       FastAPI
                     │             │
              Authentication       │
                     │             │
                     └──────┬──────┘
                            │
                       PostgreSQL
                            │
                          Redis
                            ↑
                       Scheduler
                            │
                            ↓
                         Worker
                      ┌─────┴─────┐
                      │           │
                 HTTP Check   TCP Check
                      │           │
                      └─────┬─────┘
                            │
                     Monitored Services
```

The API must not execute monitoring checks synchronously.

The scheduler is responsible for determining **when** a check should happen.

Redis is responsible for transporting and queuing **what** needs to be executed.

The worker is responsible for executing **how** the check is performed.

PostgreSQL is responsible for persistent application data and monitoring results.

---

# Main Components

| Component      | Responsibility                                   |
| -------------- | ------------------------------------------------ |
| Next.js        | Web application, authentication UI and dashboard |
| FastAPI        | REST API and business logic                      |
| PostgreSQL     | Persistent data storage                          |
| Redis          | Task queue and temporary data                    |
| Scheduler      | Creates monitoring jobs                          |
| Worker         | Executes monitoring checks                       |
| Nginx          | Reverse proxy and HTTPS termination              |
| Docker         | Application containerization                     |
| AWS EC2        | Application hosting                              |
| Route 53       | DNS                                              |
| CloudWatch     | Logs, metrics and infrastructure monitoring      |
| GitHub Actions | CI/CD                                            |

---

# Monitoring Flow

A typical monitoring cycle works as follows:

```text
Scheduler
    │
    │ enqueue check
    ↓
Redis
    │
    │ consume job
    ↓
Worker
    │
    │ HTTP/TCP request
    ↓
Monitored Service
    │
    │ response
    ↓
Worker
    │
    │ save result
    ↓
PostgreSQL
```

The frontend does not communicate directly with PostgreSQL.

```text
Next.js
   │
   │ HTTP
   ↓
FastAPI
   │
   ↓
PostgreSQL
```

---

# Authentication

The application will support user authentication.

Each user owns their own monitors and monitoring data.

The authentication flow will use JWT-based authentication.

```text
User
  │
  ↓
Next.js Login
  │
  │ POST /api/v1/auth/login
  ↓
FastAPI
  │
  ↓
JWT Access Token
  │
  ↓
Authenticated Requests
  │
  ↓
FastAPI
  │
  ├── Authentication
  ├── Authorization
  └── User data isolation
```

Initial authentication features:

* User registration
* User login
* Password hashing
* JWT access tokens
* Refresh tokens
* Token expiration
* Authenticated API requests
* User ownership of monitors
* Authorization checks

The project will initially use JWT authentication rather than OAuth providers such as Google or GitHub.

---

# Domain Model

## User

```text
id
email
password_hash
is_active
created_at
updated_at
```

## Monitor

```text
id
user_id
name
url
type
interval
timeout
expected_status
enabled
created_at
updated_at
```

Possible monitor types:

```text
HTTP
TCP
```

## CheckResult

```text
id
monitor_id
status
status_code
latency_ms
error
checked_at
```

Possible statuses:

```text
UP
DOWN
```

## Incident

```text
id
monitor_id
started_at
resolved_at
duration
reason
```

---

# API

The API will use versioning:

```text
/api/v1
```

## Authentication

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
```

## Monitors

```text
POST   /api/v1/monitors
GET    /api/v1/monitors
GET    /api/v1/monitors/{monitor_id}
PATCH  /api/v1/monitors/{monitor_id}
DELETE /api/v1/monitors/{monitor_id}
```

All monitor endpoints require authentication.

Users must only be able to access monitors belonging to their own account.

---

# Frontend

The frontend will use **Next.js**.

Initial pages:

```text
/login
/register
/dashboard
/monitors
/monitors/[monitor_id]
/incidents
/settings
```

The dashboard should provide:

* Current monitor status
* Uptime
* Response latency
* Recent checks
* Incident history
* Latency history
* Monitor management
* Account information

The frontend will communicate exclusively with the FastAPI API.

---

# Technology Stack

## Backend

```text
Language: Python
Framework: FastAPI
Validation: Pydantic
ORM: SQLAlchemy
Database: PostgreSQL
Migrations: Alembic
Authentication: JWT
Password Hashing: Argon2 or bcrypt
Testing: pytest
Linting/Formatting: Ruff
```

## Frontend

```text
Language: TypeScript
Framework: Next.js
UI: React
```

## Asynchronous Processing

```text
Redis
Scheduler
Worker
```

The worker implementation will be selected during development.

Possible technologies include:

* ARQ
* Celery
* RQ

The decision should be documented based on the project's actual requirements.

## Infrastructure

```text
Docker
Docker Compose
Nginx
Linux
AWS EC2
AWS Route 53
AWS CloudWatch
```

## CI/CD

```text
GitHub Actions
```

---

# Repository Structure

```text
service-monitor/
│
├── backend/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── schemas/
│   │   ├── services/
│   │   └── main.py
│   │
│   ├── worker/
│   ├── scheduler/
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   └── nextjs/
│       ├── app/
│       ├── components/
│       ├── lib/
│       └── ...
│
├── nginx/
│   └── nginx.conf
│
├── .github/
│   └── workflows/
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

The project will use a **monorepo** because the frontend and backend are part of the same application and are being developed together.

---

# Roadmap

## Phase 1 — Backend Foundation

* [x] Create FastAPI project
* [x] Configure project structure
* [x] Configure PostgreSQL
* [x] Configure SQLAlchemy
* [x] Configure Alembic
* [x] Create database models
* [x] Configure Pydantic
* [x] Implement Monitor model
* [x] Implement Monitor CRUD
* [x] Add API versioning
* [x] Add validation
* [x] Add error handling
* [x] Configure Swagger/OpenAPI
* [x] Add unit tests


---

## Phase 2 — Authentication

* [ ] Create User model
* [ ] Implement registration
* [ ] Implement login
* [ ] Implement password hashing
* [ ] Implement JWT access token
* [ ] Implement refresh token
* [ ] Implement token expiration
* [ ] Implement authentication dependencies
* [ ] Implement authorization
* [ ] Associate monitors with users
* [ ] Ensure user data isolation
* [ ] Add authentication tests

---

## Phase 3 — Monitoring Engine

* [ ] Implement HTTP checks
* [ ] Validate HTTP status codes
* [ ] Measure response latency
* [ ] Implement timeout handling
* [ ] Handle connection errors
* [ ] Create CheckResult model
* [ ] Store check results
* [ ] Determine UP/DOWN status
* [ ] Add monitoring tests

---

## Phase 4 — Redis, Scheduler and Worker

* [ ] Add Redis
* [ ] Implement scheduler
* [ ] Implement job queue
* [ ] Implement worker
* [ ] Enqueue monitoring jobs
* [ ] Consume monitoring jobs
* [ ] Execute checks asynchronously
* [ ] Store results in PostgreSQL
* [ ] Implement retry mechanism
* [ ] Prevent duplicate jobs
* [ ] Handle worker failures

---

## Phase 5 — Incidents

* [ ] Detect service failure
* [ ] Create incident when a monitor goes DOWN
* [ ] Detect service recovery
* [ ] Resolve incidents
* [ ] Calculate incident duration
* [ ] Store failure reason
* [ ] Prevent duplicate incidents

Example:

```text
UP
 │
 │ failure
 ↓
DOWN
 │
 │ create incident
 ↓
INCIDENT
 │
 │ recovery
 ↓
UP
 │
 │ resolve incident
 ↓
INCIDENT RESOLVED
```

---

## Phase 6 — Next.js Dashboard

* [ ] Create Next.js application
* [ ] Create login page
* [ ] Create registration page
* [ ] Implement authentication flow
* [ ] Create dashboard
* [ ] Create monitor list
* [ ] Create monitor creation form
* [ ] Create monitor details page
* [ ] Display current status
* [ ] Display latency
* [ ] Display historical checks
* [ ] Display incidents
* [ ] Add charts
* [ ] Implement periodic data refresh

WebSocket will **not** be required initially.

Real-time updates can be added later if there is a concrete requirement for them.

---

## Phase 7 — Docker

* [ ] Create backend Dockerfile
* [ ] Create frontend Dockerfile
* [ ] Configure Docker Compose
* [ ] Containerize FastAPI
* [ ] Containerize Next.js
* [ ] Containerize PostgreSQL
* [ ] Containerize Redis
* [ ] Containerize Worker
* [ ] Containerize Scheduler
* [ ] Containerize Nginx
* [ ] Configure environment variables
* [ ] Configure persistent volumes
* [ ] Configure internal Docker network
* [ ] Add health checks
* [ ] Configure restart policies

Expected architecture:

```text
Docker Compose
│
├── nginx
├── frontend
├── backend
├── worker
├── scheduler
├── redis
└── postgres
```

---

## Phase 8 — Nginx and Networking

* [ ] Configure Nginx
* [ ] Configure reverse proxy
* [ ] Configure frontend routing
* [ ] Configure API routing
* [ ] Configure HTTP headers
* [ ] Configure HTTPS
* [ ] Configure TLS certificates
* [ ] Configure domain
* [ ] Understand DNS resolution
* [ ] Understand ports and sockets
* [ ] Document network flow

Example:

```text
monitor.example.com
        │
        ↓
      Nginx
        │
        ↓
     Next.js
```

```text
api.monitor.example.com
        │
        ↓
      Nginx
        │
        ↓
     FastAPI
```

---

## Phase 9 — AWS Deployment

* [ ] Create AWS EC2 instance
* [ ] Configure Security Groups
* [ ] Configure SSH access
* [ ] Install Docker
* [ ] Deploy application
* [ ] Configure domain
* [ ] Configure Route 53
* [ ] Configure HTTPS
* [ ] Configure environment variables
* [ ] Configure CloudWatch
* [ ] Document infrastructure
* [ ] Document deployment process

Initial deployment will intentionally use a relatively simple architecture.

The project can later evolve toward:

```text
EC2
  ↓
ECS
  ↓
RDS
  ↓
Application Load Balancer
```

if there is a technical reason to do so.

---

## Phase 10 — CI/CD

Initial pipeline:

```text
Push
  ↓
Lint
  ↓
Type Check
  ↓
Tests
  ↓
Build
```

Production pipeline:

```text
Push to main
     ↓
Tests
     ↓
Docker Build
     ↓
Deploy
     ↓
Health Check
```

Tasks:

* [ ] Configure GitHub Actions
* [ ] Run backend tests
* [ ] Run frontend checks
* [ ] Run linting
* [ ] Run type checking
* [ ] Build Docker images
* [ ] Configure deployment
* [ ] Configure GitHub Secrets
* [ ] Add deployment health check
* [ ] Document rollback strategy

---

## Phase 11 — Observability

* [ ] Structured logging
* [ ] Application health checks
* [ ] Worker health checks
* [ ] Metrics
* [ ] CloudWatch logs
* [ ] CloudWatch metrics
* [ ] Alerts
* [ ] Error tracking

An important concept of the project will be:

> **Monitoring the monitoring system.**

---

## Phase 12 — Advanced Features

Only implement these features when there is a clear technical reason:

* [ ] TCP monitoring
* [ ] Ping monitoring
* [ ] Response body validation
* [ ] JSON response validation
* [ ] Retries
* [ ] Exponential backoff
* [ ] Rate limiting
* [ ] Notification system
* [ ] Email notifications
* [ ] Discord/Telegram notifications
* [ ] Public status pages
* [ ] WebSocket real-time updates
* [ ] Advanced analytics
* [ ] Multi-region monitoring
* [ ] Next.js performance improvements
* [ ] AWS ECS
* [ ] AWS RDS
* [ ] Application Load Balancer
* [ ] Terraform

---

# Testing

The project should contain different levels of tests.

## Unit Tests

Test isolated business logic.

Examples:

```text
HTTP 200 → UP
HTTP 500 → DOWN
Timeout → DOWN
Connection error → DOWN
```

## Integration Tests

Test interactions between:

```text
FastAPI
PostgreSQL
Redis
Worker
```

## API Tests

Test:

* Authentication
* Authorization
* Monitor CRUD
* Validation
* Error responses
* User data isolation

## Worker Tests

Test:

* Job consumption
* HTTP checks
* Result persistence
* Retry behavior
* Failure handling

---

# Security

Security must be considered throughout development.

Requirements:

* Never commit secrets
* Never commit `.env`
* Use `.env.example`
* Use environment variables
* Use GitHub Secrets for CI/CD
* Hash passwords securely
* Validate JWT tokens
* Implement authorization
* Restrict AWS Security Groups
* Use HTTPS
* Validate monitored URLs
* Implement SSRF protection
* Implement rate limiting
* Validate user input
* Avoid exposing internal errors
* Do not log passwords or tokens

Because the application allows users to register arbitrary URLs for monitoring, **SSRF protection is particularly important**.

---

# Metrics

The system should eventually calculate:

* Uptime percentage
* Total checks
* Successful checks
* Failed checks
* Average latency
* Minimum latency
* Maximum latency
* P50 latency
* P95 latency
* P99 latency
* Incident count
* Total downtime
* Average incident duration

---

# Architecture Principles

1. Keep the architecture simple.
2. Do not add technology without a reason.
3. Separate responsibilities between components.
4. Keep the API independent from the monitoring worker.
5. Use Redis for task transport, not permanent data storage.
6. Use PostgreSQL for persistent application data.
7. Do not allow the frontend to access the database directly.
8. Do not execute monitoring checks synchronously inside API requests.
9. Avoid premature microservices.
10. Prefer a modular architecture before introducing distributed services.
11. Every significant architectural decision should have a clear justification.
12. Optimize for learning real engineering concepts rather than maximizing the number of technologies.

---

# MVP

The initial MVP will contain:

```text
Next.js
    ↓
FastAPI
    ↓
PostgreSQL

Scheduler
    ↓
Redis
    ↓
Worker
    ↓
HTTP Checks
    ↓
PostgreSQL
```

Features:

* User registration
* User login
* JWT authentication
* Monitor creation
* Monitor management
* HTTP monitoring
* UP/DOWN status
* Response latency
* Check history
* Basic incidents
* Basic dashboard

The MVP should be functional before implementing advanced infrastructure features.

---

# Learning Goals

This project is intended to provide practical experience with:

### Backend

* REST APIs
* FastAPI
* SQLAlchemy
* PostgreSQL
* Authentication
* Authorization
* Data modeling
* Async processing
* Background workers
* Queues

### Frontend

* Next.js
* React
* TypeScript
* Authentication flows
* API integration
* Dashboard development

### Infrastructure

* Linux
* Networking
* DNS
* TCP
* HTTP
* HTTPS
* TLS
* Reverse proxies
* Nginx
* Docker
* Docker Compose

### Cloud

* AWS EC2
* Route 53
* CloudWatch
* Security Groups
* Deployment

### DevOps

* GitHub Actions
* CI/CD
* Containerized deployments
* Environment management
* Health checks

### Distributed Systems

* Queues
* Workers
* Scheduling
* Retries
* Failure handling
* Decoupled components

---

# Current Status

```text
Phase 1 — Backend Foundation: Completed
Phase 2 — Authentication: Ready to start
```


---

# License

This project is developed for educational and portfolio purposes.

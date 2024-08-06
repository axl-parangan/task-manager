# Task Manager

Task Manager is a Django-based web application designed to manage and track tasks. It uses Celery for handling background jobs and periodic tasks, and Redis as the message broker.

## Features

- Task management (CRUD operations)
- Background job processing with Celery
- Periodic task scheduling with Celery Beat
- Monitoring with Flower
- Optimized for high load and concurrency

## Setup Instructions

### Prerequisites

- Docker
- Docker Compose

### Installation

1. **Clone the repository:**
   https://github.com/axl-parangan/task-manager.git
3. **Build and run the Docker containers:**
`docker-compose build`
4. **Start the application**
`docker-compose up`

This will start the following services:

    Django application server
    PostgreSQL database
    Redis message broker
    Celery worker
    Celery Beat scheduler
    Flower monitoring tool

### Accessing the application

    Django application: http://localhost:8000

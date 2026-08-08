# DevOps Log Analyzer

A **FastAPI + Elasticsearch** service for collecting, searching, classifying, and archiving application logs.

The project demonstrates how application logs can be centralized in Elasticsearch and accessed through a REST API. It also includes automatic log classification, filtering, aggregation, and scheduled archiving.

## Features

- Collect application logs through a REST API
- Store logs in **Elasticsearch**
- Search logs using full-text search
- Filter logs by time range, log level, error type, and tags
- Sort and limit search results
- Update and delete logs
- Aggregate logs by log level
- Automatically archive old logs into a separate Elasticsearch index
- Delete old logs based on a time range
- Classify logs using a simple ML-based approach
- Tag logs by categories such as `DB`, `Network`, `Authorization`, `Payment`, and `Timeout`
- Scheduled background tasks using `BackgroundScheduler`
- Dockerized application and Elasticsearch environment
- Automated tests

## Tech Stack

| Technology | Purpose |
|---|---|
| Python | Backend development |
| FastAPI | REST API |
| Elasticsearch | Log storage and search |
| Pydantic | Data validation |
| Docker | Containerization |
| BackgroundScheduler | Scheduled archiving |
| Machine Learning | Log classification |
| Pytest | Automated testing |

## Architecture

The application consists of two main services:

```text
Application / Client
        |
        v
   FastAPI REST API
        |
        v
   Elasticsearch
        |
        +---- Logs Index
        |
        +---- Archive Index
```

FastAPI provides the REST API, while Elasticsearch is responsible for storing and searching log data.

## Log Structure

Each log contains basic information such as:

```json
{
  "timestamp": "2026-01-15T10:30:00",
  "level": "ERROR",
  "message": "Database connection failed",
  "tags": ["DB"]
}
```

The service can use the log information for searching, filtering, aggregation, classification, and archiving.

## Setup

### Requirements

- Docker
- Docker Compose

### Start the application

Build the images and start the containers:

```bash
docker compose up --build
```

The API will be available at:

```text
http://localhost:8000
```

FastAPI's interactive API documentation is available at:

```text
http://localhost:8000/docs
```

### Start in detached mode

```bash
docker compose up -d
```

To follow the logs of the FastAPI container:

```bash
docker compose logs -f app
```

### Stop the application

```bash
docker compose down
```

## API Examples

### Add a log

```bash
curl -X POST "http://localhost:8000/logs/add" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "Database connection failed",
    "level": "ERROR"
  }'
```

### Search logs

```bash
curl -X GET "http://localhost:8000/logs/search?query=error"
```

The search endpoint can be used to find logs containing a specific text.

### Interactive API documentation

After starting the application, the available endpoints can also be tested through the automatically generated Swagger UI:

```text
http://localhost:8000/docs
```

## Elasticsearch Index

The application automatically creates the required logs index if it does not already exist.

When mappings need to be changed, the existing index has to be removed and recreated with the updated mapping.

## Log Archiving

Old logs can be archived automatically based on their age.

The archiving process:

1. Finds logs older than the configured time range.
2. Copies them to a separate Elasticsearch archive index.
3. Removes the archived logs from the active index.

This keeps the active log index smaller while preserving older data for later analysis.

## Machine Learning Classification

The service includes a basic ML-based classification approach for categorizing logs.

Logs can be classified into categories such as:

- `error`
- `info`
- database-related issues
- network-related issues
- authorization issues
- payment-related issues
- timeout-related issues

The classification can be extended with additional categories or a more advanced model.

## Testing

The project includes automated tests for the application.

Tests can be run inside the development environment with:

```bash
pytest
```

## Project Purpose

This project was created to demonstrate practical backend development concepts including:

- REST API design
- Elasticsearch integration
- Full-text search
- Data validation
- Background jobs
- Log management
- Machine learning integration
- Docker containerization
- Automated testing

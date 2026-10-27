# AI-Powered Document Processing Platform

> **Status:** Completed. Built as a portfolio project with an enterprise-style architecture. Not deployed for production use.

A document intake platform that automatically classifies and routes incoming documents to the right department. It is designed for scenarios where large volumes of unstructured documents arrive through digital channels such as email attachments or file uploads, and where manual sorting is slow and error-prone.

## Features

- **Document intake:** receive documents from file uploads and email attachments.
- **Automatic classification:** an AI model assigns each document to a category.
- **Routing:** documents are sent to the matching department inbox.
- **Validation of uncertain cases:** documents the model is not confident about are flagged for manual review.
- **Departmental inbox management:** each department sees and manages its own documents.
- **Asynchronous processing:** ingestion and classification run in the background through a message queue, so user requests are not blocked.
- **Object storage:** documents are stored in an S3-compatible object store (MinIO).

## Tech Stack

- **AI / Data:** Python, dataset creation and curation, custom document classification model
- **Backend:** Python services, RabbitMQ for asynchronous messaging
- **Frontend:** React (validation and review dashboard)
- **Data & storage:** PostgreSQL, MinIO (S3-compatible)
- **Tooling:** Git, GitHub

## Architecture

The platform is split into services that communicate through RabbitMQ. Incoming documents are stored in MinIO and published as messages. A classification worker consumes these messages, assigns a category and publishes a routing event. A routing service delivers the document to the matching department inbox, and documents below the confidence threshold are sent to a review queue handled from the React dashboard.

```
Upload / Email  ->  Intake  ->  MinIO
                      |
                  RabbitMQ
                      |
        Classification worker (ML model)
                      |
              Routing service  ->  Department inbox
                      |
              Low confidence  ->  Manual review (React)
```

## Model

- **Approach:** [describe the model type, e.g., text vectorization + classifier]
- **Dataset:** [number of documents, number of classes, how the data was collected and labelled]
- **Evaluation:** [metric, test set size, and result]

## Getting Started

### Prerequisites

- Python [version]
- Docker and Docker Compose
- Node.js [version] and npm

### Run the infrastructure

```bash
docker compose up -d   # PostgreSQL, RabbitMQ, MinIO
```

### Run the services

```bash
pip install -r requirements.txt
python -m [service_module]
```

### Run the dashboard

```bash
cd [frontend-folder]
npm install
npm start
```

### Configuration

| Variable | Description |
| --- | --- |
| `DATABASE_URL` | PostgreSQL connection string |
| `RABBITMQ_URL` | RabbitMQ connection string |
| `MINIO_ENDPOINT` | MinIO endpoint |
| `MINIO_ACCESS_KEY` | MinIO access key |
| `MINIO_SECRET_KEY` | MinIO secret key |

## Author

**Raul-Gabriel Chiorean**
Software Engineer | Java Backend & Full Stack
[LinkedIn](https://www.linkedin.com/in/raul-chiorean-003039337/)

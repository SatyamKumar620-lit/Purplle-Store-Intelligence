# Purplle Store Intelligence System

## Overview

This project is an AI-powered retail analytics system that processes CCTV footage from multiple stores and generates actionable business insights.

The system detects and tracks visitors using computer vision, generates visitor events, stores them in a database, exposes analytics APIs through FastAPI, and visualizes insights using a Streamlit dashboard.

---

## Features

### Visitor Analytics

* Person Detection using YOLOv8
* Multi-object Tracking
* Visitor Entry Detection
* Visitor Exit Detection
* Dwell Time Calculation
* Zone Visit Tracking

### Event Processing

* Event Generation Pipeline
* JSONL Event Logging
* SQLite Event Storage
* Store-wise Analytics

### Dashboard

* Visitor Metrics
* Entry / Exit Analytics
* Dwell Time Analytics
* Camera Analytics
* Zone Analytics
* Store Comparison
* Conversion Funnel
* Traffic Analysis
* AI Business Insights

### APIs

* Health Endpoint
* Analytics Endpoint
* Metrics Endpoint
* Anomalies Endpoint
* Ingestion Endpoint

### Deployment

* Docker Support
* Docker Compose Support
* Swagger Documentation

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLite

### Computer Vision

* YOLOv8
* OpenCV
* Supervision

### Analytics

* Pandas
* NumPy

### Dashboard

* Streamlit

### Deployment

* Docker
* Docker Compose

---

## Project Structure

store-intelligence-template/

├── app/

├── dashboard/

├── pipeline/

├── data/

├── store.db

├── events.jsonl

├── Dockerfile

├── docker-compose.yml

├── requirements.txt

└── README.md

---

## Installation

### Clone Repository

```bash
git clone <repository-url>
cd store-intelligence-template
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Database

```bash
python create_db.py
```

---

## Running Event Processing

Process CCTV videos:

```bash
python run_all_stores.py
```

Events are stored in:

* SQLite Database
* events.jsonl

---

## Running FastAPI

```bash
uvicorn app.main:app --reload
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

## Running Dashboard

```bash
streamlit run dashboard/app.py
```

Dashboard:

```text
http://localhost:8501
```

---

## Running With Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

Swagger:

```text
http://localhost:8000/docs
```

---

## Analytics Generated

* Unique Visitors
* Total Entries
* Total Exits
* Average Dwell Time
* Zone Visits
* Camera Performance
* Store Performance
* Peak Traffic Hours
* Visitor Conversion Funnel

---

## Future Improvements

* Real-time Video Streaming
* Heatmap Generation
* Customer Journey Analysis
* Queue Detection
* Product Interaction Analytics
* Cloud Deployment

---

## Author

Satyam Pathak
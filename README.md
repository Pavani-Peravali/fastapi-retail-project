# FastAPI Retail Data Project

## Overview
This project is a FastAPI-based backend that exposes APIs for retail data analysis using real-world e-commerce datasets.

## Features
- Customer and invoice APIs
- Dataset integration using pandas
- Invoice and customer-level data retrieval
- Total invoice amount calculation
- Dockerized application

## Tech Stack
- Python
- FastAPI
- Pandas
- Docker

## How to Run (Docker)

### Pull Image
docker pull pavani666/fastapi-retail-app

### Run Container
docker run -d -p 8000:8000 pavani666/fastapi-retail-app

### Access API
http://127.0.0.1:8000/docs

## Sample Endpoints
- /dataset/summary
- /dataset/invoice/{invoice_no}
- /dataset/customer/{customer_id}

## Author
Pavani
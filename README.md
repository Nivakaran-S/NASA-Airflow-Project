# Airflow ETL Pipeline with Postgres and NASA API Integration

## Project Overview

This project demonstrates a **robust ETL (Extract, Transform, Load) pipeline** built using **Apache Airflow**. The pipeline extracts data from an external API—**NASA's Astronomy Picture of the Day (APOD) API**—transforms it into a structured format, and loads it into a **Postgres database**. Airflow orchestrates the entire workflow, allowing for scheduling, monitoring, and managing the pipeline efficiently.

The project leverages **Docker** to run Airflow and Postgres as isolated services, ensuring a reproducible environment. By using Airflow hooks and operators, the ETL process is automated, reliable, and easy to maintain.

---

## Key Components

### Apache Airflow
Airflow manages the ETL workflow using **Directed Acyclic Graphs (DAGs)**. Each DAG defines tasks and their dependencies, ensuring the pipeline runs sequentially and reliably. Tasks include **data extraction**, **transformation**, and **loading**.

### Postgres Database
A **PostgreSQL database** stores the transformed data. Postgres is hosted in a Docker container, ensuring easy management and data persistence through Docker volumes. Interaction with the database is handled via **Airflow’s PostgresHook and PostgresOperator**.

### NASA APOD API
The pipeline extracts data from **NASA's Astronomy Picture of the Day (APOD) API**, which provides metadata such as the **title**, **description**, **image URL**, and **date**. Airflow’s **SimpleHttpOperator** handles API requests efficiently.

---

## Project Objectives

1. **Extract Data**  
   The pipeline automatically fetches astronomy-related data from NASA's APOD API on a **daily schedule**.

2. **Transform Data**  
   Extracted data is cleaned and transformed using Airflow’s TaskFlow API. Relevant fields—such as `title`, `explanation`, `url`, and `date`—are formatted to be compatible with the Postgres database.

3. **Load Data into Postgres**  
   Transformed data is inserted into Postgres. If the target table does not exist, it is automatically created as part of the DAG.

---

## ETL Workflow Architecture

The ETL pipeline consists of three main stages:

1. **Extract (E)**  
   - Uses `SimpleHttpOperator` to make HTTP GET requests to the NASA APOD API.  
   - Retrieves JSON data containing fields like `title`, `explanation`, `url`, and `date`.

2. **Transform (T)**  
   - Processes the extracted JSON using Airflow’s `@task` decorator.  
   - Filters and formats the relevant fields for database insertion.

3. **Load (L)**  
   - Inserts the transformed data into a Postgres table using `PostgresHook`.  
   - Ensures automatic table creation if it does not already exist.

---

## Project Highlights

- Fully automated ETL workflow orchestrated by **Airflow DAGs**.  
- Seamless **API integration** with NASA’s APOD.  
- **Dockerized setup** for Airflow and Postgres ensures portability and reproducibility.  
- Database-ready data for **analysis, reporting, or visualization**.  
- Easily extendable to include additional APIs or transformations.

---

## Sample Data

| Date       | Title                    | URL                        | Explanation (truncated)                 |
|------------|-------------------------|----------------------------|---------------------------------------|
| 2025-08-14 | Cosmic Dawn              | https://apod.nasa.gov/... | This image shows the early universe… |

---

## How to Run

1. Clone the repository:
   
```bash
   
git clone https://github.com/yourusername/airflow-etl-nasa.git

```

2. Start Docker services:

```bash

docker-compose up -d

```

3. Access Airflow UI at http://localhost:8080 to trigger or monitor the DAG.

---

## Future Improvements

- Add support for multiple NASA APIs (e.g., Mars Rover Photos, Earth Imagery).
- Integrate data visualization dashboards using tools like Tableau or Power BI.
- Implement data quality checks to ensure API data integrity.
- Enable historical backfill for past APOD entries.

---

## Technologies Used

- Apache Airflow – workflow orchestration
- PostgreSQL – relational database
- Docker & Docker Compose – containerization
- Python – ETL scripting
- NASA APOD API – external data source
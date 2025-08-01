# Airflow ETL Pipeline wiht Postgres and API Integration
## Project Overview: 

This project involves creating an ETL (Extract, Transform, Load) pipeline using Apahe Airflow. The pipeline extracts data from an external API ( in this case, NASA's Astronomy Picture of the Day (APOD) API), transforms the data, and loads it into a Postgres database. The entire workflow is orchestrated by Airflow, a platform that allows scheduling, monitoring, and managing workflows.

The project leverates Docker to run Airflow and Postgres as services, ensuring an isolated and reproducible enviornemtn. We also utilize Airflow hoocks and operators to handle the ETL process efficiently.

## Key Components of the Project: Airflow for Orchestration:

Airflow is used to define, schedule, and monitor the entier ETL pipeline. It manages task dependencies, ensuring that the process runs sequentially and reliably. The Airflow DAG (Directed Acyclic Graph) defines the workflow, which includes tasks like data extraction, transformation, and loading. 

### Postgres Database:

A PostgresSQL database is used to store the extracted and transformed data. Postgres is hosted in a Docker container, making it easy to manage and ensuring data persistence through Docker volumes. We interact with Postgres using Airflow's PostgresHook and PostgresOperator. 

### NASA API (Astronomy Picture of the Day):

The external API used in this project is NASA's APOD API, which provides data about the astronomy picture of the day, including metadata like the tilte, explanation, and the URL of the image. We use Airflow's SimpleHttpOperator to extract data from the API. 

## Objectives of the Project: 

### 1. Extract Data:
THe pipeline extracts astronomy-related data from NASA's APOD API on a scheduled basis (daily, in this case). 

### 2. Transform Data:
Transformation such as filtering or processing the API response are performed to ensure that the data is in a suitable format before being insrted into teh database. 

### 3. Load Data into Postgres
The transformed data is loaded into a Postgres database. The datag can be used for further analysis, reporting, or visualization. 

### 4. Architecture and Workflow: 
The ETL pipeline is orchestrawted in Airflow using a DAG (Directed Acyclic Graph). The pipeline consists of the following stages:

1. Extract(E): SimpleHttpOperator is ued to make HTTP GET requests to NASA's APOD API. The response  is in JSON format, containing fields like the title of the picture, the explanation, and the URL to the image. 
2. Transform (T): The extracted JSON data is processed in the transform task using Airflow's TaskFlow API (with the @task decorator). This stage involves extracting relevant fields like title, explanation, url, and date and ensuring they are in the correct format for the database. 
3. Load (L): The transformed data is    loaded into a Postgres tabble using PostgresHook. If the target table doesn't exist in the Postgres database, it is created automatically as part of the DAG using a create table task. 
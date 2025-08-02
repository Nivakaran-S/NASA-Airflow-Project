from airflow import DAG
from airflow.providers.http.operators.http import HttpOperator
from airflow.decorators import task
from airflow.providers.postgres.hooks.postgres import PostgresHook
import pendulum
import logging
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define the DAG
with DAG(
    dag_id='nasa_apod_postgres',
    start_date=pendulum.today('UTC').subtract(days=1),
    schedule='@daily',
    catchup=False,
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'retry_delay': 300,
    },
    description='Fetch NASA APOD data and store in PostgreSQL',
    tags=['nasa', 'apod', 'postgres'],
) as dag:

    # Step 1: Create the table if it does not exist
    @task
    def create_table() -> None:
        try:
            postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS apod_data (
                id SERIAL PRIMARY KEY,
                title VARCHAR(255),
                explanation TEXT,
                url TEXT,
                date DATE,
                media_type VARCHAR(50)
            );
            """
            postgres_hook.run(create_table_query)
            logger.info("Table apod_data created or already exists")
        except Exception as e:
            logger.error(f"Failed to create table: {e}")
            raise

    # Step 2: Extract NASA APOD data
    extract_apod = HttpOperator(
        task_id='extract_apod',
        http_conn_id='nasa_api',
        endpoint='planetary/apod',
        method='GET',
        data={"api_key": "{{ conn.nasa_api.extra_dejson.api_key }}"},
        response_filter=lambda response: response.json(),
        log_response=True,
    )

    # Step 3: Transform the data
    @task
    def transform_apod_data(response: Dict[str, Any]) -> Dict[str, str]:
        try:
            apod_data = {
                'title': response.get('title', ''),
                'explanation': response.get('explanation', ''),
                'url': response.get('url', ''),
                'date': response.get('date', ''),
                'media_type': response.get('media_type', '')
            }
            logger.info(f"Transformed APOD data: {apod_data['title']}")
            return apod_data
        except Exception as e:
            logger.error(f"Failed to transform data: {e}")
            raise

    # Step 4: Load the data into PostgreSQL
    @task
    def load_data_to_postgres(apod_data: Dict[str, str]) -> None:
        try:
            postgres_hook = PostgresHook(postgres_conn_id="my_postgres_connection")
            insert_query = """
            INSERT INTO apod_data (title, explanation, url, date, media_type)
            VALUES (%s, %s, %s, %s, %s);
            """
            postgres_hook.run(insert_query, parameters=(
                apod_data['title'],
                apod_data['explanation'],
                apod_data['url'],
                apod_data['date'],
                apod_data['media_type']
            ))
            logger.info(f"Inserted APOD data for date: {apod_data['date']}")
        except Exception as e:
            logger.error(f"Failed to load data to PostgreSQL: {e}")
            raise

    # Step 5: Define task dependencies
    create_table_task = create_table()
    transform_task = transform_apod_data(extract_apod.output)
    load_task = load_data_to_postgres(transform_task)

    create_table_task >> extract_apod >> transform_task >> load_task
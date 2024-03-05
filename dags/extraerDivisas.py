'''
Propósito del Dag : Extraer par de divisas elegido.
Fecha : 04/03/2024.
Autor : Guillermo Sánchez.
'''
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
from datetime import datetime, timedelta

default_args = {
    'owner': 'Guillermo Sánchez',
    'start_date': datetime(2024, 2, 28),
    'catchup': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'email': 'guillermo.sanchezperez@zelenza.com'
}

def actualizar_divisas():
    try:
        # Realizar solicitud GET al endpoint
        endpoint = 'http://localhost:5678/webhook-test/0cd66f0c-1aa7-47b6-9180-8caf3049f106'
        response = requests.get(endpoint)
        
        # Verificar el código de estado de la respuesta
        response.raise_for_status()
        print('Solicitud exitosa. Código de estado:', response.status_code)
    except Exception as e:
        # Manejar errores
        print('Error al realizar la solicitud:', str(e))

with DAG('actualizar_divisas_dag',
         default_args=default_args,
         schedule_interval='*/1 * * * *') as dag:

    actualizar_divisas_task = PythonOperator(
        task_id='actualizar_divisas',
        python_callable=actualizar_divisas
    )

    actualizar_divisas_task

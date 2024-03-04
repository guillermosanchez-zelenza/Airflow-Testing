'''
Propósito del Dag : Registro de usuarios : LIMITE 20 .
Fecha : 04/03/2024.
Autor : Guillermo Sánchez.
'''
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import requests
from datetime import datetime, timedelta

default_args = {
    'owner': 'guille',
    'start_date': datetime(2024, 2, 28),
    'catchup': True,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email':'guillermo.sanchezperez@zelenza.com'
}

def registrar_usuarios():
    # Realizar solicitud GET al endpoint
    endpoint = 'http://localhost:5678/webhook-test/2a8a227b-13f5-4b75-954f-a34830a6bb59'
    response = requests.get(endpoint)
    
    # Imprimir el código de estado de la respuesta para verificar
    print('Código de estado de la solicitud hacia endpoint N8N:', response.status_code)

with DAG('registro_usuarios_dag',
         default_args=default_args,
         schedule_interval='0 12 * * *') as dag:

    registrar_usuarios_task = PythonOperator(
        task_id='registrar_usuarios',
        python_callable=registrar_usuarios
    )

    registrar_usuarios_task

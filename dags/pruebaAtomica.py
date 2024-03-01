'''
Propósito del Dag : Prueba Atomica Transiciones de datos.
Fecha : 28/02/2024.
Autor : Guillermo Sánchez.
'''
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.mysql_hook import MySqlHook
import requests
from random import randint
from datetime import datetime, timedelta

#Argumento end_date tambien disponible para programar una fecha en la que ya no queramos que el DAG se ejecute.
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

def get_exchange_rate():
    # Realiza la solicitud GET a la API
    api_key = "0713f7e4cfd2dc1b59404834"
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/EUR'
    response = requests.get(url)
    
    # Almacena la respuesta en una variable
    response_variable = response.json()
    
    # Imprime la respuesta para verificar
    print(response_variable)

def insert_data_to_mysql(**kwargs):
    # Crear una conexión con la base de datos MySQL utilizando el hook de MySQL
    mysql_hook = MySqlHook(mysql_conn_id='MySQL')
    
    # Definir la consulta de inserción, formatear el output de la tarea anterior.
    query = """
        INSERT INTO my_table (column1, column2, column3, created_at)
        VALUES (%s, %s, %s, %s)
    """
    
    # Datos a insertar
    data_to_insert = [
        ('value1', 'value2', 'value3', datetime.now()),
        ('value4', 'value5', 'value6', datetime.now())
        # Puedes agregar más datos aquí según sea necesario
    ]
    
    # Ejecutar la consulta de inserción para cada conjunto de datos
    for data in data_to_insert:
        mysql_hook.run(query, parameters=data)

# Define el DAG
with DAG('combined_dags', 
         schedule_interval='* * * * *',  # Se ejecuta cada minuto
         default_args=default_args) as dag:
    
    # Define la tarea que obtiene la tasa de cambio
    task_get_exchange_rate = PythonOperator(
        task_id='get_exchange_rate',
        python_callable=get_exchange_rate
    )

    # Define la tarea que inserta datos en MySQL
    task_insert_data_to_mysql = PythonOperator(
        task_id='insert_data_to_mysql',
        python_callable=insert_data_to_mysql
    )

    # Establece la dependencia de las tareas
    task_get_exchange_rate >> task_insert_data_to_mysql
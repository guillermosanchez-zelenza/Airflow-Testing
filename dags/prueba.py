'''
Proposito del Dag : Elección de branch random con mensaje inicial y final.
Fecha : 31/01/2024.
Autor : Rafael de Troya. Guillermo Sánchez
'''
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
#Libreria con error de importación
from airflow.operators.python_operator import BranchPythonOperator
from random import randint
from airflow.utils.trigger_rule import TriggerRule
import requests

# Definir la configuración de la tarea DAG, argumento end_date tambien disponible.
default_args = {
    'owner': 'guille',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
}

# Inicializar el objeto DAG
dag = DAG(
    'hola_mundo',
    default_args=default_args,
    description='Un simple DAG que branchea aleatoriamente',
    schedule_interval=timedelta(days=1),  # Frecuencia de ejecución (cada día en este caso)
)

# Definir la tarea que imprime "Hola Mundo"
def print_hello():
    print("Hola Mundo!")

#Retorno random de un numero entre 1 y 0
def choose_branch(**kwargs):
    # Esta función determina dinámicamente a cuál tarea debe ir el flujo
    # Puedes implementar tu propia lógica de decisión aquí.
    if randint(0, 1) == 0:
        return 'branch_a'
    else:
        return 'branch_b'

#Define la tarea que se imprime cuando se ejecuta la primera rama      
def run_this_first(**kwargs):
    # Tarea para el caso de la primera rama
    print("Ejecutando la primera rama")
    #Petición hacia el workflow de generarUsuarios.
    try:
        # Realizar la solicitud GET a la API ipinfo.io
        response = requests.get("https://ipinfo.io")
        
        # Verificar si la solicitud fue exitosa
        response.raise_for_status()
        
        # Imprimir la respuesta
        print('Respuesta de ipinfo.io:', response.text)
    except Exception as e:
        # Manejar cualquier error que ocurra durante la solicitud
        print('Error al realizar la solicitud:', str(e))

#Define la tarea que se imprime cuando se ejecuta la segunda rama      
def run_this_second(**kwargs):
    # Tarea para el caso de la segunda rama
    print("Ejecutando la segunda rama")    

# Definir la tarea que imprime "Adiós Mundo"
def task_final():
    print("Adios Mundo!")

# Crear un operador PythonOperator que ejecutará la función print_hello
hello_task = PythonOperator(
    task_id='print_hello_task',
    python_callable=print_hello,
    dag=dag,
)

#BranchOperator que llama a la funcion choose_branch
branch_op = BranchPythonOperator(
    task_id='branch_task',
    provide_context=True,  # Asegúrate de tener esta línea
    python_callable=choose_branch,
    dag=dag,
)

#Crea un pythonOperator que ejecuta la funcion run_this_first
branch_a = PythonOperator(
    task_id='branch_a',
    python_callable=run_this_first,
    provide_context=True,
    dag=dag,
)

#Crea un pythonOperator que ejecuta la funcion run_this_second
branch_b = PythonOperator(
    task_id='branch_b',
    python_callable=run_this_second,
    provide_context=True,
    dag=dag,
)

# Crear un operador PythonOperator que ejecutará la función print_bye
bye_task = PythonOperator(
    task_id='print_bye_task',
    python_callable=task_final,  # Corregir aquí, cambiar a la función task_final
    trigger_rule=TriggerRule.ONE_SUCCESS,
    dag=dag,
)

# Establecer la dependencia del DAG
hello_task >> branch_op >> [branch_a, branch_b] >> bye_task

if __name__ == "__main__":
    dag.cli()

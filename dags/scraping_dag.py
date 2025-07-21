from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import mysql.connector
from scraping_web import scrape_pagina12  # Importa tu función principal del script


def scrape_and_save():
    # 1. Ejemplo de scraping (ajusta según tu URL)
    url = "https://www.pagina12.com.ar/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 2. Extraer datos (ejemplo)
    datos = []
    for articulo in soup.find_all('article'):
        datos.append({
            'titulo': articulo.find('h2').text,
            'link': articulo.find('a')['href'],
            'fecha': datetime.now().date()
        })
    # 3. Guardar en MySQL
    conn = mysql.connector.connect(
        host="mysql_db",
        user="user",
        password="pass123",
        database="scraped_data"
    )
    cursor = conn.cursor()
    
    for item in datos:
        cursor.execute("""
            INSERT INTO noticias (titulo, link, fecha)
            VALUES (%s, %s, %s)
        """, (item['titulo'], item['link'], item['fecha']))
    
    conn.commit()
    cursor.close()
    conn.close()

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}
dag = DAG(
    'scraping_noticias',
    default_args=default_args,
    schedule_interval='0 6 * * *',  # Ejecución diaria
    catchup=False,
)
tarea = PythonOperator(
    task_id='scrapear_noticias',
    python_callable=scrape_and_save,
    dag=dag
)

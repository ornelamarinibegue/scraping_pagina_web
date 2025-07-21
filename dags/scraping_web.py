import requests
from bs4 import BeautifulSoup
from datetime import datetime
import mysql.connector

def scrape_pagina12():
    url = "https://www.pagina12.com.ar/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Error al acceder al sitio: {response.status_code}")

    soup = BeautifulSoup(response.content, "html.parser")
    articulos = soup.find_all("div", class_="article-title")
    
    noticias = []
    for articulo in articulos:
        titulo = articulo.find("h2").get_text(strip=True) if articulo.find("h2") else None
        link_tag = articulo.find("a")  
        link = link_tag["href"]
        if titulo and link:
            noticias.append({
                "titulo": titulo,
                "link": f"https://www.pagina12.com.ar{link}" if not link.startswith("http") else link,
                "fecha": datetime.today().date()
            })
        else:
            print(f"Falta título o enlace en: {titulo}")

    # Guardar en MySQL
    conn = mysql.connector.connect(
        host="mysql_db",
        user="root",
        password="root",
        database="scraped_data"
    )
    cursor = conn.cursor()
    
    for item in noticias:
        cursor.execute("""
            INSERT INTO noticias (titulo, link, fecha)
            VALUES (%s, %s, %s)
        """, (item['titulo'], item['link'], item['fecha']))
    
    conn.commit()
    cursor.close()
    conn.close()

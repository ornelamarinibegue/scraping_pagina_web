# Scraping Project

Este proyecto utiliza Apache Airflow para realizar scraping de noticias desde el sitio web [Página 12](https://www.pagina12.com.ar) y almacenar los resultados en una base de datos MySQL.

## Estructura del Proyecto
ScrapingProject ├── dags │ ├── scraping_web.py # Código de scraping │ └── scraping_dag.py # Definición del DAG de Airflow ├── logs # Logs generados por Airflow ├── .env # Variables de entorno para Docker └── docker-compose.yaml # Configuración de Docker


## Requisitos

- Docker
- Docker Compose

## Configuración

1. **Clona el repositorio**:

   ```bash
   git clone <URL_DEL_REPOSITORIO>
   cd ScrapingProject

Configura el archivo .env (opcional):

Asegúrate de que las variables de entorno en el archivo .env estén configuradas correctamente para tu entorno.

Construye y ejecuta los contenedores:
docker-compose up -d

Estructura de la Base de Datos
El proyecto crea una tabla en MySQL para almacenar las noticias:

CREATE TABLE IF NOT EXISTS noticias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titulo VARCHAR(255) NOT NULL,
    link VARCHAR(512) NOT NULL,
    fecha DATE NOT NULL
);

Ejecución del DAG
El DAG está programado para ejecutarse diariamente a las 9 AM (hora de Argentina). Puedes verificar el estado del DAG en la interfaz de usuario de Airflow accediendo a:

http://localhost:8080

Acceso a la Interfaz de Airflow
Usuario: admin
Contraseña: admin

Problemas Comunes
Conexión a la Base de Datos: Asegúrate de que las credenciales y el host de MySQL sean correctos.
Tabla No Creada: Verifica que la tabla noticias exista en la base de datos.
Errores en el Scraping: Revisa los logs de Airflow para identificar problemas en la ejecución del DAG.

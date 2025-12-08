# Sistema de Gestión de Clientes, Medidores, Lecturas y Boletas - CGE - Universidad Católica del Maule

Este proyecto es un backend desarrollado con FastAPI para la gestión de clientes, medidores, lecturas y generación de boletas. Está diseñado para facilitar operaciones CRUD y cálculos de consumo de manera eficiente y segura.

## Tecnologías principales

- Python 3.11+
- FastAPI: Framework principal para el desarrollo de la API.
- SQLAlchemy: ORM para comunicación con la base de datos.
- Pydantic: Para validación de datos y definición de schemas.
- MySQL / PyMySQL: Base de datos relacional.
- python-dotenv: Manejo de variables de entorno.

## Configuración y puesta en Marcha

## Pasos
1. Descarga o clona el proyecto via GitHub a través del siguiente Link: https://github.com/Naacho-mp/back_cge
1. Crear un entorno virtual en la raiz del proyecto: Comando a utilizar según Linux/Mac/Windows
2. Activar el entorno virtual.
3. Instalar dependencias contenidas en el Archivo "requirements.txt"
4. Crear el archivo .env en la raiz del proyecto con los siguientes datos:
   - DB_USER
   - DB_PASSWORD
   - DB_HOST
   - DB_NAME
5. De no estar creada la Base de Datos a utilizar, crearla.
6. Entrar a la carpeta del archivo "main.py"
7. Correr el proyecto mediante el comando "fastapi dev main.py"
8. Verificar funcionamiento. 

## Estructura del proyecto

- api/boletas/clientes/lecturas/medidores: Endpoints REST para clientes, medidores, lecturas y boletas.
- app/crud/clientes/lecturas/medidores: Funciones CRUD que interactúan con la base de datos usando SQLAlchemy.
- app/database.py: Configuración de conexión a la base de datos y sesión ORM.
- app/models/: Contiene los modelos ORM que representan las tablas de la base de datos (Clientes, Medidores, Lecturas, Boletas).
- app/schemas/: Definiciones Pydantic para validación y serialización de datos (ClienteCreate, ClienteRead, BoletaOut, etc.).
- calculos/: Funciones auxiliares como validar_rut o cálculo de boletas.
- .env: Variables de entorno para configuración de la base de datos.

## Funcionalidades principales

### Clientes
- Crear, listar, actualizar, eliminar, login, cambio de contraseña de clientes.
- Validación de campos como RUT versión Chile según módulo 11.
- Gestión de relaciones con medidores y boletas.
- Relación 1:N con medidores.
- Relación 1:N con boletas.

### Medidores
- Crear, listar, actualizar y eliminar medidores.
- Gestión de estado y dirección de suministro.
- Relación 1:N con lecturas.

### Lecturas
- Crear y listar lecturas de consumo de medidores.
- Restricción de lectura única por cliente segun medidor + año + mes.
- Lectura no negativa.

### Boletas
- Generación de boletas con cálculo de consumo, tarifa base, cargos, IVA y total.
- Listado de boletas por Rut cliente y periodo (año y mes).
- Restricción de boleta única por Rut cliente + año + mes.





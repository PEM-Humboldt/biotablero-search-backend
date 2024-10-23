# biotablero-search-backend

This is the backend for the search module of BioTablero. It's build with Python.

V.0.1.0

## Getting Started

Required Python version: 3.10+

1. [Optional], create and/or activate the [virtual env](https://docs.python.org/3/library/venv.html) for the project

   > [WIP] Change or add the option to use conda, in that case, include the .yml file in the repo (it might be necessary
   in case we need to use gdal)
1. __Install dependencies__

   `pip install -r requirements.txt`
1. Create an env mirror file of env.sample and update the values of the existing variables.

   ```
   STAC_URL="" # STAC server URL
   ENV="" # Execution Environment
   SECRET_KEY="" # Secret Key for Token Validation
   ALGORITHM="" # Encryption Algorithm
   ACCESS_TOKEN_EXPIRE_MINUTES="" # Number of Expiration Minutes
   USER_USERNAME="" # authentication user
   USER_HASHED_PASSWORD="" # authentication password
   CORS_ORIGIN="" # CORS origin values
   ```
1. Run the the development server

   `uvicorn app.main:app --reload`

## Documentation

The documentation is automatically generated at `/docs` and `/redoc`. For production `/docs` is disabled

## Styles and formatting

[WIP]

## Deploy

[WIP]

# Instalación y Configuración de LocalStack

Este documento describe los pasos necesarios para instalar y configurar LocalStack, así como las herramientas necesarias para su correcto funcionamiento.

## Requisitos previos

Antes de comenzar con la instalación de LocalStack, asegúrate de tener instalados los siguientes componentes en tu máquina:

1. **AWS CLI**: Para la administración de scripts de AWS y LocalStack.
   
   Instala AWS CLI ejecutando el siguiente comando:
   ```bash
   curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
   sudo installer -pkg AWSCLIV2.pkg -target /
    ```
   
2. **Configura AWS CLI con las credenciales para LocalStack:**

   ```bash
   aws configure --profile localstack
   # Introduce las siguientes credenciales
   AWS Access Key ID [None]: test
   AWS Secret Access Key [None]: test
   Default region name [None]: us-east-1
   Default output format [None]: json
   ```
   
3. **Docker:** LocalStack se ejecuta en contenedores Docker, por lo que es necesario tener Docker instalado. Descárgalo e instálalo desde Docker.

4. **jq:** Una herramienta de línea de comandos para procesar JSON, utilizada en los scripts de despliegue. Si no está instalado, puedes hacerlo ejecutando:

    ```bash
    sudo apt-get install -y jq  # Para Linux
    brew install jq             # Para macOS
    ```
   
# Instalación de LocalStack

**Paso 1:** Crear los paquetes para Lambda
Antes de iniciar LocalStack, es necesario empaquetar los archivos de los requisitos para las funciones Lambda.

Ejecuta el siguiente comando para comprimir los paquetes light y heavy requeridos para el despliegue de Lambda:

   ```bash
   python package_lambda.py
   ```

**Paso 2:** Iniciar los servicios con Docker Compose
Inicia los servicios de LocalStack y PostgreSQL utilizando Docker Compose:

```bash
  docker-compose up
```

**Paso 3:** Desplegar LocalStack
Una vez que los contenedores estén en ejecución, ejecuta el script de despliegue `deploy-local.sh` para configurar el entorno:

```bash
  ./deploy-local.sh
```

Este script verificará que todos los servicios de LocalStack estén en ejecución y desplegará la infraestructura necesaria utilizando AWS CDK.

**Paso 4:** Verificar el estado de los servicios

Para verificar que los servicios de LocalStack estén en ejecución, ejecuta el siguiente comando:

```bash
  python check_localstack.py
```

# Comandos útiles de AWS CLI

Listar los servicios en LocalStack

* Listar S3:

```bash
aws --endpoint-url=http://localhost:4566 --profile localstack s3 ls
```

* Listar Lambdas:

```bash
aws --endpoint-url=http://localhost:4566 --profile localstack lambda list-functions
```
* Listar API Gateway:

```bash
aws --endpoint-url=http://localhost:4567 --profile localstack apigateway get-rest-apis
```

* Listar RDS:

```bash
aws --endpoint-url=http://localhost:4566 --profile localstack rds describe-db-instances
```

**Crear nuevos recursos en LocalStack**

* Crear un bucket S3:

```bash
aws --endpoint-url=http://localhost:4566 --profile localstack s3 mb s3://my-bucket
```

* Crear una función Lambda:

```bash
aws --endpoint-url=http://localhost:4566 lambda create-function --function-name <nombre-de-funcion> \
--runtime python3.9 --role arn:aws:iam::000000000000:role/lambda-role \
--handler <archivo.handler> --code S3Bucket=<nombre-del-bucket>,S3Key=<archivo.zip>
```

* Crear un API Gateway:

```bash
aws --endpoint-url=http://localhost:4566 apigateway create-rest-api --name "<nombre-api>"
```

# **Conectarse a la base de datos PostgreSQL**

Para conectarte a la base de datos PostgreSQL en LocalStack, puedes usar las siguientes credenciales:

* **Usuario**: postgres
* **Contraseña**: postgres
* **Base de datos**: localdb
* **Host**: localhost
* **Puerto**: 5432


Puedes conectarte a PostgreSQL con el siguiente comando:

```bash
psql -h localhost -U postgres -d localdb
```

# Notas adicionales
LocalStack se ejecuta en el puerto 4566 de tu máquina local.
Asegúrate de tener permisos de ejecución para los scripts .sh `(chmod +x <script>.sh)`.

Para detener los contenedores de Docker, utiliza:

```bash
docker-compose down
```

## Authors

Línea de Desarrollo - Gerencia de Información Científica - Dirección de conocimiento - Instituto de Investigación de
Recursos Biológicos Alexander von Humboldt - Colombia

See also the list of [contributors](https://github.com/PEM-Humboldt/biotablero-search-backend/graphs/contributors) who
participated in this project.

## License

This project is licensed under the MIT [License](LICENSE).

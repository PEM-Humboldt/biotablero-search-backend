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
   DB_USER=user # Database username 
   DB_PASSWORD=password # Database password 
   DB_NAME=mydatabase # Database name 
   DB_HOST=localhost # Database host
   DB_PORT=5432 # Database port (default for PostgreSQL)
   ```
1. Run Docker Compose to start database containers:
   ```
   docker-compose up -d
   ```
1. Run the the development server

   `uvicorn app.main:app --reload`

## Database Migrations

This project uses `aerich` for database migrations. Below are the necessary commands, explanations, and how to use the dedicated endpoint for migrations.

### Migration Commands

1. **Initialize `aerich`** :
   ```
   aerich init -t app.config.TORTOISE_ORM
   ```
   This sets up aerich with the project’s ORM configuration.

1. **Create the initial migrations**:
   ```
   aerich init-db
   ```
   This command generates the database schema for the first time, regardless of whether the schema already exists. If the database schema does not exist, it will be created. If it already exists, this command will ensure the necessary structure is in place.

2. **Generate new migration files after making changes to models**:

   ```
   aerich migrate
   ```
   
   Use this command whenever you update or modify the models, so the changes can be applied to the database schema.
   Create migration files in the default migration folder, which is typically located at migrations/models/.


3. **Apply all migration files to update the database schema**:

   ```
   aerich upgrade
   ```
   This command applies all pending migrations to the database.


4. **Check migration history**:

   ```
   aerich history
   ```
   Displays a list of all migrations that have been generated.


5. **Rollback a migration**:

   ```
   aerich downgrade
   ```
   Reverts the last migration applied to the database.

### Using the /migrate Endpoint

To run migrations through the API, you can use the /migrate endpoint. This will execute the same commands as the CLI tools, but from within the application.
The /migrate endpoint will internally execute the following commands:

  * aerich migrate
  * aerich upgrade


* **Endpoint**:

  ``` 
   GET /migrate
  ```


## Documentation

The documentation is automatically generated at `/docs` and `/redoc`. For production `/docs` is disabled

## Styles and formatting

[WIP]

## Deploy

[WIP]

## Authors

Línea de Desarrollo - Gerencia de Información Científica - Dirección de conocimiento - Instituto de Investigación de
Recursos Biológicos Alexander von Humboldt - Colombia

See also the list of [contributors](https://github.com/PEM-Humboldt/biotablero-search-backend/graphs/contributors) who
participated in this project.

## License

This project is licensed under the MIT [License](LICENSE).

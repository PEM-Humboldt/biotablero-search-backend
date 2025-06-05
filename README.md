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
   CORS_ORIGIN="" # CORS origin values
   DB_USER=user # Database username 
   DB_PASSWORD=password # Database password 
   DB_NAME=mydatabase # Database name 
   DB_HOST=localhost # Database host
   DB_PORT=5433 # Database port (default for PostgreSQL)
   ```
1. Run Docker Compose to start database containers:
   ```
   docker-compose up -d
   ```
1. Run database migrations:
   ```
   aerich upgrade
   ```
1. Populate the database with initial data:
    
    Follow the steps in the [Migration of Inserts](#migration-of-inserts) section to insert required data.
   
 
7. Run the the development server

   `uvicorn app.main:app --reload`

## Documentation

The documentation is automatically generated at `/docs` and `/redoc`. For production `/docs` is disabled

## Database Migrations

This project uses `aerich` for database migrations. Below are the necessary commands, explanations, and how to use the dedicated endpoint for migrations.

### Migration Commands

- **Initialize `aerich`** :
   ```
   aerich init -t app.utils.config.TORTOISE_ORM
   ```

   This sets up aerich with the project’s ORM configuration.
- **Create the initial migrations**:
   ```
   aerich init-db
   ```
   This command generates the database schema for the first time, regardless of whether the schema already exists. If the database schema does not exist, it will be created. If it already exists, this command will ensure the necessary structure is in place.


- **Generate new migration files after making changes to models**:

   ```
   aerich migrate
   ```
   
   Use this command whenever you update or modify the models, so the changes can be applied to the database schema.
   Create migration files in the default migration folder, which is typically located at migrations/models/.


- **Apply all migration files to update the database schema**:

   ```
   aerich upgrade
   ```
   This command applies all pending migrations to the database.


- **Check migration history**:

   ```
   aerich history
   ```
   Displays a list of all migrations that have been generated.


- **Rollback a migration**:

   ```
   aerich downgrade
   ```
   Reverts the last migration applied to the database.


### **Migration of Inserts**  

Aerich only generates schema changes. For data insertion, a script was created to initialize the database using Tortoise and execute the inserts through the corresponding function.  

#### **First-Time Setup**  
You must have these files in `./data/` path:

- `departamentos.geojson`
- `jurisdicciones-ambientales.geojson`
- `subzonas-hidrograficas.geojson`
- `paramos.geojson`

When starting the migration for the first time, you must run the following command to populate the database:  

```sh
python -m database.post_migrate
```

#### **What Does This Command Do?**  
This command runs the `post_migrate` script, which:  

- Initializes the database connection using Tortoise.  
- Ensures that the necessary tables exist.  
- Executes the data insertion function while verifying that records do not already exist. If they do, they are not modified.  

By following this process, you ensure that the initial dataset is correctly inserted without duplicating entries.

## Code checks

This guide explains how to use `black` for code formatting and `pyright` for type checking.

### Installation
If `black` or `pyright` is not installed, you can add them using `pip`:

```
pip install black pyright
```

Alternatively, for `pyright`, you can install it globally with `npm`:

```
npm install -g pyright
```

### Verifying Code Style with `black`

To check if the code conforms to `black`'s style guide without making changes:

```
black --check .
```

### Explanation:
- `--check`: Ensures `black` only verifies the style and does not modify files.
- `.`: Specifies the current directory as the target. Replace `.` with the specific path if needed.

If the code passes the check, you will see:
```
All done!
N files would be left unchanged.
```
If there are style issues, `black` will list the files and lines that need formatting.

## Correcting Code Style with `black`

To automatically reformat the code to conform to `black`'s style guide:

```
black .
```

### Explanation:
- Running `black` without `--check` will directly modify the files in place to match the style guide.

After running, you will see:

```
All done!
N files reformatted, M files left unchanged.
```

## Type Checking with `pyright`

To check your code for type errors using `pyright`:

```
pyright
```

### Explanation:
- `pyright` automatically scans your code for type issues.

To focus on a specific file or directory:
```
pyright path/to/file_or_directory
```

### Running GitHub Actions Locally
To run GitHub Actions workflows locally, you can use the `act` tool. This allows you to test your workflows without pushing changes to GitHub.

### Installation

##### Windows

###### Option 1: Using Scoop
If you prefer using Scoop on Windows:
1. Open **PowerShell**.
2. Install Scoop by running:
   ```
   iwr -useb get.scoop.sh | iex
   ```
3. Close and reopen your terminal.
4. Verify Scoop installation:
   ```
   scoop --version
   ```
5. Install `act`:
   ```
   scoop install act
   ```
6. Verify installation:
   ```
   act --version
   ```   

##### Linux and macOS

###### Using Homebrew (macOS and Linux)
1. Install Homebrew if not already installed. See the [Homebrew installation guide](https://brew.sh/).
2. Install `act`:
   ```
   brew install act
   ```
3. Verify installation:
   ```
   act --version
   ```
4. Verify installation:
   ```
   act --version
   ```   

#### Running Workflows
1. Navigate to your repository's root directory where the `.github/workflows` folder is located.
2. Run `act` to execute the default workflow in terminal:
   ```
   act
   ```
   When running GitHub Actions workflows locally with `act`, you will be given the option to choose from several images. It is recommended to use the **Medium** image for most cases.

###### Image Options:
- **Large Image (Large)**:
  - **Size**: 17GB download, 53.1GB storage.
  - **Recommendation**: Only if additional tools are needed, as it is heavier.

- **Medium Image (Medium)** *(Recommended)*:
  - **Size**: 500MB.
  - **Description**: Contains the basic tools needed for most actions.
  - **Recommendation**: Ideal for most workflows.

- **Micro Image (Micro)**:
  - **Size**: Less than 200MB.
  - **Description**: Contains only NodeJS and does not work with all actions.
  - **Recommendation**: Only for very lightweight workflows.
  
3. To specify a specific event, use:
   ```
   act <event>
   ```
   Replace `<event>` with events like `push`, `pull_request`, etc.

#### Example
To simulate a `push` event:
```
act push
```

## Deploy

[WIP]

## Authors

Línea de Desarrollo - Gerencia de Información Científica - Dirección de conocimiento - Instituto de Investigación de
Recursos Biológicos Alexander von Humboldt - Colombia

See also the list of [contributors](https://github.com/PEM-Humboldt/biotablero-search-backend/graphs/contributors) who
participated in this project.

## License

This project is licensed under the MIT [License](LICENSE).

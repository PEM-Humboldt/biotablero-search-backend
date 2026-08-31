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
1. Create a `.env` file based on [env.sample](./env.sample) and update the values of the existing variables.
1. Run Docker Compose to start project containers:

   ```sh
   docker compose -f docker-compose-dev.yml up
   ```

1. Run database migrations:
   ```
   aerich upgrade
   ```
1. Populate the database with initial data:
    
   Follow the steps in the [Populate database](#populate-database) section to insert required data.
   
 
7. Run the the development server

   `uvicorn app.main:app --reload`

## Populate database

Aerich only generates schema changes. For data insertion, a script was created to populate the database.

### Prerrequisites
You must have these files in `./data/` path:

- `colombia.geojson`
- `departamentos.geojson`
- `jurisdicciones-ambientales.geojson`
- `subzonas-hidrograficas.geojson`
- `paramos.geojson`
- `dpc.csv`
- `protconn.csv`
- `statsOnSpecies.csv`
- `metric_info.csv`

### Run script

To populate the whole database run (the script deletes all the previous data in the database):

```sh
python -m database.populate_db
```

The script accepts the param `-s` or `--sets` to populate onle some set of data, these are the possible values:
- `all` (default): all tables
- `areas`: area types and polygons
- `indicators`: tables associated with precualculated indicators
- `metrics`: tables associated with metrics, collections and metric relations

At the end of this file there are some additional commands for database migrations

## Documentation

The documentation is automatically generated at `/docs` and `/redoc`. For production `/docs` is disabled

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

#### Explanation:
- `--check`: Ensures `black` only verifies the style and does not modify files.
- `.`: Specifies the current directory as the target. Replace `.` with the specific path if needed.

If the code passes the check, you will see:
```
All done!
N files would be left unchanged.
```
If there are style issues, `black` will list the files and lines that need formatting.

### Correcting Code Style with `black`

To automatically reformat the code to conform to `black`'s style guide:

```
black .
```

#### Explanation:
- Running `black` without `--check` will directly modify the files in place to match the style guide.

After running, you will see:

```
All done!
N files reformatted, M files left unchanged.
```

### Type Checking with `pyright`

To check your code for type errors using `pyright`:

```
pyright
```

#### Explanation:
- `pyright` automatically scans your code for type issues.

To focus on a specific file or directory:
```
pyright path/to/file_or_directory
```

## Running GitHub Actions Locally
To run GitHub Actions workflows locally, you can use the `act` tool. This allows you to test your workflows without pushing changes to GitHub.

### Installation

##### Windows

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

### Running Workflows
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

## Utils

### Database Migrations

This project uses `aerich` for database migrations. Below are the necessary commands, explanations, and how to use the dedicated endpoint for migrations.

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

## Docker

### Build image

```sh
# Build image
docker build -t biotablero-search-backend:latest .
# Run temporal container
docker run -it --rm --env-file .env --name bt-search-backend -p 8000:8000 --network=biotablero-search-backend_bt-search-network biotablero-search-backend:latest
```


## Authors

Línea de Desarrollo - Gerencia de Información Científica - Dirección de conocimiento - Instituto de Investigación de
Recursos Biológicos Alexander von Humboldt - Colombia

See also the list of [contributors](https://github.com/PEM-Humboldt/biotablero-search-backend/graphs/contributors) who
participated in this project.

## License

This project is licensed under the MIT [License](LICENSE).

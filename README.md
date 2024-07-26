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
   ```
1. Run the the development server

   `uvicorn app.main:app --reload`

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

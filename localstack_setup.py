#!/usr/bin/env python3
import boto3
import logging
import time
from botocore.exceptions import ClientError
from typing import Dict, Any

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class LocalStackSetup:
    def __init__(self):
        self.endpoint_url = "http://localhost:4566"
        self.aws_config = {
            'aws_access_key_id': 'test',
            'aws_secret_access_key': 'test',
            'region_name': 'us-east-1'
        }

        # Inicializar clientes
        self.s3 = self._create_client('s3')
        self.lambda_client = self._create_client('lambda')
        self.apigateway = self._create_client('apigateway')

    def _create_client(self, service_name: str) -> Any:
        """Crear un cliente de AWS para un servicio específico."""
        return boto3.client(
            service_name,
            endpoint_url=self.endpoint_url,
            **self.aws_config
        )

    def wait_for_localstack(self, max_retries: int = 30, delay: int = 1) -> None:
        """Esperar hasta que LocalStack esté listo."""
        for i in range(max_retries):
            try:
                self.s3.list_buckets()
                logger.info("LocalStack está listo")
                return
            except Exception:
                if i < max_retries - 1:
                    time.sleep(delay)
                else:
                    raise Exception("LocalStack no está disponible después de los intentos máximos")

    def setup_s3(self) -> None:
        """Configurar buckets S3."""
        buckets = ['my-test-bucket']
        for bucket in buckets:
            try:
                self.s3.create_bucket(Bucket=bucket)
                logger.info(f"Bucket creado: {bucket}")
            except ClientError as e:
                if e.response['Error']['Code'] == 'BucketAlreadyExists':
                    logger.warning(f"El bucket ya existe: {bucket}")
                else:
                    raise

    def setup_lambda(self) -> None:
        """Configurar funciones Lambda."""
        try:
            with open('app/main.py', 'rb') as f:
                self.lambda_client.create_function(
                    FunctionName='fastapi-lambda',
                    Runtime='python3.12',
                    Role='arn:aws:iam::000000000000:role/lambda-role',
                    Handler='main.handler',
                    Code={'ZipFile': f.read()},
                    Environment={
                        'Variables': {
                            'STAGE': 'dev',
                            'POSTGRES_HOST': 'postgres',
                            'POSTGRES_PORT': '5432',
                            'POSTGRES_USER': 'postgres',
                            'POSTGRES_PASSWORD': 'postgres',
                            'POSTGRES_DB': 'localdb'
                        }
                    }
                )
            logger.info("Función Lambda creada: fastapi-lambda")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceConflictException':
                logger.warning("La función Lambda ya existe")
            else:
                raise

    def setup_api_gateway(self) -> None:
        """Configurar API Gateway."""
        try:
            api = self.apigateway.create_rest_api(
                name='FastAPI-Local',
                description='Local API Gateway for FastAPI'
            )

            # Obtener el ID de la raíz del recurso
            resources = self.apigateway.get_resources(restApiId=api['id'])
            root_id = resources['items'][0]['id']

            # Crear un recurso proxy
            resource = self.apigateway.create_resource(
                restApiId=api['id'],
                parentId=root_id,
                pathPart='{proxy+}'
            )

            # Configurar el método ANY
            self.apigateway.put_method(
                restApiId=api['id'],
                resourceId=resource['id'],
                httpMethod='ANY',
                authorizationType='NONE'
            )

            logger.info(f"API Gateway creado: {api['name']} (ID: {api['id']})")
        except ClientError as e:
            if e.response['Error']['Code'] == 'ConflictException':
                logger.warning("El API Gateway ya existe")
            else:
                raise

    def setup_all(self) -> None:
        """Configurar todos los servicios."""
        try:
            logger.info("Iniciando configuración de LocalStack...")
            self.wait_for_localstack()
            self.setup_s3()
            self.setup_lambda()
            self.setup_api_gateway()
            logger.info("Configuración de LocalStack completada exitosamente")
        except Exception as e:
            logger.error(f"Error durante la configuración: {str(e)}")
            raise


if __name__ == "__main__":
    setup = LocalStackSetup()
    setup.setup_all()
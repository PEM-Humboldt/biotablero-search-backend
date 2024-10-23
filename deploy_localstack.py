import os
import boto3
import json
import time
from botocore.exceptions import ClientError


class LocalStackDeployer:
    def __init__(self):
        self.endpoint_url = "http://localhost:4566"
        self.aws_config = {
            'aws_access_key_id': 'test',
            'aws_secret_access_key': 'test',
            'region_name': 'us-east-1'
        }

        self.lambda_client = boto3.client('lambda', endpoint_url=self.endpoint_url, **self.aws_config)
        self.apigateway = boto3.client('apigateway', endpoint_url=self.endpoint_url, **self.aws_config)
        self.s3 = boto3.client('s3', endpoint_url=self.endpoint_url, **self.aws_config)

    def upload_lambda_to_s3(self):
        bucket_name = 'lambda-packages'
        key_name = 'lambda_package.zip'
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
                print(f"Error creating bucket: {str(e)}")
                raise

        try:
            with open('lambda_package.zip', 'rb') as f:
                self.s3.upload_fileobj(f, bucket_name, key_name)
            print(f"Uploaded Lambda package to S3: {bucket_name}/{key_name}")
            return bucket_name, key_name
        except Exception as e:
            print(f"Error uploading Lambda package to S3: {str(e)}")
            raise

    def upload_layer_to_s3(self, layer_zip):
        bucket_name = 'lambda-layers'
        layer_key = os.path.basename(layer_zip)
        try:
            self.s3.create_bucket(Bucket=bucket_name)
        except ClientError as e:
            if e.response['Error']['Code'] != 'BucketAlreadyOwnedByYou':
                print(f"Error creating bucket: {str(e)}")
                raise

        try:
            with open(layer_zip, 'rb') as f:
                self.s3.upload_fileobj(f, bucket_name, layer_key)
            print(f"Uploaded Lambda Layer to S3: {bucket_name}/{layer_key}")
            return bucket_name, layer_key
        except Exception as e:
            print(f"Error uploading Lambda layer to S3: {str(e)}")
            raise

    def create_lambda_layer(self, layer_name):
        try:
            bucket_name, layer_key = self.upload_layer_to_s3(f"{layer_name}.zip")
            response = self.lambda_client.publish_layer_version(
                LayerName=layer_name,
                Content={
                    'S3Bucket': bucket_name,
                    'S3Key': layer_key,
                },
                CompatibleRuntimes=['python3.9'],
                Description=f"Layer with {layer_name} dependencies"
            )
            layer_arn = response['LayerVersionArn']
            print(f"Lambda Layer created: {layer_arn}")
            return layer_arn
        except Exception as e:
            print(f"Error creating Lambda Layer: {str(e)}")
            raise

    def create_lambda_function(self):
        try:
            bucket_name, key_name = self.upload_lambda_to_s3()

            # Subir y publicar las capas
            light_layer_arn = self.create_lambda_layer('lambda_layer_light')
            heavy_layer_1_arn = self.create_lambda_layer('lambda_layer_heavy_part1')
            heavy_layer_2_arn = self.create_lambda_layer('lambda_layer_heavy_part2')
            heavy_layer_3_arn = self.create_lambda_layer('lambda_layer_heavy_part3')
            heavy_layer_4_arn = self.create_lambda_layer('lambda_layer_heavy_part4')

            try:
                self.lambda_client.update_function_code(
                    FunctionName='biotablero-search-api',
                    S3Bucket=bucket_name,
                    S3Key=key_name
                )
                print("Lambda function updated")
            except ClientError as e:
                if e.response['Error']['Code'] == 'ResourceNotFoundException':
                    self.lambda_client.create_function(
                        FunctionName='biotablero-search-api',
                        Runtime='python3.9',
                        Role='arn:aws:iam::000000000000:role/lambda-role',  # Role ficticio para LocalStack
                        Handler='app.main.handler',
                        Code={'S3Bucket': bucket_name, 'S3Key': key_name},
                        Timeout=30,
                        MemorySize=256,
                        Environment={
                            'Variables': {
                                'STAGE': 'dev',
                                'POSTGRES_HOST': 'postgres',
                                'POSTGRES_PORT': '5432',
                                'POSTGRES_USER': 'postgres',
                                'POSTGRES_PASSWORD': 'postgres',
                                'POSTGRES_DB': 'localdb'
                            }
                        },
                        Layers=[light_layer_arn, heavy_layer_1_arn, heavy_layer_2_arn, heavy_layer_3_arn, heavy_layer_4_arn]
                    )
                    print("Lambda function created with Layers")
                else:
                    raise e
        except Exception as e:
            print(f"Error with Lambda function: {str(e)}")
            raise

    def create_api(self):
        """Crear API Gateway"""
        try:
            # Crear API
            api = self.apigateway.create_rest_api(
                name='biotablero-search-api',
                description='BioTablero Search API'
            )
            api_id = api['id']

            # Obtener el ID del recurso raíz
            resources = self.apigateway.get_resources(restApiId=api_id)
            root_id = resources['items'][0]['id']

            # Crear recurso proxy
            proxy_resource = self.apigateway.create_resource(
                restApiId=api_id,
                parentId=root_id,
                pathPart='{proxy+}'
            )

            # Configurar método ANY
            self.apigateway.put_method(
                restApiId=api_id,
                resourceId=proxy_resource['id'],
                httpMethod='ANY',
                authorizationType='NONE'
            )

            # Integrar con Lambda
            lambda_arn = f'arn:aws:lambda:us-east-1:000000000000:function:biotablero-search-api'
            self.apigateway.put_integration(
                restApiId=api_id,
                resourceId=proxy_resource['id'],
                httpMethod='ANY',
                type='AWS_PROXY',
                integrationHttpMethod='POST',
                uri=f'arn:aws:apigateway:us-east-1:lambda:path/2015-03-31/functions/{lambda_arn}/invocations'
            )

            # Desplegar API
            self.apigateway.create_deployment(
                restApiId=api_id,
                stageName='dev'
            )

            print(f"API Gateway created and deployed: http://localhost:4566/restapis/{api_id}/dev/_user_request_/")
            return api_id

        except Exception as e:
            print(f"Error creating API Gateway: {str(e)}")
            raise

    def deploy_all(self):
        print("Starting deployment...")
        self.create_lambda_function()
        api_id = self.create_api()
        print(f"API available at: http://localhost:4566/restapis/{api_id}/dev/_user_request_/")
        print("You can test the API with:")
        print(f"curl -X GET http://localhost:4566/restapis/{api_id}/dev/_user_request_/")

if __name__ == "__main__":
    deployer = LocalStackDeployer()
    deployer.deploy_all()

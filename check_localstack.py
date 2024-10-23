#!/usr/bin/env python3
import boto3

import json
from botocore.config import Config
from datetime import datetime


class LocalStackChecker:
    def __init__(self):
        self.endpoint_url = "http://localhost:4566"
        self.aws_config = {
            'aws_access_key_id': 'test',
            'aws_secret_access_key': 'test',
            'region_name': 'us-east-1'
        }

    def _create_client(self, service_name):
        return boto3.client(
            service_name,
            endpoint_url=self.endpoint_url,
            **self.aws_config,
            config=Config(connect_timeout=5, read_timeout=5)
        )

    def check_s3(self):
        print("\n=== Checking S3 ===")
        try:
            s3 = self._create_client('s3')
            buckets = s3.list_buckets()['Buckets']
            print(f"Found {len(buckets)} buckets:")
            for bucket in buckets:
                print(f"- {bucket['Name']} (Created: {bucket['CreationDate']})")
                try:
                    objects = s3.list_objects_v2(Bucket=bucket['Name'])
                    if 'Contents' in objects:
                        print(f"  Contents: {len(objects['Contents'])} objects")
                except Exception as e:
                    print(f"  Error listing contents: {str(e)}")
        except Exception as e:
            print(f"Error checking S3: {str(e)}")

    def check_lambda(self):
        print("\n=== Checking Lambda ===")
        try:
            lambda_client = self._create_client('lambda')
            functions = lambda_client.list_functions()['Functions']
            print(f"Found {len(functions)} Lambda functions:")
            for func in functions:
                print(f"- {func['FunctionName']}")
                print(f"  Runtime: {func['Runtime']}")
                print(f"  Handler: {func['Handler']}")
                print(f"  Last Modified: {func['LastModified']}")
                print(f"  Memory: {func['MemorySize']}MB")
                print(f"  Timeout: {func['Timeout']}s")
        except Exception as e:
            print(f"Error checking Lambda: {str(e)}")

    def check_apigateway(self):
        print("\n=== Checking API Gateway ===")
        try:
            apigateway = self._create_client('apigateway')
            apis = apigateway.get_rest_apis()['items']
            print(f"Found {len(apis)} APIs:")
            for api in apis:
                print(f"- {api['name']} (ID: {api['id']})")
                try:
                    resources = apigateway.get_resources(restApiId=api['id'])['items']
                    print(f"  Resources: {len(resources)}")
                    for resource in resources:
                        print(f"  - Path: {resource.get('path', '/')}")
                        if 'resourceMethods' in resource:
                            print(f"    Methods: {', '.join(resource['resourceMethods'].keys())}")
                except Exception as e:
                    print(f"  Error listing resources: {str(e)}")
        except Exception as e:
            print(f"Error checking API Gateway: {str(e)}")

    def check_all(self):
        print(f"LocalStack Service Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 50)
        self.check_s3()
        self.check_lambda()
        self.check_apigateway()


if __name__ == "__main__":
    checker = LocalStackChecker()
    checker.check_all()

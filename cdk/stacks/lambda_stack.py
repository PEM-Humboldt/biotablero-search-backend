from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_rds as rds,
    aws_logs as logs,
    aws_ec2 as ec2, SecretValue,
    RemovalPolicy
)
from constructs import Construct
import os

class LambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Detect if it is LocalStack or AWS
        is_localstack = os.getenv("LOCALSTACK") is not None
        if is_localstack:
            localstack_endpoint = "http://localhost:4566"
        else:
            localstack_endpoint = None

        # Create VPC for RDS
        vpc = ec2.Vpc(self, "VPC", max_azs=2)

        # Create Lambda pointing to LocalStack or AWS
        api_lambda = lambda_.Function(
            self, "BioTableroSearchLambda",
            runtime=lambda_.Runtime.PYTHON_3_12,
            handler="app.main.handler",
            code=lambda_.Code.from_asset("app"),
            environment={
                "AWS_LAMBDA_ENDPOINT": localstack_endpoint or "AWS_DEFAULT",
                "STAGE": "dev",
                "POSTGRES_HOST": "postgres",
                "POSTGRES_PORT": "5432",
                "POSTGRES_USER": "postgres",
                "POSTGRES_PASSWORD": "postgres",
                "POSTGRES_DB": "localdb"
            }
        )

        # Create API Gateway for Lambda on LocalStack or AWS
        api = apigateway.LambdaRestApi(
            self, "APIGateway",
            handler=api_lambda,
            endpoint_types=[apigateway.EndpointType.REGIONAL]
        )

        # Create an S3 bucket on LocalStack or AWS
        bucket = s3.Bucket(
            self,
            "BiotableroS3Bucket",
            bucket_name="biotablero-local" if is_localstack else None,
            removal_policy=RemovalPolicy.DESTROY,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # RDS PostgreSQL instance on LocalStack or AWS
        db_instance = rds.DatabaseInstance(
            self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.postgres(
                version=rds.PostgresEngineVersion.VER_12_3),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO),
            vpc=vpc,
            allocated_storage=20,
            storage_type=rds.StorageType.GP2,
            multi_az=False,
            deletion_protection=False,
            publicly_accessible=True,
            port=5433 if is_localstack else 5432,
            credentials=rds.Credentials.from_password(
                "postgres", SecretValue.unsafe_plain_text("2a2f56b0")),
            vpc_subnets={
                "subnet_type": ec2.SubnetType.PUBLIC
            }
        )

        # Create logs of CloudWatch
        log_group = logs.LogGroup(
            self, "LogGroup",
            retention=logs.RetentionDays.ONE_WEEK
        )

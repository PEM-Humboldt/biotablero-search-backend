from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_apigateway as apigateway,
    aws_s3 as s3,
    aws_rds as rds,
    aws_logs as logs,
    aws_ec2 as ec2,
)
from constructs import Construct

class LambdaStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create VPC for RDS
        vpc = ec2.Vpc(self, "VPC")

        # Lambda for FastAPI
        api_lambda = lambda_.Function(
            self, "BioTableroSearchLambda",
            runtime=lambda_.Runtime.PYTHON_3_9,
            handler="app.main.handler",
            code=lambda_.Code.from_asset("app")
        )

        # API Gateway to expose Lambda
        api = apigateway.LambdaRestApi(
            self, "APIGateway",
            handler=api_lambda
        )

        # Create an S3 bucket
        bucket = s3.Bucket(self, "BiotableroS3Bucket")

        # RDS PostgreSQL
        db_instance = rds.DatabaseInstance(
            self, "RDSInstance",
            engine=rds.DatabaseInstanceEngine.postgres(version=rds.PostgresEngineVersion.VER_12_3),
            instance_type=ec2.InstanceType.of(
                ec2.InstanceClass.BURSTABLE2, ec2.InstanceSize.MICRO
            ),
            vpc=vpc,
            allocated_storage=20,
            storage_type=rds.StorageType.GP2,
            multi_az=False,
            cloudwatch_logs_exports=["postgresql"],
            deletion_protection=False,
            publicly_accessible=True,
        )

        # CloudWatch para logs
        log_group = logs.LogGroup(
            self, "LogGroup",
            retention=logs.RetentionDays.ONE_WEEK
        )

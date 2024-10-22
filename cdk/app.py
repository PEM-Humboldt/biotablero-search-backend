from aws_cdk import App, Environment
from stacks.lambda_stack import LambdaStack
import os

app = App()

# Detect environment (LocalStack vs AWS)
if os.getenv("LOCALSTACK"):
    env_local = Environment(account="000000000000", region="us-east-1")
    LambdaStack(app, "LambdaStackLocal", env=env_local)
else:
    # Set AWS credentials or use default AWS environment
    env_aws = Environment(account=os.getenv("CDK_DEFAULT_ACCOUNT"), region=os.getenv("CDK_DEFAULT_REGION"))
    LambdaStack(app, "LambdaStackAWS", env=env_aws)

app.synth()
from aws_cdk import App, Environment
from stacks.lambda_stack import LambdaStack

app = App()

env_local = Environment(account="000000000000", region="us-east-1")
env_prod = Environment(account="your-aws-account-id", region="us-east-1")

# Stack for LocalStack
LambdaStack(app, "LambdaStackLocal", env=env_local)

# Stack for production
LambdaStack(app, "LambdaStackProd", env=env_prod)

app.synth()
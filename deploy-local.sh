#!/bin/bash

# Function to install jq on different operating systems
install_jq() {
    if [[ "$(uname)" == "Darwin" ]]; then
        # For MacOS
        if ! command -v brew &> /dev/null; then
            echo "Homebrew is not installed. Installing Homebrew..."
            /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        fi
        echo "Installing jq with Homebrew..."
        brew install jq
    elif [[ "$(uname)" == "Linux" ]]; then
        # For Linux
        echo "Installing jq on Linux with apt-get..."
        sudo apt-get update && sudo apt-get install -y jq
    elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$(uname)" == "MINGW64_NT"* ]]; then
        # For Windows (Mingw)
        echo "Downloading jq for Windows..."
        curl -k -Lo jq.exe https://github.com/stedolan/jq/releases/download/jq-1.6/jq-win64.exe
        if [ -f "jq.exe" ]; then
            mv jq.exe /usr/bin/jq
            echo "jq installed correctly."
        else
            echo "Error: Could not download jq."
            exit 1
        fi
    else
        echo "Operating system not supported. Please install jq manually."
        exit 1
    fi
}

# Check if jq is installed
if ! command -v jq &> /dev/null; then
    echo "jq is not installed. Installing jq..."
    install_jq
else
    echo "jq is already installed."
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker is not installed. Please install Docker first."
    exit 1
fi

# Safely load environment variables from .env.development
if [ -f .env.development ]; then
    export $(grep -v '^#' .env.development | xargs)
else
    echo ".env.development not found."
    exit 1
fi

# Start LocalStack and PostgreSQL using Docker Compose
docker-compose up -d localstack postgres

# Check if Docker services started correctly
if [ $? -ne 0 ]; then
    echo "Error starting Docker services."
    exit 1
fi

# Check that LocalStack is running before continuing
echo "Waiting for LocalStack to be listed..."
TIMEOUT=60  # Timeout limit in seconds
WAIT_INTERVAL=5  # Interval between checks

while ! curl -s http://localhost:4566/_localstack/health | jq -e '.services.s3 == "running"' > /dev/null; do
  if [ $TIMEOUT -le 0 ]; then
    echo "Timeout waiting for LocalStack services to be operational."
    exit 1
  fi
  echo "Waiting for LocalStack services to be operational..."
  sleep $WAIT_INTERVAL
  TIMEOUT=$((TIMEOUT - WAIT_INTERVAL))
done

echo "LocalStack services are running."

# Check if AWS CDK is installed
if ! command -v cdk &> /dev/null; then
    echo "AWS CDK is not installed. Installing AWS CDK..."
    npm install -g aws-cdk
fi

# Detect whether running on Windows or Linux/macOS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$(uname)" == "MINGW64_NT"* ]]; then
    PYTHON_CMD="python"
else
    PYTHON_CMD="python3"
fi

# Configuring and deploying AWS CDK infrastructure on LocalStack
cdk synth --no-bootstrap --app "$PYTHON_CMD cdk/app.py"
if [ $? -ne 0 ]; then
    echo "CDK synthesis failed."
    exit 1
fi

cdk deploy --no-bootstrap --require-approval never --outputs-file ./cdk-outputs-local.json
if [ $? -ne 0 ]; then
    echo "CDK deployment failed."
    exit 1
fi

echo "Deployment completed in LocalStack."

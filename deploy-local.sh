#!/bin/bash

# Cargar variables de entorno desde .env.development
export $(grep -v '^#' .env.development | xargs)

# Iniciar LocalStack usando Docker Compose
docker-compose up -d localstack postgres

# Verificar que LocalStack esté listo antes de continuar
echo "Esperando a que LocalStack esté listo..."
while ! curl -s http://localhost:4566/health | grep "\"services\": \{\"s3\": \"running\""; do
  echo "Esperando que los servicios de LocalStack estén operativos..."
  sleep 5
done

# Instalar las dependencias de AWS CDK si es necesario
npm install -g aws-cdk

# Configurar y desplegar la infraestructura de AWS CDK en LocalStack
cdk bootstrap aws://000000000000/us-east-1 --app "cdk.out"
cdk deploy --require-approval never --outputs-file ./cdk-outputs-local.json

echo "Despliegue completado en LocalStack."

# Iniciar los servicios locales de LocalStack y PostgreSQL
start-local:
	docker-compose up -d localstack postgres
	@echo "Iniciando LocalStack y PostgreSQL..."

# Detener los servicios locales de LocalStack y PostgreSQL
stop-local:
	docker-compose down
	@echo "Deteniendo y eliminando LocalStack y PostgreSQL..."

# Desplegar la infraestructura en LocalStack
deploy-local:
	./deploy-local.sh
	@echo "Desplegando la infraestructura en LocalStack..."

# Desplegar la infraestructura en AWS producción
deploy-prod:
	npm install -g aws-cdk
	cdk bootstrap aws://your-aws-account-id/us-east-1
	cdk deploy --require-approval never --outputs-file ./cdk-outputs-prod.json
	@echo "Desplegando la infraestructura en AWS producción..."

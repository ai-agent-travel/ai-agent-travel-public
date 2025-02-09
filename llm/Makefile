REGION := asia-northeast1
ARTIFACT_REPOSITORY := $(REGION)-docker.pkg.dev
PROJECT_ID := $(shell gcloud config get-value project)
REPOSITORY_NAME := ai-agent-travel-llm-repository
SHORT_SHA := $(shell git rev-parse --short HEAD)
IMAGE_NAME := llm-run-service
DOCKERFILE := docker/Dockerfile.prod
FIRESTORE_DATABASE_NAME := ai-agent-travel-llm-firestore
CLOUD_RUN_SA_EMAIL := ai-agent-travel-llm-sa@$(PROJECT_ID).iam.gserviceaccount.com


.PHONY: login
login:
	gcloud auth login --update-adc

.PHONY: terraform_modules
terraform_modules:
	cd terraform_modules
	terraform init
	terraform plan
	terraform apply

.PHONY: terraform
terraform:
	terraform import google_firestore_database.default projects/$(PROJECT_ID)/databases/$(FIRESTORE_DATABASE_NAME)
	terraform import google_service_account.cloud_run_sa projects/$(PROJECT_ID)/serviceAccounts/$(CLOUD_RUN_SA_EMAIL)
	terraform init
	terraform plan
	terraform apply

.PHONY: build
build:
	gcloud auth configure-docker $(ARTIFACT_REPOSITORY)
	docker buildx build --platform=linux/amd64 --load -t $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):$(SHORT_SHA) -f $(DOCKERFILE) .
	docker tag $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):$(SHORT_SHA) $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):latest

.PHONY: push
push:
	gcloud auth configure-docker $(ARTIFACT_REPOSITORY)
	docker push $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):$(SHORT_SHA)
	docker push $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):latest

.PHONY: deploy
deploy:
	gcloud run deploy llm-run-service --image $(ARTIFACT_REPOSITORY)/$(PROJECT_ID)/$(REPOSITORY_NAME)/$(IMAGE_NAME):$(SHORT_SHA) --region $(REGION) --platform managed --allow-unauthenticated
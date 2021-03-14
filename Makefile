
.PHONY: help test build run clean update

# Leverge on comment prefix with '##' next to make command as their help text
help: ## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

test: ## Run unit tests in container
	# build arg (NOCACHE) is always set to a random value to
	# invalidate docker cache to ensure test are rerun
	docker-compose -f docker-compose.test.yaml build --build-arg NOCACHE=$$(/bin/bash -c 'echo $$RANDOM')

build: ## Build the container
	docker-compose build

run: ## Run the app locally
	docker-compose up -d

clean: ## Revert back to clean state
	docker-compose down

update: ## Update requirements.txt based on imports in src directory
	~/.local/bin/pipreqs --force --savepath requirements.txt src/app

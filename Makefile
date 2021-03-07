
.PHONY: help

# Leverge on comment prefix with '##' next to make command as their help text
help: ## Help command
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)

.DEFAULT_GOAL := help

build: ## Build the container
	docker-compose build

run: ## run the app locally
	docker-compose up -d

clean: ## Revert back to clean state

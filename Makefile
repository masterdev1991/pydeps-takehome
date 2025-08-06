.PHONY: lint check test build-base build

lint:
	ruff check apps/ lib/ scripts/ tests/
	ruff format --check apps/ lib/ scripts/ tests/

check:
	mypy apps/ lib/ scripts/ tests/

test:
	python -m pytest tests

build-base:
	docker build . -f Dockerfile -t python-base

build:
	@if [ "$(word 2,$(MAKECMDGOALS))" = "base" ]; then \
		echo "Building base image..."; \
		docker build . -f Dockerfile -t python-base; \
	elif [ "$(word 2,$(MAKECMDGOALS))" = "all" ]; then \
		echo "Building all images..."; \
		docker build . -f Dockerfile -t python-base && \
		for app in server-one server-two job-a job-b job-c; do \
			echo "Building $$app..."; \
			docker build apps/$$app/ -t $$app; \
		done; \
	else \
		APP=$(word 2,$(MAKECMDGOALS)); \
		if [ -d "apps/$$APP" ]; then \
			echo "Building $$APP..."; \
			docker build apps/$$APP/ -t $$APP; \
		else \
			echo "App $$APP not found in apps/ directory"; \
			exit 1; \
		fi; \
	fi

# Prevent make from treating build arguments as targets
%:
	@:
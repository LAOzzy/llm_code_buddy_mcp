SHELL := /bin/bash

.PHONY: help dev test fmt lint check

DEV_SCRIPT := ./scripts/dev
TEST_SCRIPT := ./scripts/test
FMT_SCRIPT  := ./scripts/fmt
LINT_SCRIPT := ./scripts/lint

help:
	@echo "Available targets:"
	@echo "  make dev   - Start local dev workflow"
	@echo "  make test  - Run tests"
	@echo "  make fmt   - Format code"
	@echo "  make lint  - Lint code"
	@echo "  make check - Format+lint+test"

dev:
	@$(DEV_SCRIPT)

test:
	@$(TEST_SCRIPT)

fmt:
	@$(FMT_SCRIPT)

lint:
	@$(LINT_SCRIPT)

check: fmt lint test


# Define the Python interpreter
PYTHON := python3

# Define the main application file
MAIN_APP := main.py

# Define environment variables
export MODE := development

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make run    - Get historical data for the given interval"
	@echo "  make help   - Show this help message"

# Run the Streamlit application
run:
	$(PYTHON) $(MAIN_APP)

migrate:
	$(PYTHON) migrate.py

.PHONY: help run

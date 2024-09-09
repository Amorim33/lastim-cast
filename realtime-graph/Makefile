# Define the Python interpreter
PYTHON := python3

# Define the Streamlit command
STREAMLIT := streamlit

# Define the main application file
MAIN_APP := main.py

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make run    - Run the Streamlit application"
	@echo "  make help   - Show this help message"

# Run the Streamlit application
run:
	$(STREAMLIT) run $(MAIN_APP)

.PHONY: help run

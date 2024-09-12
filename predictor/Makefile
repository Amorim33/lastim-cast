# Define the Python interpreter
PYTHON := python3

# Define environment variables
export MODE := development

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "  make retrain    - Retrain model for the given interval"
	@echo "  make help   - Show this help message"

# Train the LSTM model for the first time
train:
	$(PYTHON) train.py

# Predict all next datapoints
predict:
	$(PYTHON) predict.py

.PHONY: help run

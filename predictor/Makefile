# Define the Python interpreter
PYTHON := python3

# Define environment variables
export MODE := development

# Default target
.DEFAULT_GOAL := help

# Help target
help:
	@echo "Available commands:"
	@echo "make train - Perform the initial training with 90% of the available data"
	@echo "make predict - Predict all "next" datapoints and retrain the model with the new available data"
	@echo "make help - Show this help message"

# Train the LSTM model for the first time
train:
	$(PYTHON) train.py

# Predict all next datapoints
predict:
	$(PYTHON) predict.py

.PHONY: help run

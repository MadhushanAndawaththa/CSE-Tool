# Use official Python runtime as a parent image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies from pyproject.toml
# We use pip to install the package in editable mode to get dependencies
COPY pyproject.toml .
# Create a dummy README to satisfy build backend if needed, though usually not for pip install -e .
RUN touch README.md
# Or just install dependencies directly if requirements.txt exists
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project code
COPY . .

# Run the CLI application by default
CMD ["python", "main.py"]

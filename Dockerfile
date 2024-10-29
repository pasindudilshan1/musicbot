FROM python:3.8  # Use a compatible Python version

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install virtualenv
RUN pip install virtualenv

# Create a virtual environment
RUN virtualenv venv

# Activate the virtual environment and install dependencies
RUN . venv/bin/activate && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application
COPY . .

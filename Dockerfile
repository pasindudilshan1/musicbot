# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Expose the port your application runs on (adjust as needed, e.g., 8000)
EXPOSE 8000

# Specify the command to run the application
# Replace 'bot.py' with the main entry file of your application
CMD ["python", "bot.py"]

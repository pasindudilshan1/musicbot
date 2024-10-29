# Start from a base image
FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .
RUN pip install --upgrade pip

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the bot code to the working directory
COPY . .

# Expose a port (if needed, only for web server or Flask use)
# EXPOSE 5000

# Start the bot
CMD ["python", "bot.py"]

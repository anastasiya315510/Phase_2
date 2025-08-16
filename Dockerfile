# Use lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY app.py task.py /app/

# Expose Flask port
EXPOSE 8000

# Default command: start Flask app
CMD ["python", "app.py"]

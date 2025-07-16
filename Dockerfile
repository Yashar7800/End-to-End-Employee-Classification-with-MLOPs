# Use a modern, lightweight Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Gunicorn separately (ensures it's installed even if requirements.txt fails)
RUN pip install gunicorn==20.1.0

# Copy the rest of the project
COPY . .

# Expose port (5000 for ECS/EC2, change to 8080 for SageMaker)
EXPOSE 5000

# Set Flask environment variables
ENV FLASK_APP=app.py
ENV FLASK_ENV=production

# Run Gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
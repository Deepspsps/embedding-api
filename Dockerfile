# Use a lightweight Python image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port for Railway (they’ll inject PORT env var)
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

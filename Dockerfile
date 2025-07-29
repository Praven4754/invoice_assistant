FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything into the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Start app
CMD ["python", "app.py"]

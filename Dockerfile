FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Load .env manually if needed (not strictly required unless your app does it)
# RUN pip install python-dotenv

# Expose app port
EXPOSE 7860

# Run your main app
CMD ["python", "app.py"]

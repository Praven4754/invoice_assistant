# Use Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Expose Gradio port (if you use it)
EXPOSE 7860

# Run your main file
CMD ["python", "app.py"]

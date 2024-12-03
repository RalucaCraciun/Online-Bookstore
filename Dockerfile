FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy application code
COPY app /app

RUN pip install --no-cache-dir -r /app/requirements.txt


# Expose the port
EXPOSE 8000

WORKDIR /

# Command to run FastAPI using uvicorn
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

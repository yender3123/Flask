FROM python:3.12-slim

# Create a non-root user
RUN useradd -m myuser

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Change ownership to non-root user
RUN chown -R myuser:myuser /app

# Switch to non-root user
USER myuser

# Expose port
EXPOSE 8080

# Run application
CMD ["python", "main.py"]
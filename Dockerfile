# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install --with-deps chromium

# Expose port
EXPOSE 5000

# Run using gunicorn (production server)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]

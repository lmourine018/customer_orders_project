# Base Image
FROM python:3.10

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Copy files
COPY . /app/

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Run migrations and start server
CMD ["gunicorn", "customer_order.wsgi:application", "--bind", "0.0.0.0:8000"]

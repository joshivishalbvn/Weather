# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables to avoid Python buffering
ENV PYTHONUNBUFFERED 1

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements/ /app/requirements/

# Install the dependencies from the requirements file
RUN pip install --upgrade pip
RUN pip install -r /app/requirements/base.txt

# Copy the entire project into the container
COPY . /app/

# Ensure wait-for-it.sh is executable
COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Expose port 8000 for the app to be accessible
EXPOSE 8000

# Command to run the Django development server after migrations
CMD ["./wait-for-it.sh", "redis:6379", "--", "bash", "-c", "python manage.py seed && python manage.py add_cities && celery -A weather worker --loglevel=info & celery -A weather beat --loglevel=info & python manage.py runserver 0.0.0.0:8000"]


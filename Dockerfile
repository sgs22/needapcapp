# Use an official Python runtime as the base image
FROM python:3.11

ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the working directory
COPY requirements.txt .

# Install the Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django project code to the working directory
COPY . .

# Expose the default Django port
EXPOSE 8100

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8100"]
# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the rest of the codebase into the workdir
COPY . .

# Copy the requirements.txt file into our workdir
COPY requirements.txt ./

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the app runs on
EXPOSE 5000

# Command to run on container start
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]

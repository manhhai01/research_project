# Use a lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR ./app

# Copy requirements and install dependencies
COPY ./api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY ./api .

# Expose the port the app runs on
EXPOSE 8000
EXPOSE 8001

# Default command to run the app
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get -y install curl
RUN apt-get install libgomp1
CMD ["fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]
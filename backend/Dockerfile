# Use an official Python runtime as a parent image
FROM python:3.12 AS base

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port
EXPOSE 5001

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "5001"]

# Build another stage with a smaller image
FROM base AS production

# Copy only the necessary files to reduce the image size
COPY --from=base /app /app
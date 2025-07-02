FROM python:3.6-slim-buster
# Set the working directory in the container
WORKDIR /app
# Copy the requirements file into the container at /app
COPY requirements.txt ./
# Install the dependencies
RUN pip install -r requirements.txt
# Copy the rest of the application code into the container at /app
COPY . .
# Expose the port the app runs on
EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
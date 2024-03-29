# Use the official lightweight Python image.
# https://hub.docker.com/_/python

FROM python:3.9-slim

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# Create the LOGS directory
RUN mkdir -p /app/LOGS

# Copy local code to the container image.
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install --no-cache-dir -r requirements-prod.txt
RUN pip install Flask gunicorn 

# Make port 8000 available to the world outside this container
EXPOSE 8080
# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
# Timeout is set to 0 to disable the timeouts of the workers to allow Cloud Run to handle instance scaling.
CMD ["gunicorn", "-b", "0.0.0.0:8080","--access-logfile", "./LOGS/app.log", "app:app"]

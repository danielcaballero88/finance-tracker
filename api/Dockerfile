FROM python:3.9-slim

# Expose port 8000.
# This is just informational, to actually publish the port at runtime, use the
# command `docker run -p 8000:8000 ...`
EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY ./src /app

# Creates a non-root user with an explicit UID and adds permission to access the
# /app folder. For more info, please refer to:
# https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# Command to run. The host is directed to "0.0.0.0" to make it accessible from
# outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

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

# The following WORKDIR is where the app runs inside the container
WORKDIR /usr/local/api
# The COPY command puts everything that is in `./src` (in the host) into
# `./usr/local/api` (in the container). That's the WORKDIR by the way,
# so the RUN command below is executed there where all the files will be
# present.
COPY ./src /usr/local/api

# Creates a non-root user with an explicit UID and adds permission to access the
# `/usr/local/api` folder. For more info, please refer to:
# https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /usr/local/api
USER appuser

# Command to run. The host is directed to "0.0.0.0" to make it accessible from
# outside the container.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--reload"]

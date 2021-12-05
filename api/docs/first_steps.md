# First Steps

## Run the Server

From the root folder (`api`) run:

```bash
uvicorn src.main:app --reload
```

## Run the Container

The backend is containerized!

To build it get inside the "api" directory and do:

```bash
docker build -t ${TAG} .
```

To run it:

```bash
docker run -p 8000:8000 ${TAG}
```

The `-p` option allows to publish the port so it's accessible from the host.

To run the container and get inside:

```bash
docker run -it ${TAG} bash
```

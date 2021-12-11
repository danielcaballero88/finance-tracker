# First Steps

## Run the Server

From the root folder (`front`) run:

```bash
ng serve
```

This runs the Angular development server.

## Run the Container

The Frontend is containerized!

To build it get inside the "front" directory and do:

```bash
docker build -t ${TAG} .
```

To run it:

```bash
docker run -p 4200:4200 ${TAG}
```

The `-p` option allows to publish the port so it's accessible from the host.

To run the container and get inside:

```bash
docker run -it ${TAG} bash
```

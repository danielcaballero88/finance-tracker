# Finance Tracker App

The app consists, at the moment, of three docker images:
1. API
2. Frontend
3. MongoDB

## API

The API is built using Python + FastAPI, it will provide the logic interface 
between the Frontend and all other services (at the moment I can only think of
the database, but more could be added).

## Frontend

The Frontend is an Angular app with the purpose of providing a nice UI/UX.

## MongoDB

The MongoDB uses a remote image ("mongo:5.0"), the connection was tested using
Robo 3T and works fine.

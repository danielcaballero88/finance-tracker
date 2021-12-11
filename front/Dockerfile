FROM docker.io/library/node:16.13.1

RUN npm install -g @angular/cli @angular-devkit/build-angular

WORKDIR /app
COPY . .

RUN npm install

CMD ng serve --host 0.0.0.0

# Exposed port.
# This is just informational, to actually publish the port at runtime,
# use the `-p` option with `docker run`.
EXPOSE 4200

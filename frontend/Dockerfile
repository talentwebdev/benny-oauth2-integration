FROM node:14

# install npm version as same as local
# RUN npm install -g npm@6.14.5

# RUN npm i --unsafe-perm -g expo-cli@latest

# setup working directory
WORKDIR /app/frontend

# install npm packages
COPY ./package.json /app/frontend

# set git frontend module
RUN npm install

COPY . /app/frontend


# build stage


FROM node:20-bookworm AS build-stage

WORKDIR /app

COPY package.json .

RUN npm install

RUN npm i -g serve

COPY . .

RUN npm run build


FROM node:20-alpine3.19 AS prod-stage
COPY --from=build-stage /app/dist/ /dist
RUN npm install -g serve
EXPOSE 80

CMD [ "serve", "-s", "dist", "-p", "80" ]
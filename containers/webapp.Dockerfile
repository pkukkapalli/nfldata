FROM node:current as builder

WORKDIR /usr/src/app

COPY webapp/package*.json ./

RUN npm install

COPY webapp/src/ src/
COPY webapp/public/ public/
COPY webapp/.env.production ./

RUN npm run build

FROM nginx:latest

COPY --from=builder /usr/src/app/build/ /usr/share/nginx/html/

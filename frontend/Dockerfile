FROM node:lts-alpine3.20 AS builder

WORKDIR /app

COPY ./package.json ./
COPY ./package-lock.json ./

RUN npm install

COPY ./ ./

RUN npm run build

FROM nginx:stable-alpine3.19-otel as production

COPY ./nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=builder /app/dist ./usr/share/nginx/html/

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]

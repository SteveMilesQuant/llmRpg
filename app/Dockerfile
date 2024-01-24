FROM node:18-alpine AS build-stage

WORKDIR /stories-app
COPY ./*.json ./
RUN npm install

COPY . ./
RUN npm run build

FROM nginx:1.25-alpine
RUN  touch /var/run/nginx.pid && \
     chown -R nginx:nginx /var/cache/nginx /var/run/nginx.pid
USER nginx

WORKDIR /lul-app
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY --from=build-stage /lul-app/dist ./

EXPOSE 8080
CMD ["nginx", "-g", "daemon off;"]


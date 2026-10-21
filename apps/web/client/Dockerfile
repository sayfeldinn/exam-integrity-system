# syntax=docker/dockerfile:1
# M0-26: web client image — Vite build (env baked at build time) served by nginx.
# VITE_API_URL must be a URL the *browser* can reach (see infra/.env.example).
FROM node:20-alpine AS build

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
ARG VITE_API_URL=http://localhost:8000
ENV VITE_API_URL=$VITE_API_URL
RUN npm run build

FROM nginx:1.27-alpine
COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80

# frontend/Dockerfile

# Step 1: Use node image to build the app
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run build

# Step 2: Use nginx to serve the built files
FROM nginx:stable-alpine
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy default nginx config
EXPOSE 5173
CMD ["nginx", "-g", "daemon off;"]

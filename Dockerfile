# -------- Build Frontend --------
    FROM node:20-alpine AS frontend-builder

    WORKDIR /frontend
    COPY frontend/package*.json ./
    RUN npm install
    COPY frontend/ .
    RUN npm run build
    
    
    # -------- Final Container --------
    FROM python:3.11-slim
    
    # Set workdir
    WORKDIR /app
    
    # Install system dependencies (Python + Nginx)
    RUN apt-get update && apt-get install -y \
        build-essential \
        nginx \
        curl \
        && rm -rf /var/lib/apt/lists/*
    
    # Install backend Python packages
    COPY requirements.txt .
    RUN pip install --no-cache-dir -r requirements.txt
    
    # Copy backend app
    COPY app ./app
    COPY db ./db
    COPY data ./data
    
    # Copy frontend build output to Nginx
    RUN rm -rf /usr/share/nginx/html/*
    # Remove default Nginx site to prevent conflict
    RUN rm -f /etc/nginx/sites-enabled/default
    COPY --from=frontend-builder /frontend/dist /usr/share/nginx/html
    RUN ls -la /usr/share/nginx/html
    COPY nginx.conf /etc/nginx/conf.d/default.conf
    
    # Copy and set entrypoint
    COPY start.sh .
    RUN chmod +x start.sh
    
    # Create directories
    RUN mkdir -p /app/data/resumes /app/data/outputs
    
    # Expose both ports
    EXPOSE 80
    EXPOSE 8000
    
    # Start both backend and frontend
    CMD ["./start.sh"]
    
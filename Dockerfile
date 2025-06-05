FROM python:3.9-slim-buster

WORKDIR /app

# Install Node.js for building Vue frontend
RUN apt-get update && apt-get install -y curl && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Copy backend and frontend code
COPY . .

# Install backend dependencies
RUN pip install Flask==2.1.1
RUN pip install Flask-HTTPAuth==4.1.0
RUN pip install Flask-Login==0.6.2
RUN pip install Werkzeug==2.0.0
RUN pip install gunicorn
RUN pip install flask-cors flask_sqlalchemy

# Build frontend
WORKDIR /app/dufbuntu
RUN npm install
RUN npm run build

# Move built frontend to Flask static folder
WORKDIR /app
RUN mkdir -p static && cp -r dufbuntu/dist/* static/

# Expose Flask port
EXPOSE 5000

# Run Flask (serving static files)
CMD ["python", "app.py"]

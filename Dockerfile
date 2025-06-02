FROM python:3.9-slim-buster

WORKDIR /app

COPY . .


RUN pip install Flask==2.1.1
RUN pip install Flask-HTTPAuth==4.1.0
RUN pip install Flask-Login==0.6.2
RUN pip install Werkzeug==2.0.0
RUN pip install gunicorn


EXPOSE 5000

CMD ["python", "app.py"]

FROM python:3.8
RUN pip install flask && pip install flask-cors && pip install flask_limiter && pip install psycopg2  && pip install requests
COPY ./src /home/app/src
COPY docker-db-config.json /home/app
WORKDIR /home/app/src/main
CMD ["python3", "app.py"]
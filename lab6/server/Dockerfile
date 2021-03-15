FROM python:3.8-alpine
WORKDIR /app
COPY ./requirements.txt .
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
RUN pip install -r requirements.txt
EXPOSE 5000
COPY . /app
CMD ["flask", "run"]


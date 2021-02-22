web: gunicorn app:app
DATABASE_URL=$(heroku config:get DATABASE_URL -a salesman-api) python app.py
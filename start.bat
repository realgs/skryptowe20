@ECHO OFF
IF EXIST venv (
    venv\Scripts\activate
    python app.py --update
     
) ELSE (
    python -m venv venv
    venv\Scripts\activate
    python -m pip install --upgrade pip
    pip install requests, pandas, flask, flask-caching, flask-limiter
    python app.py --set-up
)
python app.py --run
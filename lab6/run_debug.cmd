@ECHO OFF

cd api
start python run.py --debug --update
cd ..

cd frontend
start npm run serve
cd ..

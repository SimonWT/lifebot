run: 

gunicorn app:app

push heroku: 

git add .
git commit -m "add another handler"
git push heroku master
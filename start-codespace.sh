sudo service --status-all
sudo service mongodb start

cd DeploymentCenter/web
gunicorn -w 2 -b 127.0.0.1:5000 app:app
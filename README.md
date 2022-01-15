# Первый запуск

```
cd /srv/front-office
python3 -m venv venv

cat gunicorn.ini > /etc/systemd/system/front-office.service

sudo systemctl start front-office
sudo systemctl enable front-office
sudo systemctl status front-office

cat nginx.conf > /etc/nginx/sites-available/front-office
sudo ln -s /etc/nginx/sites-available/front-office /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx

sudo ufw allow 'Nginx Full'

sudo add-apt-repository ppa:certbot/certbot
sudo apt install python-certbot-nginx
sudo certbot --nginx -d i.easytap.io

```

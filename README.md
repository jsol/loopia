# Loopia IP refresher

Loopia is a swedish domain registrar. This is a helper script that checks
the public IP of the server running it and updates all the domains and
subdomain A records to the new IP if needed.

Edit loopia.service with the auth of your API user (can be created on the loopia
customer pages)

Edit loopia.timer with the interval you want to check (default is soon after boot
and once per hour)

sudo cp loopia.py /usr/local/bin/
sudp cp loopia.service /etc/systemd/system/
sudp cp loopia.timer /etc/systemd/system/

sudo useradd loopia
sudo touch /var/currentip
sudo chown loopia /var/currentip

systemctl daemon-reload
systemctl enable loopia.timer

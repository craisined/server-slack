# Server Slack
A slack bot for monitoring my docker server

# Commands
- `/server-ping`: check if my server is alive
- `/server-stats`: check if my server is dying (cpu, ram, and disk stats)
- `/server-docker`: check if my stack is dying (disk consumption and dead containers)
- `/server-updates`: check how long I neglected my server for (lists updatable packages)

# Deployment
A Debian based distro is required for apt:
```
git clone https://github.com/craisined/server-slack.git
cd server-slack
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
pip install -r requirements.txt
sudo .venv/bin/python3 main.py
```

# Tech
- Slack Bolt for Python used for Slack bot
- Docker Python SDK used for Docker inference
- Apt used for updates

# Other
No AI used, made for Stardance
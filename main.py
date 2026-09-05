from datetime import datetime, timedelta
from dotenv import load_dotenv
from slack_bolt import App
import os
import psutil
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.command("/server-ping")
def ping(ack, respond, command):
    ack()
    respond("Pong!")

@app.command("/server-stats")
def server_stats(ack, respond, command):
    ack()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    boot_duration = datetime.now() - boot_time
    clean_boot_duration = boot_duration - timedelta(microseconds=boot_duration.microseconds)
    msg = f"""
*CPU utilization*: {psutil.cpu_percent()}%
*RAM utilization*: {(psutil.virtual_memory().used / (1024 ** 3)):.3f}/{(psutil.virtual_memory().total / (1024 ** 3)):.3f} GB
*Last reboot*: {boot_time} ({clean_boot_duration} ago)
"""
    respond(msg)

if __name__=="__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()
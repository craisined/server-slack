import apt
from datetime import datetime, timedelta
import docker
from dotenv import load_dotenv
from slack_bolt import App
import os
import psutil
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"])
docker_client = docker.from_env()


@app.command("/server-ping")
def ping(ack, respond, command):
    ack()
    respond("Pong! minicraisin is alive")


@app.command("/server-stats")
def server_stats(ack, respond, command):
    ack()
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    boot_duration = datetime.now() - boot_time
    clean_boot_duration = boot_duration - timedelta(
        microseconds=boot_duration.microseconds
    )
    msg = f"""
*CPU utilization*: {psutil.cpu_percent()}%
*RAM utilization*: {(psutil.virtual_memory().used / (1024 ** 3)):.2f}/{(psutil.virtual_memory().total / (1024 ** 3)):.2f} GB
*Last reboot*: {boot_time} ({clean_boot_duration} ago)
"""
    disks = psutil.disk_partitions()
    disk_msg = "*Disks*:\n" + "\n".join(
        [
            f"• {p.device} | {(psutil.disk_usage(p.mountpoint).used / (1024 ** 3)):.2f} / {(psutil.disk_usage(p.mountpoint).total / (1024 ** 3)):.2f} GB"
            for p in psutil.disk_partitions()
        ]
    )
    respond(msg + disk_msg if disks else msg)


@app.command("/server-docker")
def server_docker(ack, respond, command):
    ack()
    disk = docker_client.df()
    container_usage = sum(c.get("SizeRw", 0) for c in disk.get("Containers", []))
    img_usage = sum(img.get("Size", 0) for img in disk.get("Images", []))
    msg = f"*Disk Usage*: {((container_usage + img_usage) / (1024 ** 3)):.2f} GB (container: {(container_usage / (1024 ** 3)):.2f} GB | img: {(img_usage/ (1024 ** 3)):.2f} GB)\n"
    unhealthy_containers = docker_client.containers.list(
        all=True, filters={"status": ["paused", "exited", "dead", "restarting"]}
    )
    if unhealthy_containers:
        msg += "*Unhealthy containers*:\n"
    for container in unhealthy_containers:
        msg += f"• {container.name} | {container.status}\n"
    respond(msg)

@app.command("/server-updates")
def server_updates(ack, respond, command):
    pass

if __name__ == "__main__":
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

import psutil

#Stats
print(psutil.cpu_percent())
print(psutil.virtual_memory().available)
print(psutil.virtual_memory().active)

# Storage
print(psutil.disk_partitions())
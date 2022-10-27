import os
import subprocess

import requests # pip install requests
import hashlib # pip install hashlib

SERVER_FILE = "server.jar"
SERVER_VERSION = "1.19.2"
ALLOCATED_MEMORY = 4096 # mb

os.chdir(os.path.dirname(os.path.realpath(__file__)))

def main():

    print("Getting version information...")
    response = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{SERVER_VERSION}")
    if response.status_code != 200:
        print("Error: Failed to get version information.")
        exit(1)
    latest_build = response.json()["builds"][-1]

    print("Checking for updates...")
    response = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{SERVER_VERSION}/builds/{latest_build}")
    if response.status_code != 200:
        print("Error: Failed to get latest build information.")
        exit(1)
    application_info = response.json()["downloads"]["application"]

    if not os.path.exists(SERVER_FILE) or hash_file(SERVER_FILE) != application_info["sha256"]:

        print("Downloading latest build...")
        response = requests.get(f"https://api.papermc.io/v2/projects/paper/versions/{SERVER_VERSION}/builds/{latest_build}/downloads/{application_info['name']}", stream=True)
        if response.status_code != 200:
            print("Error: Failed to download latest build.")
            exit(1)
        with open(SERVER_FILE, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

    print("Starting server...")
    print()
    subprocess.run([

        "java",

        f"-Xms{ALLOCATED_MEMORY}M",
        f"-Xmx{ALLOCATED_MEMORY}M",

        "-XX:+UseG1GC",
        "-XX:+ParallelRefProcEnabled",
        "-XX:MaxGCPauseMillis=200",
        "-XX:+UnlockExperimentalVMOptions",
        "-XX:+DisableExplicitGC",
        "-XX:+AlwaysPreTouch",
        "-XX:G1NewSizePercent=30",
        "-XX:G1MaxNewSizePercent=40",
        "-XX:G1HeapRegionSize=8M",
        "-XX:G1ReservePercent=20",
        "-XX:G1HeapWastePercent=5",
        "-XX:G1MixedGCCountTarget=4",
        "-XX:InitiatingHeapOccupancyPercent=15",
        "-XX:G1MixedGCLiveThresholdPercent=90",
        "-XX:G1RSetUpdatingPauseTimePercent=5",
        "-XX:SurvivorRatio=32",
        "-XX:+PerfDisableSharedMem",
        "-XX:MaxTenuringThreshold=1",
        "-Dusing.aikars.flags=https://mcflags.emc.gs",
        "-Daikars.new.flags=true",

        "-jar",
        SERVER_FILE,
        "--nogui"

    ])

    exit(0)

def hash_file(file_name):

    buffer_size = 65536
    hash = hashlib.sha256()
    with open(file_name, 'rb') as file:
        while True:
            data = file.read(buffer_size)
            if not data:
                break
            hash.update(data)
    return hash.hexdigest()

main()
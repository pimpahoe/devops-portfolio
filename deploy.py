import subprocess
import sys
import time

def run (command, description):
    print(f"\n>>> {description}")
    result = subprocess.run(command.split(), capture_output=False)
    if result.returncode != 0:
        print(f"Ошибка: {description} ")
        sys.exit(1)
    print(f"Done")

print("===Deploy===")

run("docker compose down", "Stop old containers")
run("docker compose up --build -d", "Build and start new stack")

print("\n Waiting for services up...")
time.sleep(5)

run("python health_check.py", "Services health check")

print("\n===Deploy is done===")

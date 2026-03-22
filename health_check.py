import requests
import subprocess
import sys

SERVICES = {
    "Nginx": "http://localhost/tasks",
    "app1": "http://localhost/tasks",
}

def check_http(name,url):
    try:
        r = requests.get(url, timeout=3)
        if r.status_code == 200:
            print(f"{name} is working ({r.status_code})")
            return True
        else:
            print(f"{name} is not working ({r.status_code})")
            return False
    except Exception as e:
        print(f"{name} is not working ({e})")
        return False

def check_container(name):
    result = subprocess.run(
        ["docker","inspect","--format","{{.State.Status}}", name],
        capture_output=True, text=True
    )
    status = result.stdout.strip()
    if status == "running":
        print(f"{name} is working ({status})")
        return True
    else:
        print(f"{name} is not working ({status})")
        return False

print("===Health Check===")

print("[Containers]")
containers = [
    "pythonproject-app1-1",
    "pythonproject-app2-1",
    "pythonproject-nginx-1",
    "pythonproject-db-1",
]

results = [check_container(c) for c in containers]
print("\n[ HTTP ]")
results.append(check_http("API from Nginx", "http://localhost/tasks"))

print("\n" + "="*20)
if all(results):
    print("All services are working")
else:
    print("Some services are not working")
    sys.exit(1)
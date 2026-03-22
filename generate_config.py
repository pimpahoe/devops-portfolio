import yaml

def generate_compose(app_count=2, db_name="tododb", db_user="todouser", db_password="todopass"):

    services = {}

    #БД
    services["db"] = {
        "image": "postgres:16-alpine",
        "environment": {
            "POSTGRES_DB": db_name,
            "POSTGRES_USER": db_user,
            "POSTGRES_PASSWORD": db_password,
        },
        "volumes": ["postgres_data:/var/lib/postgresql/data"]
    }

    #Инстансы Фласка
    for i in range(1, app_count + 1):
        services[f"app{i}"] = {
            "build": ".",
            "environment": {
                "DB_HOST": "db",
                "DB_PORT": 5432,
                "DB_NAME": db_name,
                "DB_USER": db_user,
                "DB_PASSWORD": db_password,
            },
            "depends_on": ["db"]
        }

    #nginx
    services["nginx"] = {
        "image": "nginx:alpine",
        "ports": ["80:80"],
        "volumes": [
            "./nginx.conf:/etc/nginx/conf.d/default.conf",
            "./index.html:/usr/share/nginx/html/index.html",
        ],
        "depends_on": [f"app{i}" for i in range(1, app_count + 1)]
    }
    config = {
        "services": services,
        "volumes": {"postgres_data": None}
    }

    with open("docker_compose.generated.yml", "w") as f:
        yaml.dump(config, f, default_flow_style=False, sort_keys=False)

    print(f"Generated docker-compose.yml with {app_count} Flask instances")

generate_compose(app_count=3)
from flask import Flask, jsonify, request, abort
import psycopg2
import os

app = Flask(__name__)

def get_db():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", 5432),
        database=os.environ.get("DB_NAME", "tododb"),
        user=os.environ.get("DB_USER", "todouser"),
        password=os.environ.get("DB_PASSWORD", "todopass")
    )

def init_db():
    retries = 5
    while retries > 0:
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id SERIAL PRIMARY KEY,
                    title TEXT NOT NULL,
                    done BOOLEAN DEFAULT FALSE
                )
            """)
            conn.commit()
            cur.close()
            conn.close()
            print("БД готова")
            return
        except Exception as e:
            print(f"Жду PostgreSQL... ({e})")
            retries -= 1
            import time
            time.sleep(3)
    raise Exception("Не удалось подключиться к БД")

# GET /tasks — список всех задач
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    tasks = [{"id": r[0], "title": r[1], "done": r[2]} for r in rows]
    return jsonify(tasks), 200


# POST /tasks — добавить задачу
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    if not data or "title" not in data:
        abort(400, description="Field 'title' is required")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, done) VALUES (%s, %s) RETURNING id",
        (data["title"], data.get("done", False))
    )
    task_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()

    return jsonify({"id": task_id, "title": data["title"], "done": data.get("done", False)}), 201


# PUT /tasks/<id> — обновить задачу
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    if not data:
        abort(400, description="JSON body is required")

    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE tasks SET title=%s, done=%s WHERE id=%s RETURNING id",
        (data.get("title"), data.get("done", False), task_id)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        abort(404, description=f"Task {task_id} not found")

    return jsonify({"id": task_id, "title": data.get("title"), "done": data.get("done", False)}), 200


# DELETE /tasks/<id> — удалить задачу
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM tasks WHERE id=%s RETURNING id",
        (task_id,)
    )
    row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()

    if row is None:
        abort(404, description=f"Task {task_id} not found")

    return jsonify({"message": f"Task {task_id} deleted"}), 200


@app.errorhandler(400)
@app.errorhandler(404)
def handle_error(e):
    return jsonify({"error": str(e.description)}), e.code


if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", debug=True)

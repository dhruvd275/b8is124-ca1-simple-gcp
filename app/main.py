from flask import Flask, jsonify, request
from google.cloud import datastore

app = Flask(__name__)
db = datastore.Client()
KIND = "Task"

@app.get("/")
def home():
    return "B8IS124 CA1 - App Engine + Datastore Mode is running"

@app.post("/add")
def add_item():
    data = request.get_json(silent=True) or {}
    task = (data.get("task") or "").strip()
    if not task:
        return jsonify({"error": "task is required"}), 400

    entity = datastore.Entity(key=db.key(KIND))
    entity.update({"task": task})
    db.put(entity)

    return jsonify({"status": "ok", "id": entity.key.id})

@app.get("/tasks")
def list_tasks():
    query = db.query(kind=KIND)
    tasks = []
    for entity in list(query.fetch()):
        tasks.append({"id": entity.key.id, "task": entity.get("task", "")})
    return jsonify(tasks)

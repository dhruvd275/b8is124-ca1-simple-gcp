from flask import Flask, jsonify, request
from google.cloud import datastore

app = Flask(__name__)
db = datastore.Client()
KIND = "Task"

@app.get("/")
def home():
    return """
    <div style="
        background: #0f9d58;
        color: white;
        padding: 12px 18px;
        font-family: Arial, sans-serif;
        font-size: 14px;
        border-radius: 8px;
        display: inline-block;
        margin-bottom: 16px;
    ">
        🟢 Live on Google Cloud · Auto-deployed via CI/CD
    </div>
    <h2 style="font-family: Arial, sans-serif;">
        B8IS124 CA1 – App Engine + Firestore (Datastore mode)
    </h2>
    <p style="font-family: Arial, sans-serif;">
        This application demonstrates cloud deployment, persistent storage, and automated CI/CD.
    </p>
    """

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
        tasks.append({
            "id": entity.key.id,
            "task": entity.get("task", "")
        })
    return jsonify(tasks)

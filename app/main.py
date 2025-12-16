from flask import Flask, jsonify, request
from google.cloud import firestore

app = Flask(__name__)
db = firestore.Client()

@app.get("/")
def home():
    return "B8IS124 CA1 - App Engine + Firestore is running"

@app.post("/add")
def add_item():
    data = request.get_json(silent=True) or {}
    task = data.get("task", "").strip()
    if not task:
        return jsonify({"error": "task is required"}), 400

    doc_ref = db.collection("tasks").add({"task": task})
    return jsonify({"status": "ok", "id": doc_ref[1].id})

@app.get("/tasks")
def list_tasks():
    tasks = []
    for doc in db.collection("tasks").stream():
        item = doc.to_dict()
        item["id"] = doc.id
        tasks.append(item)
    return jsonify(tasks)


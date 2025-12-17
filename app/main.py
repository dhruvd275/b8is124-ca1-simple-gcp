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
        Visual demo: <a href="/ui">/ui</a>
    </p>
    """

@app.get("/ui")
def ui():
    return """
<!doctype html>
<html>
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Firestore Task Demo</title>
</head>
<body style="font-family: Arial, sans-serif; margin: 24px; max-width: 720px;">

  <div style="
      background: #1a73e8;
      color: white;
      padding: 10px 14px;
      border-radius: 10px;
      display: inline-block;
      margin-bottom: 16px;
  ">
    ☁️ Firestore-backed Task List (Live)
  </div>

  <h2>Add a Task</h2>

  <div style="display: flex; gap: 10px; margin-bottom: 16px;">
    <input id="taskInput" placeholder="Type a task..." style="
        flex: 1;
        padding: 10px 12px;
        border: 1px solid #ddd;
        border-radius: 10px;
        font-size: 14px;
    " />
    <button onclick="addTask()" style="
        padding: 10px 14px;
        border: none;
        border-radius: 10px;
        background: #0f9d58;
        color: white;
        cursor: pointer;
    ">Add</button>
  </div>

  <div id="msg" style="margin-bottom: 12px; color: #555;"></div>

  <h3>Tasks (stored in Firestore)</h3>
  <ul id="taskList"></ul>

<script>
async function refreshTasks() {
  const res = await fetch('/tasks');
  const tasks = await res.json();
  const ul = document.getElementById('taskList');
  ul.innerHTML = '';
  tasks.forEach(t => {
    const li = document.createElement('li');
    li.style.marginBottom = '6px';
    li.innerHTML = `
      ${t.task}
      <button onclick="deleteTask(${t.id})"
        style="
          margin-left: 10px;
          background: #d93025;
          color: white;
          border: none;
          border-radius: 6px;
          padding: 4px 8px;
          cursor: pointer;
        ">
        Delete
      </button>
    `;
    ul.appendChild(li);
  });
}

async function addTask() {
  const input = document.getElementById('taskInput');
  const task = (input.value || '').trim();
  const msg = document.getElementById('msg');

  if (!task) {
    msg.textContent = 'Please enter a task.';
    return;
  }

  msg.textContent = 'Adding...';

  const res = await fetch('/add', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({task})
  });

  if (!res.ok) {
    msg.textContent = 'Failed to add task.';
    return;
  }

  input.value = '';
  msg.textContent = 'Added ✅';
  refreshTasks();
}

async function deleteTask(id) {
  await fetch('/delete/' + id, { method: 'DELETE' });
  refreshTasks();
}

refreshTasks();
</script>
</body>
</html>
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

@app.delete("/delete/<int:item_id>")
def delete_item(item_id):
    key = db.key(KIND, item_id)
    db.delete(key)
    return jsonify({"status": "deleted"})

@app.get("/tasks")
def list_tasks():
    query = db.query(kind=KIND)
    tasks = []
    for entity in list(query.fetch()):
        tasks.append({"id": entity.key.id, "task": entity.get("task", "")})
    return jsonify(tasks)

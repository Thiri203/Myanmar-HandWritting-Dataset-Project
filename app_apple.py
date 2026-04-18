## Myanmar Syllable Handwritten Collector - Flask Backend (Windows / Dell Laptop + iPad + Apple Pencil)
## Based on app.py by Ye Kyaw Thu, LU Lab., Myanmar
## Separate version for friend running on Windows PC with iPad + Apple Pencil
## How to run: python app_friend.py
## Then open on iPad browser: http://<laptop-ip>:5000

import os
import json
import re
import time
from datetime import datetime
from flask import Flask, render_template, request, jsonify, session
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'myanmar-syllable-collector-secret'

DATASET_DIR = "dataset"
SYLLABLE_FILE = "syl.txt"

os.makedirs(DATASET_DIR, exist_ok=True)


# -------------------------
# Load Syllables
# -------------------------
def load_syllables():
    if not os.path.exists(SYLLABLE_FILE):
        return []
    with open(SYLLABLE_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return lines


# -------------------------
# User Management
# -------------------------
@app.route('/api/users', methods=['GET'])
def get_users():
    os.makedirs(DATASET_DIR, exist_ok=True)
    users = []
    for user in os.listdir(DATASET_DIR):
        user_path = os.path.join(DATASET_DIR, user)
        if os.path.isdir(user_path):
            info_path = os.path.join(user_path, "user_info.json")
            if os.path.exists(info_path):
                with open(info_path, "r") as f:
                    info = json.load(f)
                users.append(info)
            else:
                users.append({"name": user, "age": None, "sex": None, "education": None})
    return jsonify(users)


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.json
    name = data.get('name', '').replace(" ", "_")
    if not name:
        return jsonify({"error": "Name required"}), 400

    name = secure_filename(name)
    user_path = os.path.join(DATASET_DIR, name)

    if os.path.exists(user_path):
        return jsonify({"error": "User already exists"}), 400

    os.makedirs(user_path, exist_ok=True)

    user_info = {
        "name": name,
        "age": data.get('age'),
        "sex": data.get('sex'),
        "education": data.get('education'),
        "created_at": datetime.now().isoformat()
    }

    with open(os.path.join(user_path, "user_info.json"), "w") as f:
        json.dump(user_info, f)

    session['current_user'] = name
    return jsonify(user_info), 201


@app.route('/api/users/<user_name>', methods=['GET'])
def select_user(user_name):
    user_name = secure_filename(user_name)
    user_path = os.path.join(DATASET_DIR, user_name)

    if not os.path.exists(user_path):
        return jsonify({"error": "User not found"}), 404

    info_path = os.path.join(user_path, "user_info.json")
    if os.path.exists(info_path):
        with open(info_path, "r") as f:
            user_info = json.load(f)
    else:
        user_info = {"name": user_name}

    written = set()
    for f in os.listdir(user_path):
        m = re.match(r"(\d+)-\d+\.txt", f)
        if m:
            written.add(int(m.group(1)))

    syllables = load_syllables()
    total = len(syllables)

    resume_index = 1
    if total > 0:
        for idx in range(1, total + 1):
            if idx not in written:
                resume_index = idx
                break
        else:
            resume_index = total

    progress = {
        "completed": len(written),
        "total": total,
        "percentage": (len(written) / total * 100) if total else 0,
        "resume_index": resume_index
    }

    session['current_user'] = user_name

    return jsonify({
        "user_info": user_info,
        "progress": progress
    })


# -------------------------
# Syllable Data
# -------------------------
@app.route('/api/syllables', methods=['GET'])
def get_syllables():
    syllables = load_syllables()
    return jsonify({"syllables": syllables, "total": len(syllables)})


@app.route('/api/syllables/<int:index>', methods=['GET'])
def get_syllable(index):
    syllables = load_syllables()
    if index < 1 or index > len(syllables):
        return jsonify({"error": "Index out of range"}), 404
    return jsonify({
        "index": index,
        "syllable": syllables[index - 1],
        "total": len(syllables)
    })


# -------------------------
# Stroke Data
# -------------------------
@app.route('/api/save-strokes', methods=['POST'])
def save_strokes():
    data = request.json

    current_user = session.get('current_user')
    if not current_user:
        return jsonify({"error": "No user selected"}), 400

    syllable_index = data.get('syllable_index')
    strokes = data.get('strokes', [])

    if not syllable_index or syllable_index < 1:
        return jsonify({"error": "Invalid syllable index"}), 400

    if not strokes or len(strokes) == 0:
        return jsonify({"error": "No strokes to save"}), 400

    user_path = os.path.join(DATASET_DIR, current_user)
    os.makedirs(user_path, exist_ok=True)

    base = str(syllable_index)
    i = 1
    while True:
        fname = f"{base}-{i}.txt"
        fpath = os.path.join(user_path, fname)
        if not os.path.exists(fpath):
            break
        i += 1

    with open(fpath, "w") as f:
        for stroke_idx, stroke in enumerate(strokes):
            f.write(f"STROKE {stroke_idx + 1}\n")
            for point in stroke:
                x = point.get('x', 0)
                y = point.get('y', 0)
                t = point.get('t', time.time())
                f.write(f"{x} {y} {t}\n")
            f.write("\n")

    return jsonify({
        "success": True,
        "message": f"Saved {fname}",
        "filename": fname
    }), 201


@app.route('/api/get-user-progress', methods=['GET'])
def get_user_progress():
    current_user = session.get('current_user')
    if not current_user:
        return jsonify({"error": "No user selected"}), 400

    user_path = os.path.join(DATASET_DIR, current_user)

    written = set()
    for f in os.listdir(user_path):
        m = re.match(r"(\d+)-\d+\.txt", f)
        if m:
            written.add(int(m.group(1)))

    syllables = load_syllables()

    return jsonify({
        "completed": len(written),
        "total": len(syllables),
        "percentage": (len(written) / len(syllables) * 100) if syllables else 0,
        "completed_list": sorted(list(written))
    })


# -------------------------
# Serve Web App
# -------------------------
@app.route('/')
def index():
    return render_template('index_friend.html')


# -------------------------
# Error Handlers
# -------------------------
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Server error"}), 500


if __name__ == '__main__':
    PORT = 5000
    print("=" * 55)
    print("Myanmar Syllable Handwritten Collector")
    print("Windows / Dell Laptop + iPad + Apple Pencil Version")
    print("=" * 55)
    print(f"\nDataset Directory: {os.path.abspath(DATASET_DIR)}")
    print(f"Syllables Loaded : {len(load_syllables())}")
    print("\nTo access from iPad:")
    print("  1. Find your laptop IP address:")
    print("     - Open Command Prompt (Win+R, type cmd, Enter)")
    print("     - Type: ipconfig")
    print("     - Look for 'IPv4 Address' under your Wi-Fi adapter")
    print(f"  2. Open Safari on iPad: http://<laptop-ip>:{PORT}")
    print("     Example: http://192.168.1.5:5000")
    print("\nNote: Laptop and iPad must be on the same Wi-Fi network.")
    print("=" * 55)
    print(f"\nStarting server on http://0.0.0.0:{PORT}\n")

    app.run(host='0.0.0.0', port=PORT, debug=True)

from flask import Flask, request, jsonify
import json
import os
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # تسمح للمتصفح يوصل للسيرفر
LOG_FILE = "messages.json"

# نجهز الملف إذا ما كان موجود
if not os.path.exists(LOG_FILE):
    with open(LOG_FILE, "w") as f:
        json.dump([], f)

@app.route("/send", methods=["POST"])
def send_message():
    data = request.get_json()
    message = data.get("message")
    if not message:
        return jsonify({"error": "No message provided"}), 400

    log_entry = {
        "message": message,
        "ip": request.remote_addr,
        "time": datetime.now().isoformat()
    }

    # نضيف الرسالة إلى الملف
    with open(LOG_FILE, "r+") as f:
        old_data = json.load(f)
        old_data.append(log_entry)
        f.seek(0)
        json.dump(old_data, f, indent=4)

    return jsonify({"status": "saved", "entry": log_entry})

@app.route("/messages", methods=["GET"])
def get_logs():
    with open(LOG_FILE, "r") as f:
        data = json.load(f)
    return jsonify(data)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # تستخدم بورت من متغير البيئة أو الافتراضي 10000
    app.run(host="0.0.0.0", port=port)

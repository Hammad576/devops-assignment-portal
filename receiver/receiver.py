import json
from flask import Flask, request, jsonify

app = Flask(__name__)

REPORT_FILE = "test-report.json"


@app.route("/report", methods=["POST"])
def receive_report():
    report = request.get_json()

    if report is None:
        return jsonify({
            "error": "Invalid JSON report"
        }), 400

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)

    return jsonify({
        "message": "Report received successfully"
    }), 200


@app.route("/", methods=["GET"])
def home():
    return "DevOps Test Report Receiver is running."


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5001)

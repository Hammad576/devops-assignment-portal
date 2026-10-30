import json
import os
from urllib.parse import urlparse

from flask import Flask, render_template, request

app = Flask(__name__)

SUBMISSIONS_FILE = "submissions.json"


def load_submissions():
    if not os.path.exists(SUBMISSIONS_FILE):
        return []

    with open(SUBMISSIONS_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def save_submissions(submissions):
    with open(SUBMISSIONS_FILE, "w", encoding="utf-8") as file:
        json.dump(submissions, file, indent=4)


def is_valid_url(url):
    try:
        parsed_url = urlparse(url)
        return parsed_url.scheme in ("http", "https") and bool(parsed_url.netloc)
    except ValueError:
        return False


@app.route("/", methods=["GET", "POST"])
def index():
    message = None
    message_type = None
    submissions = load_submissions()

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        registration_number = request.form.get(
            "registration_number", ""
        ).strip()
        assignment_title = request.form.get(
            "assignment_title", ""
        ).strip()
        submission_url = request.form.get(
            "submission_url", ""
        ).strip()

        if not name:
            message = "Name is required."
            message_type = "error"

        elif not registration_number:
            message = "Registration number is required."
            message_type = "error"

        elif not assignment_title:
            message = "Assignment title is required."
            message_type = "error"

        elif not submission_url:
            message = "Submission URL is required."
            message_type = "error"

        elif not is_valid_url(submission_url):
            message = "Invalid submission URL."
            message_type = "error"

        else:
            submission = {
                "name": name,
                "registration_number": registration_number,
                "assignment_title": assignment_title,
                "submission_url": submission_url
            }

            submissions.append(submission)
            save_submissions(submissions)

            message = "Submission saved successfully."
            message_type = "success"

    return render_template(
        "index.html",
        message=message,
        message_type=message_type,
        submissions=submissions
    )


if __name__ == "__main__":
    app.run(debug=True, port=5000)

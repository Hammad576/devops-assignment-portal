import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import app.app as application


@pytest.fixture
def client(tmp_path, monkeypatch):
    submissions_file = tmp_path / "submissions.json"

    monkeypatch.setattr(
        application,
        "SUBMISSIONS_FILE",
        str(submissions_file)
    )

    application.app.config["TESTING"] = True

    with application.app.test_client() as test_client:
        yield test_client


def test_complete_valid_submission_is_saved(client):
    response = client.post(
        "/",
        data={
            "name": "Hammad Nawaz",
            "registration_number": "FA22-BCS-031",
            "assignment_title": "DevOps Mid",
            "submission_url": "https://github.com"
        }
    )

    assert response.status_code == 200
    assert b"Submission saved successfully." in response.data

    with open(application.SUBMISSIONS_FILE, "r", encoding="utf-8") as file:
        submissions = json.load(file)

    assert len(submissions) == 1
    assert submissions[0]["name"] == "Hammad Nawaz"
    assert submissions[0]["registration_number"] == "FA22-BCS-031"


def test_missing_registration_number_is_rejected(client):
    response = client.post(
        "/",
        data={
            "name": "Hammad Nawaz",
            "registration_number": "",
            "assignment_title": "DevOps Mid",
            "submission_url": "https://github.com"
        }
    )

    assert response.status_code == 200
    assert b"Registration number is required." in response.data

    if Path(application.SUBMISSIONS_FILE).exists():
        with open(
            application.SUBMISSIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            submissions = json.load(file)

        assert len(submissions) == 0


def test_invalid_submission_url_is_rejected(client):
    response = client.post(
        "/",
        data={
            "name": "Hammad Nawaz",
            "registration_number": "FA22-BCS-031",
            "assignment_title": "DevOps Mid",
            "submission_url": "hello"
        }
    )

    assert response.status_code == 200
    assert b"Invalid submission URL." in response.data

    if Path(application.SUBMISSIONS_FILE).exists():
        with open(
            application.SUBMISSIONS_FILE,
            "r",
            encoding="utf-8"
        ) as file:
            submissions = json.load(file)

        assert len(submissions) == 0

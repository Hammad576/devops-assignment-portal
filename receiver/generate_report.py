import json
import os
from datetime import datetime, timezone
import urllib.request

INPUT_FILE = "pytest-report.json"
OUTPUT_FILE = "formatted-report.json"


def main():
    with open(INPUT_FILE, "r", encoding="utf-8") as file:
        pytest_report = json.load(file)

    tests = []

    for test in pytest_report.get("tests", []):
        result = test.get("outcome", "unknown")

        failure_message = None

        call_data = test.get("call", {})

        if result == "failed":
            crash = call_data.get("crash", {})
            failure_message = crash.get("message")

            if not failure_message:
                failure_message = call_data.get("longrepr")

        tests.append({
            "name": test.get("nodeid", "unknown"),
            "result": result,
            "failure_message": failure_message
        })

    total = len(tests)
    passed = sum(1 for test in tests if test["result"] == "passed")
    failed = sum(1 for test in tests if test["result"] == "failed")

    report = {
        "repository": "devops-assignment-portal",
        "branch": "main",
        "commit_sha": "local-test",
        "run_id": "local-test-001",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "repository": os.environ.get(
        "GITHUB_REPOSITORY",
        "devops-assignment-portal"
         
         ),
        "branch": os.environ.get(
        "GITHUB_REF_NAME",
        "main"
         ),
        "commit_sha": os.environ.get(
        "GITHUB_SHA",
        "local-test"
         ),
        "run_id": os.environ.get(
        "GITHUB_RUN_ID",
        "local-test-001"
         ),
        "tests": tests,

        "total": total,
        "passed": passed,
        "failed": failed,
        "overall_status": "passed" if failed == 0 else "failed"
    }




    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(report, file, indent=4)
    
    receiver_url = os.environ.get(
    "REPORT_RECEIVER_URL",
    "http://127.0.0.1:5001/report"
    )
    with open(OUTPUT_FILE, "rb") as file:
        report_data = file.read()

    request = urllib.request.Request(
        receiver_url,
        data=report_data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(request) as response:
        response_data = response.read().decode("utf-8")

    print(f"Receiver response: {response_data}")
    print(f"Report generated: {OUTPUT_FILE}")
    print(f"Total: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Status: {report['overall_status']}")


if __name__ == "__main__":
    main()

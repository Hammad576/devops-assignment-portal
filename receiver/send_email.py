
import json
import os
import smtplib

from pathlib import Path
from email.message import EmailMessage


# Read the generated test report
report_file = Path("formatted-report.json")

if not report_file.exists():
    raise FileNotFoundError("formatted-report.json not found!")

with report_file.open("r", encoding="utf-8") as file:
    report = json.load(file)


# Read credentials from environment variables
sender_email = os.getenv("MAIL_USERNAME")
app_password = os.getenv("MAIL_PASSWORD")
receiver_email = os.getenv("MAIL_TO")

if not sender_email or not app_password or not receiver_email:
    raise ValueError("Email configuration is missing!")


# Prepare email
status = str(report.get("overall_status", "UNKNOWN")).upper()

message = EmailMessage()
message["Subject"] = f"[{status}] DevOps Assignment Portal Test Report"
message["From"] = sender_email
message["To"] = receiver_email

message.set_content(
    "Hello,\n\n"
    "Your automated DevOps test report is ready.\n\n"
    "The JSON test report is attached to this email.\n\n"
    "Regards,\n"
    "DevOps Assignment Portal - GitHub Actions"
)

# Attach JSON report
message.add_attachment(
    report_file.read_bytes(),
    maintype="application",
    subtype="json",
    filename=report_file.name
)


# Send email using Gmail SMTP
with smtplib.SMTP("smtp.gmail.com", 587, timeout=30) as smtp:
    smtp.starttls()
    smtp.login(sender_email, app_password)
    smtp.send_message(message)

print("Test report email sent successfully!")

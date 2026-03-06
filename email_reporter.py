# Email reporting module for job application statistics.
#
# This module:
# 1) Reads application data from SQLite
# 2) Builds a plain-text report
# 3) Sends the report via SMTP email

import smtplib
import sqlite3
from datetime import datetime
from email.message import EmailMessage


# SQLite DB file used by the project.
DB_FILE = "job_applications.db"


# Generate a text report from database statistics.
def generate_report():
    print("Generating job application report...")

    try:
        with sqlite3.connect(DB_FILE) as conn:
            cursor = conn.cursor()

            # Total applications count.
            cursor.execute("SELECT COUNT(*) FROM applications")
            total_applications = cursor.fetchone()[0]

            # Unique companies count.
            cursor.execute("SELECT COUNT(DISTINCT company) FROM applications")
            unique_companies = cursor.fetchone()[0]

            # Applications today count.
            # We compare date portion of applied_date with today's local date.
            today = datetime.now().date().isoformat()
            cursor.execute(
                """
                SELECT COUNT(*)
                FROM applications
                WHERE substr(applied_date, 1, 10) = ?
                """,
                (today,),
            )
            applications_today = cursor.fetchone()[0]

    except sqlite3.Error as exc:
        print(f"Database error while generating report: {exc}")
        return ""

    # Format report text in a beginner-friendly style.
    report = (
        "Job Bot Report\n\n"
        f"Total Applications: {total_applications}\n"
        f"Applications Today: {applications_today}\n"
        f"Companies Applied: {unique_companies}\n"
    )

    return report


# Send the generated report to the user's email address.
def send_email_report():
    print("Sending email notification...")

    # Ask user for SMTP credentials and recipient.
    sender_email = input("Enter your email address (sender): ").strip()
    sender_password = input("Enter your email password or app password: ").strip()
    smtp_server = input("Enter SMTP server (example: smtp.gmail.com): ").strip()
    smtp_port_raw = input("Enter SMTP port (example: 587): ").strip()
    recipient_email = input("Enter recipient email address: ").strip()

    # Basic validation.
    if not sender_email or not sender_password or not smtp_server or not smtp_port_raw or not recipient_email:
        print("Error: missing required email settings.")
        return False

    try:
        smtp_port = int(smtp_port_raw)
    except ValueError:
        print("Error: SMTP port must be a number.")
        return False

    # Build report first.
    report_text = generate_report()
    if not report_text:
        print("Error: report is empty. Email not sent.")
        return False

    # Create formatted email message.
    message = EmailMessage()
    message["Subject"] = "Job Application Automation Report"
    message["From"] = sender_email
    message["To"] = recipient_email
    message.set_content(report_text)

    # Send email via SMTP with TLS.
    try:
        with smtplib.SMTP(smtp_server, smtp_port, timeout=30) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)

        print("Email report sent successfully.")
        return True

    except smtplib.SMTPException as exc:
        print(f"Email sending failed: {exc}")
        return False
    except Exception as exc:
        print(f"Unexpected email error: {exc}")
        return False

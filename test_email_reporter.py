# Test script for email_reporter module.
#
# This script:
# 1) Generates and prints a report preview
# 2) Optionally sends the report via SMTP

from email_reporter import generate_report, send_email_report


# Main test entry.
def main():
    report = generate_report()

    if report:
        print("\nGenerated Report:\n")
        print(report)
    else:
        print("Failed to generate report.")
        return

    choice = input("Do you want to send this report email now? (y/n): ").strip().lower()
    if choice == "y":
        send_email_report()
    else:
        print("Email sending skipped.")


if __name__ == "__main__":
    main()

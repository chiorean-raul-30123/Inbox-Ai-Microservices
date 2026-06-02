import smtplib
from email.message import EmailMessage
from pathlib import Path


message = EmailMessage()
message["From"] = "andrei.popescu@client.local"
message["To"] = "intake@ai-inbox.local"
message["Subject"] = "Contract for review"
message.set_content("Hello, please process the attached contract.")

pdfPath = Path("SampleContract-Shuttle.pdf")

with pdfPath.open("rb") as file:
    message.add_attachment(
        file.read(),
        maintype="application",
        subtype="pdf",
        filename=pdfPath.name,
    )

with smtplib.SMTP("localhost", 1025) as smtp:
    smtp.send_message(message)

print("Email sent to Mailpit.")
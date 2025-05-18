import requests
import os


def send_email_maileroo(to_email, subject, html_content, plain_text=None):
    api_key = os.getenv("MAILEROO_API_KEY")

    # Correct endpoint from documentation
    url = "https://smtp.maileroo.com/send"

    # Headers with X-API-Key for authentication
    headers = {
        "X-API-Key": api_key
    }

    # Preparing data payload
    payload = {
        "from": f"Agendados <no-reply@25c7c7ffff3b7e3a.maileroo.org>",
        "to": to_email,
        "subject": subject,
        "html": html_content
    }

    # Add plain text version if provided
    if plain_text:
        payload["plain"] = plain_text

    # Send the request
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        print("Email sent successfully.")
        return response.json()
    else:
        print(f"Error sending email: {response.status_code} - {response.text}")
        return {"success": False, "message": response.text}
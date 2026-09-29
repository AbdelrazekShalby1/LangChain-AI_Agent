from langchain.tools import tool


@tool
def send_email(recipient: str, subject: str, body: str) -> str:
    """Send an email.

    This project uses a mock implementation so it is safe to run locally.
    Replace this function with Gmail/SMTP/SendGrid/etc. only after adding
    proper credentials and security controls.
    """
    return (
        f"Demo email sent to {recipient} with subject '{subject}'. "
        f"Body length: {len(body)} characters."
    )


@tool
def read_email(email_id: str) -> str:
    """Read a demo email by ID. Replace with a real email provider integration."""
    return (
        f"Demo email {email_id}: This is sample email content for the project."
    )

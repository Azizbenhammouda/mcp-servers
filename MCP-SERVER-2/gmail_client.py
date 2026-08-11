# Once auth.py hands us valid credentials 
# we still can't just directly ask Gmail for emails in plain English. 
# Google's API expects very specific calls, and it returns data in a deeply nested,
#  kind of ugly JSON format — full of stuff we don't care about 
# (internal IDs, MIME structure, etc)


from googleapiclient.discovery import build
from auth import get_credentials


def get_gmail_service():
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def list_recent_emails(max_results: int = 10):
  """
    Fetch the most recent emails from the user's Gmail inbox.

    Makes two API calls per batch: first to list message IDs, then one
    per message to fetch its headers (From, Subject, Date) and snippet.

    Args:
        max_results: Maximum number of emails to fetch. Defaults to 10.

    Returns:
        A list of dicts, one per email, each shaped like:
        {
            "id": "18e4f2a1b2c3d4e5",
            "from": "someone@example.com",
            "subject": "Meeting tomorrow",
            "date": "Tue, 11 Aug 2026 09:15:00 -0700",
            "snippet": "Hey, just wanted to confirm..."
        }
    """
    
  service = get_gmail_service()

    # Stage 1: get a bare list of message IDs
  results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()

  messages = results.get("messages", [])

    # Stage 2: fetch details for each message ID
  emails = []
  for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg_data["payload"]["headers"]
        email_info = {
            "id": msg["id"],
            "from": next((h["value"] for h in headers if h["name"] == "From"), ""),
            "subject": next((h["value"] for h in headers if h["name"] == "Subject"), ""),
            "date": next((h["value"] for h in headers if h["name"] == "Date"), ""),
            "snippet": msg_data.get("snippet", ""),
        }
        emails.append(email_info)

  return emails
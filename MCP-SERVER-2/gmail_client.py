"""
Thin wrapper around the Gmail API.

This module hides all the Gmail/Google-specific details (auth, nested
JSON shapes, base64 decoding, MIME parts) behind a few simple functions
that return plain Python data. Nothing outside this file should ever
need to touch `googleapiclient` directly.
"""

import base64
from googleapiclient.discovery import build
from auth import get_credentials


def get_gmail_service():
    """
    Build an authenticated Gmail API client.

    Returns:
        A `Resource` object (from googleapiclient) with methods for
        every Gmail API endpoint, e.g. service.users().messages()...
    """
    creds = get_credentials()
    return build("gmail", "v1", credentials=creds)


def _get_header(headers: list, name: str) -> str:
    """
    Pull a single header value out of Gmail's header list.

    Gmail returns headers as a flat list like:
        [{"name": "From", "value": "a@b.com"}, {"name": "Subject", ...}]
    instead of a dict, so we have to search for the one we want.

    Args:
        headers: The list of header dicts from a Gmail message payload.
        name: The header name to look for (e.g. "From", "Subject").

    Returns:
        The header's value, or "" if that header isn't present.
    """
    return next((h["value"] for h in headers if h["name"] == name), "")


def _decode_body(data: str) -> str:
    """
    Decode a base64url-encoded email body into plain text.

    Gmail encodes all body content this way for safe transport over JSON.

    Args:
        data: The base64url-encoded string from a message part's body.

    Returns:
        The decoded text. Any undecodable bytes are replaced rather
        than raising an error.
    """
    return base64.urlsafe_b64decode(data).decode("utf-8", errors="replace")


def _extract_plain_text(payload: dict) -> str:
    """
    Find and decode the plain-text body from a Gmail message payload.

    Handles both shapes Gmail can return:
    - Simple emails: body is directly at payload["body"]["data"]
    - Multipart emails (text + HTML, or attachments): body lives inside
      payload["parts"], and we need to find the part with
      mimeType == "text/plain".

    Args:
        payload: The "payload" object from a Gmail message (format="full").

    Returns:
        The decoded plain-text body, or "" if none could be found.
    """
    # Simple case: body data sits directly on the payload
    if payload.get("body", {}).get("data"):
        return _decode_body(payload["body"]["data"])

    # Multipart case: search through parts for a text/plain part
    for part in payload.get("parts", []):
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return _decode_body(part["body"]["data"])

        # Some emails nest parts inside parts (e.g. multipart/alternative
        # inside multipart/mixed) — recurse to handle that.
        if "parts" in part:
            nested = _extract_plain_text(part)
            if nested:
                return nested

    return ""


def list_recent_emails(max_results: int = 10) -> list[dict]:
    """
    Fetch the most recent emails from the user's Gmail inbox.

    Makes one API call to list message IDs, then one more call per
    message to fetch its headers (From, Subject, Date) and snippet.
    Does NOT fetch the full body — use get_email_body() for that.

    Args:
        max_results: Maximum number of emails to fetch. Defaults to 10.

    Returns:
        A list of dicts, one per email, shaped like:
        {
            "id": "18e4f2a1b2c3d4e5",
            "from": "someone@example.com",
            "subject": "Meeting tomorrow",
            "date": "Tue, 11 Aug 2026 09:15:00 -0700",
            "snippet": "Hey, just wanted to confirm..."
        }
    """
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()

    messages = results.get("messages", [])

    emails = []
    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="metadata",
            metadataHeaders=["From", "Subject", "Date"]
        ).execute()

        headers = msg_data["payload"]["headers"]
        emails.append({
            "id": msg["id"],
            "from": _get_header(headers, "From"),
            "subject": _get_header(headers, "Subject"),
            "date": _get_header(headers, "Date"),
            "snippet": msg_data.get("snippet", ""),
        })

    return emails


def get_email_body(message_id: str) -> dict:
    """
    Fetch the full content of a single email, including its plain-text body.

    Args:
        message_id: The Gmail message ID (e.g. from list_recent_emails()).

    Returns:
        A dict shaped like:
        {
            "id": "18e4f2a1b2c3d4e5",
            "from": "someone@example.com",
            "subject": "Meeting tomorrow",
            "date": "Tue, 11 Aug 2026 09:15:00 -0700",
            "body": "Hey, just wanted to confirm we're still on for..."
        }
    """
    service = get_gmail_service()

    msg_data = service.users().messages().get(
        userId="me", id=message_id, format="full"
    ).execute()

    payload = msg_data["payload"]
    headers = payload["headers"]

    return {
        "id": message_id,
        "from": _get_header(headers, "From"),
        "subject": _get_header(headers, "Subject"),
        "date": _get_header(headers, "Date"),
        "body": _extract_plain_text(payload),
    }


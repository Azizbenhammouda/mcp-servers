"""
Handles OAuth2 authentication for the Gmail API.

First run: opens a browser window for you to log in and grant access.
Later runs: reuses/refreshes the saved token in token.json automatically.
"""

import os
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Scopes define what this app is allowed to do with Gmail.
# Start read-only; widen later once you need to send/modify mail.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

CREDENTIALS_FILE = "credentials.json"
TOKEN_FILE = "token.json"


def get_credentials() -> Credentials:
    """
    Returns valid Gmail API credentials, handling the full lifecycle:
    - Load existing token if present
    - Refresh it if expired
    - Otherwise run the interactive OAuth flow and save a new token
    """
    creds = None

    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_FILE):
                raise FileNotFoundError(
                    f"{CREDENTIALS_FILE} not found. Download it from Google "
                    "Cloud Console (OAuth client ID, Desktop app type) and "
                    "place it in this directory."
                )
            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE, SCOPES
            )
            creds = flow.run_local_server(port=0)

        # Save the (refreshed or new) credentials for next time
        with open(TOKEN_FILE, "w") as token:
            token.write(creds.to_json())

    return creds
# Once auth.py hands us valid credentials 
# we still can't just directly ask Gmail for emails in plain English. 
# Google's API expects very specific calls, and it returns data in a deeply nested,
#  kind of ugly JSON format — full of stuff we don't care about 
# (internal IDs, MIME structure, etc)
from googleapiclient.discovery import build #to make a gmail client
from auth import get_credentials
def get_gmail_service():
  creds = get_credentials()
  return build("gmail","v1",credentials=creds)
def  list_recent_emails(max_results: int = 10):
    service = get_gmail_service()
    results = service.users().messages().list(
        userId="me", maxResults=max_results
    ).execute()

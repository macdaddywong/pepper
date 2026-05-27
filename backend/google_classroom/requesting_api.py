import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
URL="https://classroom.google.com/c/ODU4NDgzNTIwNzQ4"

# The scope defines what Pepper is allowed to see
SCOPES = ['https://www.googleapis.com/auth/classroom.coursework.readonly']

def get_classroom_assignments(course_id):
    creds = None
    
    # 1. Look for existing 'token.json' (saved login session)
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # 2. If no valid login, trigger the login flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You must download 'credentials.json' from Google Cloud Console first!
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        # 3. Save the session for next time
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    # 4. Build the service and fetch data
    service = build('classroom', 'v1', credentials=creds)
    results = service.courses().courseWork().list(courseId=course_id).execute()
    return results.get('courseWork', [])

if __name__ == "__main__":
    course_id = URL.split('/')[-1] 
    example = get_classroom_assignments(course_id)
    
    for assignment in example:
        print(f"Name: {assignment.get('title')}")
        
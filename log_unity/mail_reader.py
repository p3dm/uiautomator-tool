import os
import pickle
import base64
import re
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/spreadsheets.readonly"
]

def extract_unity_code(email_text):
    """Thử nhiều pattern để tìm OTP từ Unity"""
    patterns = [
        r"Your one-time login code:\s*(\d+)",
        r"code:\s*(\d{4,8})",
        r"OTP:\s*(\d{4,8})",
        r"verification code:\s*(\d{4,8})",
        r"login code is:\s*(\d{4,8})",
        r"\b(\d{6})\b"  # fallback: số 6 chữ số đứng riêng
    ]
    
    for pattern in patterns:
        match = re.search(pattern, email_text, re.IGNORECASE)
        if match:
            return match.group(1)
    
    return None

def get_gmail_service():
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def get_credentials():
    """Trả về credentials để dùng chung cho cả Gmail và Sheets"""
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            "client_secret.json",
            SCOPES
        )
        creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return creds


def get_latest_unity_otp(service):
    """
    Tìm OTP Unity từ email mới nhất
    From: Unity Nodes <noreply@unitynodes.io>
    Subject: Your Unity Login Code
    """
    # Query chính xác cho Unity Login Code
    results = service.users().messages().list(
        userId="me",
        q='from:unitynodes.io subject:"Your Unity Login Code" newer_than:1d',
        maxResults=1  # Lấy 1 mail mới nhất
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        print("[DEBUG] Không tìm thấy email 'Your Unity Login Code' từ unitynodes.io trong 24h qua")
        return None
    
    print(f"[DEBUG] Tìm thấy {len(messages)} email Unity Login Code, đang kiểm tra...")

    # Duyệt qua từng email để tìm OTP
    for i, msg_info in enumerate(messages):
        msg_id = msg_info["id"]
        
        msg_data = service.users().messages().get(
            userId="me",
            id=msg_id,
            format="full"
        ).execute()

        # Lấy subject và from để debug
        headers = msg_data["payload"].get("headers", [])
        subject = next((h["value"] for h in headers if h["name"].lower() == "subject"), "No Subject")
        from_email = next((h["value"] for h in headers if h["name"].lower() == "from"), "Unknown")
        print(f"[DEBUG] Email {i+1}: From={from_email}, Subject={subject}")

        payload = msg_data["payload"]
        email_text = ""
        
        # Trường hợp 1: Email có parts (multipart)
        parts = payload.get("parts", [])
        if parts:
            for part in parts:
                mime_type = part.get("mimeType", "")
                if "text/plain" in mime_type or "text/html" in mime_type:
                    body_data = part.get("body", {}).get("data")
                    if body_data:
                        decoded = base64.urlsafe_b64decode(body_data).decode(errors='ignore')
                        email_text += decoded + "\n"
        
        # Trường hợp 2: Email single-part (body trực tiếp)
        if not email_text:
            body_data = payload.get("body", {}).get("data")
            if body_data:
                email_text = base64.urlsafe_b64decode(body_data).decode(errors='ignore')

        # Tìm OTP trong nội dung
        if email_text:
            otp = extract_unity_code(email_text)
            if otp:
                print(f"[DEBUG] ✅ Tìm thấy OTP: {otp}")
                return otp
            else:
                # Debug: in một đoạn ngắn nội dung email
                preview = email_text[:300].replace('\n', ' ')
                print(f"[DEBUG] ❌ Không thấy OTP. Preview: {preview}...")

    print("[DEBUG] Không tìm thấy OTP trong tất cả các email")
    return None
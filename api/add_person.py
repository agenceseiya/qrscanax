from http.server import BaseHTTPRequestHandler
import json
import os
import gspread
from google.oauth2.service_account import Credentials
import traceback

def get_credentials():
    try:
        creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
        if not creds_json:
            raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
        creds_dict = json.loads(creds_json)
        return Credentials.from_service_account_info(creds_dict)
    except Exception as e:
        return f"Error in get_credentials: {str(e)}"

def add_person_to_sheet(firstname, lastname, email, telephone):
    try:
        creds = get_credentials()
        if isinstance(creds, str):  # This means there was an error
            raise ValueError(creds)
        client = gspread.authorize(creds)
        sheet = client.open('Visitor Database').sheet1
        row = [firstname, lastname, email, telephone]
        sheet.append_row(row)
        return ','.join(row)
    except Exception as e:
        return f"Error in add_person_to_sheet: {str(e)}"

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        try:
            qr_data = add_person_to_sheet(data['firstname'], data['lastname'], data['email'], data['telephone'])
            if qr_data.startswith("Error"):
                raise ValueError(qr_data)
            response = json.dumps({'success': True, 'qr_data': qr_data})
            status_code = 200
        except Exception as e:
            error_message = f"Error: {str(e)}\n\nTraceback:\n{traceback.format_exc()}"
            response = json.dumps({'success': False, 'error': error_message})
            status_code = 500

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

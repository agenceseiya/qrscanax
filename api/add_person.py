from http.server import BaseHTTPRequestHandler
import json
import os
import gspread
from google.oauth2.service_account import Credentials

def get_credentials():
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    return Credentials.from_service_account_info(creds_dict)

def add_person_to_sheet(firstname, lastname, email, telephone):
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # Make sure to replace 'Visitor Database' with your actual Google Sheet name
    sheet = client.open('Visitor Database').sheet1
    
    row = [firstname, lastname, email, telephone]
    sheet.append_row(row)
    return ','.join(row)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        try:
            qr_data = add_person_to_sheet(data['firstname'], data['lastname'], data['email'], data['telephone'])
            response = json.dumps({'success': True, 'qr_data': qr_data})
            status_code = 200
        except Exception as e:
            response = json.dumps({'success': False, 'error': str(e)})
            status_code = 500

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

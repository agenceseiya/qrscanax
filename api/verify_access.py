from http.server import BaseHTTPRequestHandler
import json
import os
import gspread
from google.oauth2.service_account import Credentials

def get_credentials():
    creds_json = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    return Credentials.from_service_account_info(creds_dict)

def verify_access(data):
    creds = get_credentials()
    client = gspread.authorize(creds)
    
    # Make sure to replace 'Visitor Database' with your actual Google Sheet name
    sheet = client.open('Visitor Database').sheet1
    
    # This assumes the data is a comma-separated string of values
    values = data.split(',')
    if len(values) != 4:
        return False
    
    # Search for the exact row
    cell_list = sheet.findall(values[0])  # Search by first name
    for cell in cell_list:
        row = sheet.row_values(cell.row)
        if row == values:
            return True
    
    return False

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        try:
            access_granted = verify_access(data['data'])
            message = 'Access granted' if access_granted else 'Access denied'
            response = json.dumps({'success': True, 'message': message})
            status_code = 200
        except Exception as e:
            response = json.dumps({'success': False, 'error': str(e)})
            status_code = 500

        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(response.encode('utf-8'))

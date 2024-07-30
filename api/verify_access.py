from http.server import BaseHTTPRequestHandler
import json
import gspread
from google.oauth2.service_account import Credentials

def verify_access(data):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('path/to/credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open('Visitor Database').sheet1
    
    cell = sheet.find(data)
    return cell is not None

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        access_granted = verify_access(data['data'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        message = 'Access granted' if access_granted else 'Access denied'
        response = json.dumps({'success': True, 'message': message})
        self.wfile.write(response.encode('utf-8'))

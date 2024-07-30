from http.server import BaseHTTPRequestHandler
import json
import gspread
from google.oauth2.service_account import Credentials

def add_person_to_sheet(firstname, lastname, email, telephone):
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = Credentials.from_service_account_file('path/to/credentials.json', scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open('Visitor Database').sheet1
    
    row = [firstname, lastname, email, telephone]
    sheet.append_row(row)
    return ','.join(row)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))

        qr_data = add_person_to_sheet(data['firstname'], data['lastname'], data['email'], data['telephone'])

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        response = json.dumps({'success': True, 'qr_data': qr_data})
        self.wfile.write(response.encode('utf-8'))

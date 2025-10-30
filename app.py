import http.server
import socketserver
import json
import os
import base64
from datetime import datetime
import urllib.parse
import threading

# Initialize data with thread safety
data_lock = threading.Lock()

# Initialize data
def init_data():
    with data_lock:
        if not os.path.exists('smartcampus_data.json'):
            data = {
                'users': {
                    '25CS001': {'password': 'smartcampus123', 'name': 'Alex Johnson', 'password_changed': False},
                    '25CS002': {'password': 'smartcampus123', 'name': 'Maria Garcia', 'password_changed': False},
                    '25CS003': {'password': 'smartcampus123', 'name': 'David Smith', 'password_changed': False},
                    '25CS004': {'password': 'smartcampus123', 'name': 'Sarah Williams', 'password_changed': False},
                    '25CS005': {'password': 'smartcampus123', 'name': 'James Brown', 'password_changed': False},
                    '25CS006': {'password': 'smartcampus123', 'name': 'Lisa Davis', 'password_changed': False},
                    '25CS007': {'password': 'smartcampus123', 'name': 'Michael Wilson', 'password_changed': False},
                    '25CS008': {'password': 'smartcampus123', 'name': 'Emma Taylor', 'password_changed': False},
                    '25CS009': {'password': 'smartcampus123', 'name': 'Robert Miller', 'password_changed': False},
                    '25CS010': {'password': 'smartcampus123', 'name': 'Olivia Anderson', 'password_changed': False}
                },
                'lost_items': [
                    {
                        'id': '1', 'user_id': '25CS001', 'user_name': 'Alex Johnson',
                        'type': 'laptop', 'description': 'Silver MacBook Pro 13" with mountain sticker on cover',
                        'location': 'Library - 2nd floor', 'date': '2024-01-15', 'status': 'active',
                        'created_at': '2024-01-15T10:00:00',
                        'image': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHg9IjEwIiB5PSIyMCIgd2lkdGg9IjE4MCIgaGVpZ2h0PSI4MCIgcng9IjUiIGZpbGw9IiMzNDk4REIiIGZpbGwtb3BhY2l0eT0iMC4xIi8+CjxyZWN0IHg9IjIwIiB5PSIzMCIgd2lkdGg9IjE2MCIgaGVpZ2h0PSI2MCIgcng9IjMiIGZpbGw9IiMzNDk4REIiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iNzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMzNDk4REIiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+TEFQVE9QPC90ZXh0Pgo8L3N2Zz4K'
                    }
                ],
                'found_items': [
                    {
                        'id': '2', 'user_id': '25CS005', 'user_name': 'James Brown', 
                        'type': 'laptop', 'description': 'Silver laptop with mountain sticker, found in computer lab',
                        'location': 'Computer Lab B', 'date': '2024-01-15', 'status': 'active',
                        'created_at': '2024-01-15T14:00:00',
                        'image': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+CjxyZWN0IHg9IjEwIiB5PSIyMCIgd2lkdGg9IjE4MCIgaGVpZ2h0PSI4MCIgcng9IjUiIGZpbGw9IiMyZWNjNzEiIGZpbGwtb3BhY2l0eT0iMC4xIi8+CjxyZWN0IHg9IjIwIiB5PSIzMCIgd2lkdGg9IjE2MCIgaGVpZ2h0PSI2MCIgcng9IjMiIGZpbGw9IiMyZWNjNzEiIGZpbGwtb3BhY2l0eT0iMC4yIi8+Cjx0ZXh0IHg9IjEwMCIgeT0iNzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMyZWNjNzEiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+TEFQVE9QPC90ZXh0Pgo8L3N2Zz4K'
                    }
                ],
                'chats': {
                    'chat_1_2': {
                        'messages': [
                            {
                                'id': '1', 'sender_id': '25CS005', 'sender_name': 'James Brown',
                                'message': 'Hello! I found a silver laptop in the computer lab. Does it belong to you?',
                                'timestamp': '2024-01-15T14:30:00'
                            },
                            {
                                'id': '2', 'sender_id': '25CS001', 'sender_name': 'Alex Johnson', 
                                'message': 'Yes! I lost my MacBook Pro. Does it have a mountain sticker?',
                                'timestamp': '2024-01-15T14:35:00'
                            },
                            {
                                'id': '3', 'sender_id': '25CS005', 'sender_name': 'James Brown',
                                'message': 'Yes, it has a mountain sticker! Where can we meet for you to collect it?',
                                'timestamp': '2024-01-15T14:40:00'
                            }
                        ]
                    }
                },
                'password_change_attempts': {}
            }
            with open('smartcampus_data.json', 'w') as f:
                json.dump(data, f, indent=2)

# Load data from file
def load_data():
    with data_lock:
        if os.path.exists('smartcampus_data.json'):
            with open('smartcampus_data.json', 'r') as f:
                return json.load(f)
        return {'users': {}, 'lost_items': [], 'found_items': [], 'chats': {}, 'password_change_attempts': {}}

# Save data to file
def save_data(data):
    with data_lock:
        with open('smartcampus_data.json', 'w') as f:
            json.dump(data, f, indent=2)

# HTML template (your complete HTML goes here - too long to include fully)
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartCampus Lost & Found</title>
    <style>
        /* Your complete CSS styles */
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div id="app"></div>
    <!-- Modals and other HTML elements -->
</body>
<script>
    // Your complete JavaScript code
</script>
</html>
'''

class SmartCampusHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode())
        elif self.path == '/data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            data = load_data()
            self.wfile.write(json.dumps(data).encode())
        elif self.path.startswith('/get_chat'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(self.path)
            query_params = parse_qs(parsed.query)
            chat_id = query_params.get('chat_id', [None])[0]
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            data = load_data()
            chat_data = data.get('chats', {}).get(chat_id, {'messages': []})
            self.wfile.write(json.dumps(chat_data).encode())
        else:
            super().do_GET()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data)
        
        user_data = load_data()
        response_data = {}
        
        if self.path == '/report':
            user_id = data.get('currentUser')
            
            new_item = {
                'id': str(len(user_data['lost_items']) + len(user_data['found_items']) + 1),
                'user_id': user_id,
                'user_name': user_data['users'][user_id]['name'],
                'type': data.get('item_type'),
                'description': data.get('description'),
                'location': data.get('location'),
                'date': data.get('date'),
                'image': data.get('image', ''),
                'status': 'active',
                'created_at': datetime.now().isoformat()
            }
            
            if data.get('type') == 'lost':
                user_data['lost_items'].append(new_item)
            else:
                user_data['found_items'].append(new_item)
                
            save_data(user_data)
            response_data = {'success': True, 'data': user_data}
            
        elif self.path == '/change_password':
            user_id = data.get('currentUser')
            current_password = data.get('current_password')
            new_password = data.get('new_password')
            
            if (user_id in user_data['users'] and 
                user_data['users'][user_id]['password'] == current_password):
                
                user_data['users'][user_id]['password'] = new_password
                user_data['users'][user_id]['password_changed'] = True
                
                if 'password_change_attempts' not in user_data:
                    user_data['password_change_attempts'] = {}
                user_data['password_change_attempts'][user_id] = True
                
                save_data(user_data)
                response_data = {'success': True}
            else:
                response_data = {'success': False, 'message': 'Invalid current password'}
        
        elif self.path == '/send_message':
            chat_id = data.get('chat_id')
            sender_id = data.get('sender_id')
            sender_name = data.get('sender_name')
            message = data.get('message')
            
            if chat_id not in user_data['chats']:
                user_data['chats'][chat_id] = {'messages': []}
            
            new_message = {
                'id': str(len(user_data['chats'][chat_id]['messages']) + 1),
                'sender_id': sender_id,
                'sender_name': sender_name,
                'message': message,
                'timestamp': datetime.now().isoformat()
            }
            
            user_data['chats'][chat_id]['messages'].append(new_message)
            save_data(user_data)
            response_data = {'success': True}
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

def main():
    init_data()
    
    # Use PORT environment variable for Render
    PORT = int(os.environ.get('PORT', 8000))
    
    with socketserver.TCPServer(("", PORT), SmartCampusHandler) as httpd:
        print(f"🚀 SmartCampus Lost & Found Portal Started!")
        print(f"📍 Access: http://localhost:{PORT}")
        print("👤 Demo Users: 25CS001 to 25CS010")
        print("🔑 Password: smartcampus123")
        print("💬 Real-time Chat: Enabled (works across devices)")
        print("📸 Features: Image Upload • Smart Matching • Live Chat • Password Management")
        print("🛑 Press Ctrl+C to stop")
        print("="*50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")

if __name__ == "__main__":
    main()

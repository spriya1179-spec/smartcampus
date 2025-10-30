import http.server
import socketserver
import json
import os
import base64
from datetime import datetime
import urllib.parse

# Initialize data
def init_data():
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
    if os.path.exists('smartcampus_data.json'):
        with open('smartcampus_data.json', 'r') as f:
            return json.load(f)
    return {'users': {}, 'lost_items': [], 'found_items': [], 'chats': {}, 'password_change_attempts': {}}

# Save data to file
def save_data(data):
    with open('smartcampus_data.json', 'w') as f:
        json.dump(data, f, indent=2)

# Default item images (SVG as base64)
DEFAULT_IMAGES = {
    'laptop': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iMTAiIHk9IjIwIiB3aWR0aD0iMTgwIiBoZWlnaHQ9IjgwIiByeD0iNSIgZmlsbD0iIzM0OThEQiIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIyMCIgeT0iMzAiIHdpZHRoPSIxNjAiIGhlaWdodD0iNjAiIHJ4PSIzIiBmaWxsPSIjMzQ5OERCIiBmaWxsLW9wYWNpdHk9IjAuMiIvPjx0ZXh0IHg9IjEwMCIgeT0iNzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMzNDk4REIiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+TEFQVE9QPC90ZXh0Pjwvc3ZnPg==',
    'phone': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iODAiIHk9IjEwIiB3aWR0aD0iNDAiIGhlaWdodD0iMTAwIiByeD0iNSIgZmlsbD0iIzJlY2M3MSIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI4NSIgeT0iMTUiIHdpZHRoPSIzMCIgaGVpZ2h0PSI5MCIgcng9IjMiIGZpbGw9IiMyZWNjNzEiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHRleHQgeD0iMTAwIiB5PSI3MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzJlY2M3MSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5QSE9ORTwvdGV4dD48L3N2Zz4=',
    'book': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNjAiIHk9IjIwIiB3aWR0aD0iODAiIGhlaWdodD0iODAiIHJ4PSIzIiBmaWxsPSIjZjM5YzEyIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxwYXRoIGQ9Ik02MCAyMCBDNzAgMTUgOTAgMTUgMTAwIDIwIEwxMDAgMTAwIEM5MCA5NSA3MCA5NSA2MCAxMDAgVjIwWiIgZmlsbD0iI2YzOWMxMiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjYwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZjM5YzEyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPkJPT0s8L3RleHQ+PC9zdmc+',
    'wallet': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNzAiIHk9IjMwIiB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHJ4PSI1IiBmaWxsPSIjZTc0YzNjIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjY1IiB5PSIyNSIgd2lkdGg9IjcwIiBoZWlnaHQ9IjcwIiByeD0iOCIgZmlsbD0iI2U3NGMzYyIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI3NSIgeT0iMzUiIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCIgcng9IjQiIGZpbGw9IiNlNzRjM2MiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHRleHQgeD0iMTAwIiB5PSI3MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2U3NGMzYyIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5XQUxMRVQ8L3RleHQ+PC9zdmc+',
    'keys': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iODAiIGN5PSI1MCIgcj0iMjAiIGZpbGw9IiM5NTdhNWEiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHJlY3QgeD0iOTUiIHk9IjQ1IiB3aWR0aD0iNDAiIGhlaWdodD0iMTAiIHJ4PSIyIiBmaWxsPSIjOTU3YTVhIiBmaWxsLW9wYWNpdHk9IjAuMyIvPjxyZWN0IHg9IjEwNSIgeT0iMzUiIHdpZHRoPSIyMCIgaGVpZ2h0PSIxMCIgcng9IjIiIGZpbGw9IiM5NTdhNWEiIGZpbGwtb3BhY2l0eT0iMC4zIi8+PHRleHQgeD0iMTAwIiB5PSI5MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzk1N2E1YSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5LRVlTPC90ZXh0Pjwvc3ZnPg==',
    'water-bottle': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iODUiIHk9IjIwIiB3aWR0aD0iMzAiIGhlaWdodD0iNzAiIHJ4PSI1IiBmaWxsPSIjMzQ5OERCIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjgwIiB5PSIxNSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjEwIiByeD0iMyIgZmlsbD0iIzM0OThEQiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzM0OThEQiIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5CT1RUTEU8L3RleHQ+PC9zdmc+',
    'bag': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNzAiIHk9IjMwIiB3aWR0aD0iNjAiIGhlaWdodD0iNTAiIHJ4PSI1IiBmaWxsPSIjZjM5YzEyIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9Ijc1IiB5PSIyMCIgd2lkdGg9IjUwIiBoZWlnaHQ9IjE1IiByeD0iMyIgZmlsbD0iI2YzOWMxMiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjkwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZjM5YzEyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiPkJBRzwvdGV4dD48L3N2Zz4=',
    'other': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTAwIiBjeT0iNjAiIHI9IjMwIiBmaWxsPSIjOTU3YTVhIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjx0ZXh0IHg9IjEwMCIgeT0iNjUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5NTdhNWEiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+SVRFTTwvdGV4dD48L3N2Zz4='
}

# HTML template with embedded CSS and JavaScript
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SmartCampus Lost & Found</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }

        :root {
            --primary: #3498db;
            --secondary: #2ecc71;
            --danger: #e74c3c;
            --warning: #f39c12;
            --dark: #2c3e50;
            --light: #ecf0f1;
            --gray: #7f8c8d;
        }

        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        /* Login Styles */
        .login-container {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 100vh;
        }

        .login-card {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            width: 100%;
            max-width: 400px;
        }

        .login-header {
            text-align: center;
            margin-bottom: 30px;
        }

        .login-header i {
            font-size: 48px;
            color: var(--primary);
            margin-bottom: 15px;
            display: block;
        }

        .login-header h1 {
            font-size: 24px;
            margin-bottom: 10px;
            color: var(--dark);
        }

        .form-group {
            margin-bottom: 20px;
        }

        .form-group label {
            display: block;
            margin-bottom: 8px;
            font-weight: 500;
            color: var(--dark);
        }

        .form-control {
            width: 100%;
            padding: 12px 15px;
            border: 2px solid #e1e8ed;
            border-radius: 8px;
            font-size: 16px;
            transition: all 0.3s ease;
        }

        .form-control:focus {
            border-color: var(--primary);
            outline: none;
            box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
        }

        .btn {
            padding: 12px 20px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            text-decoration: none;
        }

        .btn-primary {
            background: var(--primary);
            color: white;
        }

        .btn-primary:hover {
            background: #2980b9;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(52, 152, 219, 0.3);
        }

        .btn-success {
            background: var(--secondary);
            color: white;
        }

        .btn-danger {
            background: var(--danger);
            color: white;
        }

        .btn-warning {
            background: var(--warning);
            color: white;
        }

        .btn-block {
            width: 100%;
        }

        .demo-info {
            background: var(--light);
            border-radius: 8px;
            padding: 20px;
            margin-top: 20px;
            border-left: 4px solid var(--primary);
        }

        .demo-info h3 {
            color: var(--dark);
            margin-bottom: 10px;
            font-size: 14px;
        }

        /* Dashboard Styles */
        header {
            background: linear-gradient(135deg, var(--primary), #2980b9);
            color: white;
            padding: 15px 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            border-radius: 10px;
            margin-bottom: 20px;
        }

        .header-content {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .logo {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .logo i {
            font-size: 28px;
        }

        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }

        .user-avatar {
            width: 40px;
            height: 40px;
            background-color: white;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--primary);
            font-weight: bold;
        }

        .main-content {
            display: grid;
            grid-template-columns: 250px 1fr;
            gap: 20px;
        }

        .sidebar {
            background-color: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            height: fit-content;
        }

        .nav-menu {
            list-style: none;
        }

        .nav-item {
            margin-bottom: 10px;
        }

        .nav-link {
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 12px 15px;
            border-radius: 8px;
            color: var(--dark);
            text-decoration: none;
            transition: all 0.3s ease;
        }

        .nav-link:hover, .nav-link.active {
            background-color: var(--primary);
            color: white;
        }

        .content-area {
            background-color: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .section-title {
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 1px solid #eee;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }

        .stat-card {
            display: flex;
            align-items: center;
            gap: 15px;
            padding: 20px;
            background: white;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--primary);
        }

        .stat-icon {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            color: white;
        }

        .stat-icon.lost { background-color: var(--danger); }
        .stat-icon.found { background-color: var(--secondary); }
        .stat-icon.match { background-color: var(--warning); }
        .stat-icon.chat { background-color: var(--primary); }

        .quick-actions {
            margin-top: 30px;
        }

        .quick-actions h3 {
            margin-bottom: 15px;
        }

        .action-buttons {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
        }

        /* Items List */
        .items-list {
            display: grid;
            gap: 15px;
        }

        .item-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
            border-left: 4px solid var(--primary);
            display: flex;
            gap: 20px;
        }

        .item-image {
            width: 120px;
            height: 120px;
            border-radius: 8px;
            object-fit: cover;
            background: var(--light);
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--gray);
            font-size: 12px;
        }

        .item-content {
            flex: 1;
        }

        .item-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 10px;
        }

        .item-title {
            font-size: 18px;
            font-weight: 600;
        }

        .item-status {
            padding: 5px 10px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 500;
        }

        .status-lost { background: rgba(231, 76, 60, 0.2); color: var(--danger); }
        .status-found { background: rgba(46, 204, 113, 0.2); color: var(--secondary); }
        .status-match { background: rgba(52, 152, 219, 0.2); color: var(--primary); }

        .item-description {
            color: var(--gray);
            margin-bottom: 15px;
            line-height: 1.5;
        }

        .item-footer {
            display: flex;
            justify-content: space-between;
            align-items: center;
            font-size: 14px;
            color: var(--gray);
        }

        /* Image Upload */
        .image-upload {
            border: 2px dashed #ddd;
            border-radius: 8px;
            padding: 20px;
            text-align: center;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-bottom: 20px;
        }

        .image-upload:hover {
            border-color: var(--primary);
            background: rgba(52, 152, 219, 0.05);
        }

        .image-upload i {
            font-size: 48px;
            color: var(--gray);
            margin-bottom: 10px;
        }

        .image-preview {
            max-width: 200px;
            max-height: 150px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }

        /* Chat Styles */
        .chat-container {
            display: flex;
            flex-direction: column;
            height: 500px;
            border: 1px solid #eee;
            border-radius: 10px;
            overflow: hidden;
        }

        .chat-header {
            background-color: var(--primary);
            color: white;
            padding: 15px;
            text-align: center;
        }

        .chat-messages {
            flex: 1;
            padding: 15px;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .message {
            max-width: 70%;
            padding: 12px 15px;
            border-radius: 18px;
            position: relative;
        }

        .message-sent {
            align-self: flex-end;
            background-color: var(--primary);
            color: white;
            border-bottom-right-radius: 5px;
        }

        .message-received {
            align-self: flex-start;
            background-color: #f1f1f1;
            color: var(--dark);
            border-bottom-left-radius: 5px;
        }

        .message-time {
            font-size: 12px;
            margin-top: 5px;
            opacity: 0.7;
        }

        .chat-input {
            display: flex;
            padding: 15px;
            border-top: 1px solid #eee;
            background-color: #f9f9f9;
        }

        .chat-input input {
            flex: 1;
            padding: 12px 15px;
            border: 1px solid #ddd;
            border-radius: 20px;
            outline: none;
        }

        .chat-input button {
            margin-left: 10px;
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
        }

        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-color: rgba(0, 0, 0, 0.5);
            z-index: 1000;
            align-items: center;
            justify-content: center;
        }

        .modal-content {
            background-color: white;
            border-radius: 10px;
            width: 90%;
            max-width: 400px;
            padding: 25px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
        }

        .close-modal {
            background: none;
            border: none;
            font-size: 24px;
            cursor: pointer;
            color: var(--gray);
        }

        /* Notification */
        .notification {
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            z-index: 1000;
            display: flex;
            align-items: center;
            gap: 10px;
            transform: translateX(400px);
            transition: transform 0.3s ease;
        }

        .notification.show {
            transform: translateX(0);
        }

        .notification.success { background: var(--secondary); }
        .notification.error { background: var(--danger); }
        .notification.info { background: var(--primary); }

        /* Responsive */
        @media (max-width: 768px) {
            .main-content {
                grid-template-columns: 1fr;
            }
            .header-content {
                flex-direction: column;
                gap: 15px;
            }
            .stats-grid {
                grid-template-columns: 1fr;
            }
            .action-buttons {
                flex-direction: column;
            }
            .message {
                max-width: 85%;
            }
            .item-card {
                flex-direction: column;
            }
            .item-image {
                width: 100%;
                height: 150px;
            }
        }
    </style>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body>
    <div id="app">
        <!-- Content loaded by JavaScript -->
    </div>

    <!-- Change Password Modal -->
    <div class="modal" id="changePasswordModal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Change Password</h2>
                <button class="close-modal">&times;</button>
            </div>
            <form id="changePasswordForm">
                <div class="form-group">
                    <label>Current Password</label>
                    <input type="password" id="currentPassword" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>New Password</label>
                    <input type="password" id="newPassword" class="form-control" required>
                </div>
                <div class="form-group">
                    <label>Confirm New Password</label>
                    <input type="password" id="confirmPassword" class="form-control" required>
                </div>
                <button type="submit" class="btn btn-primary btn-block">Change Password</button>
            </form>
        </div>
    </div>

    <!-- Notification -->
    <div class="notification" id="notification">
        <i class="fas fa-check-circle"></i>
        <span id="notificationText">Welcome to SmartCampus!</span>
    </div>

    <script>
        let currentUser = null;
        let currentPage = 'login';
        let appData = {};
        let reportType = 'lost';

        // Utility functions
        function showNotification(message, type = 'success') {
            const notification = document.getElementById('notification');
            const notificationText = document.getElementById('notificationText');
            notificationText.textContent = message;
            notification.className = 'notification ' + type + ' show';
            setTimeout(() => notification.classList.remove('show'), 4000);
        }

        function navigateTo(page) {
            currentPage = page;
            render();
        }

        function setReportType(type) {
            reportType = type;
            const lostBtn = document.getElementById('lostBtn');
            const foundBtn = document.getElementById('foundBtn');
            if (lostBtn && foundBtn) {
                if (type === 'lost') {
                    lostBtn.className = 'btn btn-primary';
                    foundBtn.className = 'btn btn-success';
                } else {
                    lostBtn.className = 'btn btn-primary';
                    foundBtn.className = 'btn btn-success';
                }
            }
        }

        // Render functions
        function renderLogin() {
            return `
                <div class="login-container">
                    <div class="login-card">
                        <div class="login-header">
                            <i class="fas fa-laptop"></i>
                            <h1>SmartCampus Lost & Found</h1>
                            <p>Login to your account</p>
                        </div>
                        <form id="loginForm">
                            <div class="form-group">
                                <label>User ID</label>
                                <input type="text" id="userId" class="form-control" required placeholder="Enter your User ID">
                            </div>
                            <div class="form-group">
                                <label>Password</label>
                                <input type="password" id="password" class="form-control" required placeholder="Enter your password">
                            </div>
                            <button type="submit" class="btn btn-primary btn-block">
                                <i class="fas fa-sign-in-alt"></i> Login
                            </button>
                        </form>
                        <div class="demo-info">
                            <h3>Demo Credentials:</h3>
                            <p><strong>User IDs:</strong> 25CS001 to 25CS010</p>
                            <p><strong>Password:</strong> smartcampus123</p>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderDashboard() {
            const userLost = appData.lost_items.filter(item => item.user_id === currentUser).length;
            const userFound = appData.found_items.filter(item => item.user_id === currentUser).length;
            const matches = findMatches().length;
            const activeChats = Object.values(appData.chats).filter(chat => 
                chat.messages.some(msg => msg.sender_id === currentUser)
            ).length;

            return `
                <div class="container">
                    <header>
                        <div class="header-content">
                            <div class="logo">
                                <i class="fas fa-laptop"></i>
                                <h1>SmartCampus Lost & Found</h1>
                            </div>
                            <div class="user-info">
                                <div class="user-avatar">${appData.users[currentUser].name[0]}</div>
                                <div>
                                    <div>${appData.users[currentUser].name}</div>
                                    <div style="font-size: 12px; opacity: 0.8;">ID: ${currentUser}</div>
                                </div>
                                <button class="btn btn-warning" onclick="showChangePassword()">
                                    <i class="fas fa-key"></i> Change Password
                                </button>
                                <button class="btn btn-danger" onclick="logout()">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </button>
                            </div>
                        </div>
                    </header>

                    <div class="main-content">
                        <div class="sidebar">
                            <ul class="nav-menu">
                                <li class="nav-item"><a href="#" class="nav-link active" onclick="navigateTo('dashboard')"><i class="fas fa-home"></i> Dashboard</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('report')"><i class="fas fa-plus-circle"></i> Report Item</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('lost')"><i class="fas fa-search"></i> Lost Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('found')"><i class="fas fa-check-circle"></i> Found Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('matches')"><i class="fas fa-handshake"></i> Matches</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('chats')"><i class="fas fa-comments"></i> Messages</a></li>
                            </ul>
                        </div>

                        <div class="content-area">
                            <div class="section-title">
                                <h2>Dashboard</h2>
                            </div>
                            <div class="stats-grid">
                                <div class="stat-card">
                                    <div class="stat-icon lost"><i class="fas fa-search"></i></div>
                                    <div class="stat-info"><h3>${userLost}</h3><p>Lost Items</p></div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-icon found"><i class="fas fa-check-circle"></i></div>
                                    <div class="stat-info"><h3>${userFound}</h3><p>Found Items</p></div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-icon match"><i class="fas fa-handshake"></i></div>
                                    <div class="stat-info"><h3>${matches}</h3><p>Potential Matches</p></div>
                                </div>
                                <div class="stat-card">
                                    <div class="stat-icon chat"><i class="fas fa-comments"></i></div>
                                    <div class="stat-info"><h3>${activeChats}</h3><p>Active Chats</p></div>
                                </div>
                            </div>
                            <div class="quick-actions">
                                <h3>Quick Actions</h3>
                                <div class="action-buttons">
                                    <button class="btn btn-primary" onclick="navigateTo('report')"><i class="fas fa-plus"></i> Report Lost Item</button>
                                    <button class="btn btn-success" onclick="navigateTo('report')"><i class="fas fa-plus"></i> Report Found Item</button>
                                    <button class="btn btn-primary" onclick="navigateTo('matches')"><i class="fas fa-handshake"></i> View Matches</button>
                                </div>
                            </div>
                            ${matches > 0 ? `<div style="margin-top: 20px; padding: 15px; background: #e8f4fd; border-radius: 8px; border-left: 4px solid var(--primary);">
                                <h4>🎉 You have ${matches} potential matches!</h4>
                                <p>Check the Matches section to connect with finders and recover your items.</p>
                            </div>` : ''}
                        </div>
                    </div>
                </div>
            `;
        }

        function renderReport() {
            return `
                <div class="container">
                    <header>
                        <div class="header-content">
                            <div class="logo">
                                <i class="fas fa-laptop"></i>
                                <h1>Report Item - SmartCampus</h1>
                            </div>
                            <div class="user-info">
                                <div class="user-avatar">${appData.users[currentUser].name[0]}</div>
                                <div>${appData.users[currentUser].name}</div>
                                <button class="btn btn-danger" onclick="logout()">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </button>
                            </div>
                        </div>
                    </header>

                    <div class="main-content">
                        <div class="sidebar">
                            <ul class="nav-menu">
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('dashboard')"><i class="fas fa-home"></i> Dashboard</a></li>
                                <li class="nav-item"><a href="#" class="nav-link active" onclick="navigateTo('report')"><i class="fas fa-plus-circle"></i> Report Item</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('lost')"><i class="fas fa-search"></i> Lost Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('found')"><i class="fas fa-check-circle"></i> Found Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('matches')"><i class="fas fa-handshake"></i> Matches</a></li>
                            </ul>
                        </div>

                        <div class="content-area">
                            <div class="section-title">
                                <h2>Report ${reportType === 'lost' ? 'Lost' : 'Found'} Item</h2>
                            </div>
                            
                            <form id="reportForm">
                                <div class="form-group">
                                    <label>Report Type</label>
                                    <div style="display: flex; gap: 10px;">
                                        <button type="button" class="btn ${reportType === 'lost' ? 'btn-primary' : 'btn-primary'}" id="lostBtn" onclick="setReportType('lost')">Report Lost Item</button>
                                        <button type="button" class="btn ${reportType === 'found' ? 'btn-success' : 'btn-success'}" id="foundBtn" onclick="setReportType('found')">Report Found Item</button>
                                    </div>
                                </div>
                                
                                <div class="form-group">
                                    <label>Item Type</label>
                                    <select id="itemType" class="form-control" required>
                                        <option value="">Select item type</option>
                                        <option value="laptop">Laptop</option>
                                        <option value="phone">Phone</option>
                                        <option value="book">Book</option>
                                        <option value="wallet">Wallet</option>
                                        <option value="keys">Keys</option>
                                        <option value="water-bottle">Water Bottle</option>
                                        <option value="bag">Bag</option>
                                        <option value="other">Other</option>
                                    </select>
                                </div>
                                
                                <div class="form-group">
                                    <label>Item Description</label>
                                    <textarea id="description" class="form-control" rows="4" placeholder="Provide a detailed description of the item..." required></textarea>
                                </div>
                                
                                <div class="form-group">
                                    <label>Location</label>
                                    <input type="text" id="location" class="form-control" placeholder="Where did you lose/find the item?" required>
                                </div>
                                
                                <div class="form-group">
                                    <label>Date</label>
                                    <input type="date" id="date" class="form-control" required>
                                </div>

                                <div class="form-group">
                                    <label>Item Image (Optional)</label>
                                    <div class="image-upload" onclick="document.getElementById('imageInput').click()">
                                        <i class="fas fa-cloud-upload-alt"></i>
                                        <p>Click to upload an image of the item</p>
                                        <small>Supported formats: JPG, PNG, SVG</small>
                                        <img id="imagePreview" class="image-preview" alt="Image preview">
                                    </div>
                                    <input type="file" id="imageInput" accept="image/*" style="display: none" onchange="previewImage(event)">
                                </div>
                                
                                <button type="submit" class="btn btn-primary btn-block">Submit Report</button>
                            </form>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderLostItems() {
            const userItems = appData.lost_items.filter(item => item.user_id === currentUser);
            const itemsHtml = userItems.length > 0 ? userItems.map(item => `
                <div class="item-card">
                    <div class="item-image">
                        <img src="${item.image || getDefaultImage(item.type)}" alt="${item.type}" style="width: 100%; height: 100%; border-radius: 8px;">
                    </div>
                    <div class="item-content">
                        <div class="item-header">
                            <div class="item-title">${item.type.charAt(0).toUpperCase() + item.type.slice(1)}</div>
                            <div class="item-status status-lost">Lost</div>
                        </div>
                        <div class="item-description">${item.description}</div>
                        <div class="item-footer">
                            <div>
                                <strong>Location:</strong> ${item.location} | 
                                <strong>Date:</strong> ${item.date}
                            </div>
                        </div>
                    </div>
                </div>
            `).join('') : '<p>No lost items reported yet.</p>';

            return `
                <div class="container">
                    <header>
                        <div class="header-content">
                            <div class="logo">
                                <i class="fas fa-laptop"></i>
                                <h1>Lost Items - SmartCampus</h1>
                            </div>
                            <div class="user-info">
                                <div class="user-avatar">${appData.users[currentUser].name[0]}</div>
                                <div>${appData.users[currentUser].name}</div>
                                <button class="btn btn-danger" onclick="logout()">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </button>
                            </div>
                        </div>
                    </header>

                    <div class="main-content">
                        <div class="sidebar">
                            <ul class="nav-menu">
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('dashboard')"><i class="fas fa-home"></i> Dashboard</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('report')"><i class="fas fa-plus-circle"></i> Report Item</a></li>
                                <li class="nav-item"><a href="#" class="nav-link active" onclick="navigateTo('lost')"><i class="fas fa-search"></i> Lost Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('found')"><i class="fas fa-check-circle"></i> Found Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('matches')"><i class="fas fa-handshake"></i> Matches</a></li>
                            </ul>
                        </div>

                        <div class="content-area">
                            <div class="section-title">
                                <h2>Your Lost Items</h2>
                                <button class="btn btn-primary" onclick="navigateTo('report')">
                                    <i class="fas fa-plus"></i> Report New Item
                                </button>
                            </div>
                            <div class="items-list">
                                ${itemsHtml}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        function renderMatches() {
            const matches = findMatches();
            const matchesHtml = matches.length > 0 ? matches.map(match => `
                <div class="item-card">
                    <div class="item-image">
                        <img src="${match.found_item.image || getDefaultImage(match.found_item.type)}" alt="${match.found_item.type}" style="width: 100%; height: 100%; border-radius: 8px;">
                    </div>
                    <div class="item-content">
                        <div class="item-header">
                            <div class="item-title">${match.lost_item.type.charAt(0).toUpperCase() + match.lost_item.type.slice(1)} Match Found!</div>
                            <div class="item-status status-match">Match</div>
                        </div>
                        <div class="item-description">
                            <p><strong>Your Item:</strong> ${match.lost_item.description}</p>
                            <p><strong>Found Item:</strong> ${match.found_item.description}</p>
                            <p><strong>Found by:</strong> ${match.found_item.user_name} (${match.found_item.user_id})</p>
                        </div>
                        <div class="item-footer">
                            <button class="btn btn-primary" onclick="startChat('${match.found_item.user_id}', '${match.lost_item.id}', '${match.found_item.id}')">
                                <i class="fas fa-comments"></i> Start Chat
                            </button>
                        </div>
                    </div>
                </div>
            `).join('') : '<p>No matches found yet. Report your lost items to find matches!</p>';

            return `
                <div class="container">
                    <header>
                        <div class="header-content">
                            <div class="logo">
                                <i class="fas fa-laptop"></i>
                                <h1>Matches - SmartCampus</h1>
                            </div>
                            <div class="user-info">
                                <div class="user-avatar">${appData.users[currentUser].name[0]}</div>
                                <div>${appData.users[currentUser].name}</div>
                                <button class="btn btn-danger" onclick="logout()">
                                    <i class="fas fa-sign-out-alt"></i> Logout
                                </button>
                            </div>
                        </div>
                    </header>

                    <div class="main-content">
                        <div class="sidebar">
                            <ul class="nav-menu">
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('dashboard')"><i class="fas fa-home"></i> Dashboard</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('report')"><i class="fas fa-plus-circle"></i> Report Item</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('lost')"><i class="fas fa-search"></i> Lost Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link" onclick="navigateTo('found')"><i class="fas fa-check-circle"></i> Found Items</a></li>
                                <li class="nav-item"><a href="#" class="nav-link active" onclick="navigateTo('matches')"><i class="fas fa-handshake"></i> Matches</a></li>
                            </ul>
                        </div>

                        <div class="content-area">
                            <div class="section-title">
                                <h2>Potential Matches</h2>
                            </div>
                            <div class="items-list">
                                ${matchesHtml}
                            </div>
                        </div>
                    </div>
                </div>
            `;
        }

        // Helper functions
        function findMatches() {
            const matches = [];
            const userLost = appData.lost_items.filter(item => item.user_id === currentUser);
            
            userLost.forEach(lostItem => {
                appData.found_items.forEach(foundItem => {
                    if (foundItem.user_id !== currentUser && isPotentialMatch(lostItem, foundItem)) {
                        matches.push({lost_item: lostItem, found_item: foundItem});
                    }
                });
            });
            return matches;
        }

        function isPotentialMatch(lost, found) {
            if (lost.type !== found.type) return false;
            const lostWords = lost.description.toLowerCase().split(/\\s+/);
            const foundWords = found.description.toLowerCase().split(/\\s+/);
            const commonWords = lostWords.filter(word => foundWords.includes(word) && word.length > 3);
            return commonWords.length >= 1;
        }

        function getDefaultImage(itemType) {
            const defaultImages = {
                'laptop': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iMTAiIHk9IjIwIiB3aWR0aD0iMTgwIiBoZWlnaHQ9IjgwIiByeD0iNSIgZmlsbD0iIzM0OThEQiIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSIyMCIgeT0iMzAiIHdpZHRoPSIxNjAiIGhlaWdodD0iNjAiIHJ4PSIzIiBmaWxsPSIjMzQ5OERCIiBmaWxsLW9wYWNpdHk9IjAuMiIvPjx0ZXh0IHg9IjEwMCIgeT0iNzAiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiMzNDk4REIiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+TEFQVE9QPC90ZXh0Pjwvc3ZnPg==',
                'phone': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iODAiIHk9IjEwIiB3aWR0aD0iNDAiIGhlaWdodD0iMTAwIiByeD0iNSIgZmlsbD0iIzJlY2M3MSIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI4NSIgeT0iMTUiIHdpZHRoPSIzMCIgaGVpZ2h0PSI5MCIgcng9IjMiIGZpbGw9IiMyZWNjNzEiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHRleHQgeD0iMTAwIiB5PSI3MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzJlY2M3MSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5QSE9ORTwvdGV4dD48L3N2Zz4=',
                'book': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNjAiIHk9IjIwIiB3aWR0aD0iODAiIGhlaWdodD0iODAiIHJ4PSIzIiBmaWxsPSIjZjM5YzEyIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxwYXRoIGQ9Ik02MCAyMCBDNzAgMTUgOTAgMTUgMTAwIDIwIEwxMDAgMTAwIEM5MCA5NSA3MCA5NSA2MCAxMDAgVjIwWiIgZmlsbD0iI2YzOWMxMiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjYwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZjM5YzEyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTQiPkJPT0s8L3RleHQ+PC9zdmc+',
                'wallet': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNzAiIHk9IjMwIiB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHJ4PSI1IiBmaWxsPSIjZTc0YzNjIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjY1IiB5PSIyNSIgd2lkdGg9IjcwIiBoZWlnaHQ9IjcwIiByeD0iOCIgZmlsbD0iI2U3NGMzYyIgZmlsbC1vcGFjaXR5PSIwLjEiLz48cmVjdCB4PSI3NSIgeT0iMzUiIHdpZHRoPSI1MCIgaGVpZ2h0PSI1MCIgcng9IjQiIGZpbGw9IiNlNzRjM2MiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHRleHQgeD0iMTAwIiB5PSI3MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iI2U3NGMzYyIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5XQUxMRVQ8L3RleHQ+PC9zdmc+',
                'keys': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iODAiIGN5PSI1MCIgcj0iMjAiIGZpbGw9IiM5NTdhNWEiIGZpbGwtb3BhY2l0eT0iMC4yIi8+PHJlY3QgeD0iOTUiIHk9IjQ1IiB3aWR0aD0iNDAiIGhlaWdodD0iMTAiIHJ4PSIyIiBmaWxsPSIjOTU3YTVhIiBmaWxsLW9wYWNpdHk9IjAuMyIvPjxyZWN0IHg9IjEwNSIgeT0iMzUiIHdpZHRoPSIyMCIgaGVpZ2h0PSIxMCIgcng9IjIiIGZpbGw9IiM5NTdhNWEiIGZpbGwtb3BhY2l0eT0iMC4zIi8+PHRleHQgeD0iMTAwIiB5PSI5MCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzk1N2E1YSIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5LRVlTPC90ZXh0Pjwvc3ZnPg==',
                'water-bottle': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iODUiIHk9IjIwIiB3aWR0aD0iMzAiIGhlaWdodD0iNzAiIHJ4PSI1IiBmaWxsPSIjMzQ5OERCIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9IjgwIiB5PSIxNSIgd2lkdGg9IjQwIiBoZWlnaHQ9IjEwIiByeD0iMyIgZmlsbD0iIzM0OThEQiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjEwMCIgdGV4dC1hbmNob3I9Im1pZGRsZSIgZmlsbD0iIzM0OThEQiIgZm9udC1mYW1pbHk9IkFyaWFsIiBmb250LXNpemU9IjEyIj5CT1RUTEU8L3RleHQ+PC9zdmc+',
                'bag': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PHJlY3QgeD0iNzAiIHk9IjMwIiB3aWR0aD0iNjAiIGhlaWdodD0iNTAiIHJ4PSI1IiBmaWxsPSIjZjM5YzEyIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjxyZWN0IHg9Ijc1IiB5PSIyMCIgd2lkdGg9IjUwIiBoZWlnaHQ9IjE1IiByeD0iMyIgZmlsbD0iI2YzOWMxMiIgZmlsbC1vcGFjaXR5PSIwLjIiLz48dGV4dCB4PSIxMDAiIHk9IjkwIiB0ZXh0LWFuY2hvcj0ibWlkZGxlIiBmaWxsPSIjZjM5YzEyIiBmb250LWZhbWlseT0iQXJpYWwiIGZvbnQtc2l6ZT0iMTIiPkJBRzwvdGV4dD48L3N2Zz4=',
                'other': 'data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjEyMCIgdmlld0JveD0iMCAwIDIwMCAxMjAiIGZpbGw9Im5vbmUiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGNpcmNsZSBjeD0iMTAwIiBjeT0iNjAiIHI9IjMwIiBmaWxsPSIjOTU3YTVhIiBmaWxsLW9wYWNpdHk9IjAuMSIvPjx0ZXh0IHg9IjEwMCIgeT0iNjUiIHRleHQtYW5jaG9yPSJtaWRkbGUiIGZpbGw9IiM5NTdhNWEiIGZvbnQtZmFtaWx5PSJBcmlhbCIgZm9udC1zaXplPSIxNCI+SVRFTTwvdGV4dD48L3N2Zz4='
            };
            return defaultImages[itemType] || defaultImages['other'];
        }

        function previewImage(event) {
            const input = event.target;
            const preview = document.getElementById('imagePreview');
            
            if (input.files && input.files[0]) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    preview.src = e.target.result;
                    preview.style.display = 'block';
                }
                reader.readAsDataURL(input.files[0]);
            }
        }

        function showChangePassword() {
            document.getElementById('changePasswordModal').style.display = 'flex';
        }

        function logout() {
            currentUser = null;
            currentPage = 'login';
            render();
            showNotification('Logged out successfully', 'success');
        }

        // Event handlers
        async function handleLogin(e) {
            e.preventDefault();
            const userId = document.getElementById('userId').value;
            const password = document.getElementById('password').value;

            if (appData.users[userId] && appData.users[userId].password === password) {
                currentUser = userId;
                showNotification(`Welcome ${appData.users[userId].name}!`, 'success');
                navigateTo('dashboard');
            } else {
                showNotification('Invalid credentials. Use demo users: 25CS001-25CS010, password: smartcampus123', 'error');
            }
        }

        async function handleReport(e) {
            e.preventDefault();
            const itemType = document.getElementById('itemType').value;
            const description = document.getElementById('description').value;
            const location = document.getElementById('location').value;
            const date = document.getElementById('date').value;
            const imageInput = document.getElementById('imageInput');
            
            if (!itemType || !description || !location || !date) {
                return showNotification('Please fill all required fields', 'error');
            }

            let imageData = getDefaultImage(itemType);
            if (imageInput.files && imageInput.files[0]) {
                imageData = await readFileAsDataURL(imageInput.files[0]);
            }

            const newItem = {
                id: Date.now().toString(),
                user_id: currentUser,
                user_name: appData.users[currentUser].name,
                type: itemType,
                description: description,
                location: location,
                date: date,
                image: imageData,
                status: 'active',
                created_at: new Date().toISOString()
            };

            if (reportType === 'lost') {
                appData.lost_items.push(newItem);
            } else {
                appData.found_items.push(newItem);
            }

            // Save to server
            const response = await fetch('/report', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    currentUser: currentUser,
                    type: reportType,
                    item_type: itemType,
                    description: description,
                    location: location,
                    date: date,
                    image: imageData
                })
            });

            if (response.ok) {
                showNotification('Item reported successfully!', 'success');
                navigateTo('dashboard');
            } else {
                showNotification('Error reporting item', 'error');
            }
        }

        function readFileAsDataURL(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader();
                reader.onload = () => resolve(reader.result);
                reader.onerror = reject;
                reader.readAsDataURL(file);
            });
        }

        function startChat(foundUserId, lostItemId, foundItemId) {
            const chatId = 'chat_' + lostItemId + '_' + foundItemId;
            if (!appData.chats[chatId]) {
                appData.chats[chatId] = {messages: []};
            }
            navigateTo('chat');
            showNotification('Chat feature would open here! In full version, you can message the finder.', 'info');
        }

        async function handleChangePassword(e) {
            e.preventDefault();
            const currentPass = document.getElementById('currentPassword').value;
            const newPass = document.getElementById('newPassword').value;
            const confirmPass = document.getElementById('confirmPassword').value;

            if (appData.users[currentUser].password !== currentPass) {
                return showNotification('Current password is incorrect', 'error');
            }
            if (newPass !== confirmPass) {
                return showNotification('New passwords do not match', 'error');
            }
            if (appData.password_change_attempts && appData.password_change_attempts[currentUser]) {
                return showNotification('You have already used your password change attempt', 'error');
            }

            appData.users[currentUser].password = newPass;
            appData.users[currentUser].password_changed = true;
            
            if (!appData.password_change_attempts) {
                appData.password_change_attempts = {};
            }
            appData.password_change_attempts[currentUser] = true;

            // Save to server
            const response = await fetch('/change_password', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({
                    currentUser: currentUser,
                    current_password: currentPass,
                    new_password: newPass
                })
            });

            if (response.ok) {
                document.getElementById('changePasswordModal').style.display = 'none';
                document.getElementById('changePasswordForm').reset();
                showNotification('Password changed successfully!', 'success');
            }
        }

        // Main render function
        function render() {
            let content = '';
            switch(currentPage) {
                case 'login': content = renderLogin(); break;
                case 'dashboard': content = renderDashboard(); break;
                case 'report': content = renderReport(); break;
                case 'lost': content = renderLostItems(); break;
                case 'matches': content = renderMatches(); break;
                default: content = renderDashboard();
            }

            document.getElementById('app').innerHTML = content;
            
            // Attach event listeners
            setTimeout(() => {
                const loginForm = document.getElementById('loginForm');
                if (loginForm) loginForm.onsubmit = handleLogin;
                
                const reportForm = document.getElementById('reportForm');
                if (reportForm) reportForm.onsubmit = handleReport;

                const changePasswordForm = document.getElementById('changePasswordForm');
                if (changePasswordForm) changePasswordForm.onsubmit = handleChangePassword;

                // Set today's date for report form
                const dateField = document.getElementById('date');
                if (dateField) {
                    const today = new Date().toISOString().split('T')[0];
                    dateField.value = today;
                }

                // Close modal handlers
                const closeModal = document.querySelector('.close-modal');
                if (closeModal) {
                    closeModal.onclick = () => {
                        document.getElementById('changePasswordModal').style.display = 'none';
                    };
                }
            }, 100);
        }

        // Close modal when clicking outside
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                e.target.style.display = 'none';
            }
        });

        // Initialize app
        async function init() {
            try {
                const response = await fetch('/data');
                appData = await response.json();
                render();
                showNotification('Use 25CS001 to 25CS010 with password: smartcampus123', 'info');
            } catch (error) {
                showNotification('Error loading data. Please refresh the page.', 'error');
            }
        }

        init();
    </script>
</body>
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
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response_data).encode())

def main():
    init_data()
    PORT = 8000
    with socketserver.TCPServer(("", PORT), SmartCampusHandler) as httpd:
        print("🚀 SmartCampus Lost & Found Portal Started!")
        print("📍 Access: http://localhost:8000")
        print("👤 Demo Users: 25CS001 to 25CS010")
        print("🔑 Password: smartcampus123")
        print("📸 Features: Image Upload • Smart Matching • Live Chat • Password Management")
        print("🛑 Press Ctrl+C to stop")
        print("="*50)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped!")

if __name__ == "__main__":
    main()

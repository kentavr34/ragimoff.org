#!/usr/bin/env python3
"""Discover LightRAG API endpoints"""

import requests

api_key = 'chesscoin_rag_secret_2026'
base_url = 'http://185.203.116.131:9622'

headers = {
    'X-API-Key': api_key,
    'Content-Type': 'application/json'
}

print('Discovering LightRAG API endpoints...\n')

# Common LightRAG endpoints
endpoints = [
    ('GET', '/'),
    ('GET', '/health'),
    ('GET', '/api'),
    ('GET', '/docs'),
    ('GET', '/openapi.json'),
    ('POST', '/query'),
    ('POST', '/insert'),
    ('POST', '/api/query'),
    ('POST', '/api/insert'),
    ('GET', '/graphs'),
    ('POST', '/graphs'),
    ('PUT', '/graphs'),
]

for method, path in endpoints:
    try:
        if method == 'GET':
            r = requests.get(f'{base_url}{path}', headers=headers, timeout=2)
        else:
            r = requests.post(f'{base_url}{path}', json={'label': 'test'}, headers=headers, timeout=2)
        
        status_text = f'{r.status_code}'
        if r.status_code < 400:
            status_text += ' ✓'
            
        print(f'{method:4} {path:20} -> {status_text}')
        
        # Show response for successful queries
        if r.status_code < 300 and len(r.text) < 200:
            print(f'      Response: {r.text[:100]}')
            
    except requests.exceptions.Timeout:
        print(f'{method:4} {path:20} -> Timeout')
    except requests.exceptions.ConnectionError:
        print(f'{method:4} {path:20} -> Connection refused')
    except Exception as e:
        print(f'{method:4} {path:20} -> {type(e).__name__}')

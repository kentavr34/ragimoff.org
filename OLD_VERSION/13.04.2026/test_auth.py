#!/usr/bin/env python3
"""Test different authentication methods for LightRAG"""

import requests

api_key = 'chesscoin_rag_secret_2026'
url = 'http://185.203.116.131:9622/graphs'

print('Testing different auth formats...\n')

tests = [
    ('Bearer token', {'Authorization': f'Bearer {api_key}'}),
    ('X-API-Key header', {'X-API-Key': api_key}),
]

for name, headers in tests:
    try:
        r = requests.get(url, headers=headers, timeout=3)
        print(f'{name}: {r.status_code} - {r.text[:100]}')
    except Exception as e:
        print(f'{name}: Error - {e}')

# Test with query parameter
try:
    r = requests.get(f'{url}?api_key={api_key}', timeout=3)
    print(f'Query param: {r.status_code} - {r.text[:100]}')
except Exception as e:
    print(f'Query param: Error - {e}')

# Test without auth
try:
    r = requests.get(url, timeout=3)
    print(f'No auth: {r.status_code} - {r.text[:100]}')
except Exception as e:
    print(f'No auth: Error - {e}')

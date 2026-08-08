#!/usr/bin/env python3
"""Test LightRAG API with correct auth and label"""

import requests
import json

api_key = 'chesscoin_rag_secret_2026'
url = 'http://185.203.116.131:9622/graphs'

headers = {'X-API-Key': api_key}

print('Testing with X-API-Key header and label=ragimoff.org...\n')

try:
    r = requests.get(f'{url}?label=ragimoff.org', headers=headers, timeout=5)
    print(f'Status: {r.status_code}')
    
    if r.status_code == 200:
        print('✓ Connection successful!')
        try:
            data = r.json()
            print(f'Response type: {type(data).__name__}')
            if isinstance(data, dict):
                print(f'Keys: {list(data.keys())}')
            elif isinstance(data, list):
                print(f'Items: {len(data)}')
        except:
            print(f'Response (raw): {r.text[:300]}')
    else:
        print(f'Status message: {r.text[:300]}')
        
except Exception as e:
    print(f'Error: {type(e).__name__}: {e}')

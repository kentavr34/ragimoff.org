#!/usr/bin/env python3
"""Test LightRAG API - POST data to /graphs"""

import requests
import json

api_key = 'chesscoin_rag_secret_2026'
base_url = 'http://185.203.116.131:9622'

headers = {
    'X-API-Key': api_key,
    'Content-Type': 'application/json'
}

# Test data for ragimoff.org project
data = {
    'label': 'ragimoff.org',
    'nodes': [
        {
            'id': 'ragimoff_site',
            'type': 'project',
            'label': 'ragimoff.org'
        }
    ],
    'edges': [],
    'source_long_form': 'Static website - Psychology services and education'
}

print('Attempting to register ragimoff.org project in LightRAG...\n')
print(f'API URL: {base_url}/graphs')
print(f'Using X-API-Key authentication\n')

try:
    # Try POST to /graphs
    r = requests.post(
        f'{base_url}/graphs',
        json=data,
        headers=headers,
        timeout=5
    )
    print(f'POST /graphs - Status: {r.status_code}')
    print(f'Response: {r.text[:300]}')
    
except Exception as e:
    print(f'Error: {e}')

print('\n' + '='*50)

# Try alternative endpoints  
endpoints = ['/api/graphs', '/graph', '/project']

for endpoint in endpoints:
    try:
        r = requests.post(
            f'{base_url}{endpoint}',
            json={'label': 'ragimoff.org'},
            headers=headers,
            timeout=3
        )
        print(f'POST {endpoint}: {r.status_code}')
    except:
        print(f'POST {endpoint}: No connection')

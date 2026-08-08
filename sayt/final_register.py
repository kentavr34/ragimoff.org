#!/usr/bin/env python3
"""Register ragimoff.org project in LightRAG"""

import requests
import json
from datetime import datetime

api_key = 'chesscoin_rag_secret_2026'
base_url = 'http://185.203.116.131:9622'

headers = {
    'X-API-Key': api_key,
    'Content-Type': 'application/json'
}

project_name = 'ragimoff_site_2026'
label = 'ragimoff.org'

print(f'Registering project "{label}" in LightRAG...\n')

# Prepare project data
project_data = {
    'text': 'Project: ragimoff.org - Static website for psychology services and education (Azerbaijan)',
    'nodes': [
        {
            'id': 'ragimoff_site',
            'type': 'project',
            'label': 'ragimoff.org',
            'properties': {
                'name': 'ragimoff.org',
                'description': 'Static website - Psychology services and education',
                'url': 'https://ragimoff.org',
                'created': datetime.now().isoformat(),
                'type': 'static-website',
                'status': 'active'
            }
        },
        {
            'id': 'tech_html5',
            'type': 'technology',
            'label': 'HTML5'
        },
        {
            'id': 'tech_css3',
            'type': 'technology',
            'label': 'CSS3'
        },
        {
            'id': 'tech_js',
            'type': 'technology',
            'label': 'JavaScript'
        }
    ],
    'edges': [
        {'source': 'ragimoff_site', 'target': 'tech_html5', 'type': 'uses_technology'},
        {'source': 'ragimoff_site', 'target': 'tech_css3', 'type': 'uses_technology'},
        {'source': 'ragimoff_site', 'target': 'tech_js', 'type': 'uses_technology'}
    ]
}

# Try to insert the data
try:
    url = f'{base_url}/insert/{project_name}'
    print(f'POST {url}')
    print(f'Payload: {len(str(project_data))} bytes\n')
    
    response = requests.post(
        url,
        json=project_data,
        headers=headers,
        timeout=10
    )
    
    print(f'Status: {response.status_code}')
    
    if response.status_code in [200, 201]:
        print('✓ Project registered successfully!')
        print(f'Response: {response.text[:300]}')
    else:
        print(f'Response: {response.text[:500]}')
        
except Exception as e:
    print(f'Error: {e}')

# Also try with just source_long_form (simpler format)
print('\n' + '='*50)
print('\nAlternate format test:\n')

simple_data = {
    'text': 'ragimoff.org Project Registration - Static website for psychology services and education',
    'nodes': [
        {
            'id': 'ragimoff_site',
            'label': 'ragimoff.org'
        }
    ]
}

try:
    response = requests.post(
        f'{base_url}/insert/{project_name}',
        json=simple_data,
        headers=headers,
        timeout=10
    )
    
    print(f'Simple format - Status: {response.status_code}')
    if response.status_code < 400:
        print('✓ Success with simple format!')
    print(f'Response: {response.text[:300]}')
    
except Exception as e:
    print(f'Error: {e}')

#!/usr/bin/env python3
"""Register ragimoff.org project in LightRAG service"""

import requests
import json
from datetime import datetime
import sys

api_key = 'chesscoin_rag_secret_2026'
# Try direct URL first, fall back to proxy
base_url_direct = 'http://185.203.116.131:9622'
base_url_proxy = 'https://chesscoin.app/lightrag'
base_url = base_url_direct  # Start with direct

headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {api_key}'
}

project_data = {
    'project_id': 'ragimoff_site_2026',
    'project_name': 'ragimoff.org',
    'project_label': 'ragimoff.org',
    'timestamp': datetime.now().isoformat(),
    'description': 'Static website - Psychology services and education (Azerbaijan)',
    'url': 'https://ragimoff.org',
    'type': 'static-website',
    'status': 'active',
    'metadata': {
        'framework': 'HTML5/CSS3/JavaScript (no build)',
        'deploment': 'Netlify',
        'design_system': 'Mobile-first, Playfair+Lato, Navy+Gold',
        'pages': '25+ (blog, services, education, diplomas)'
    }
}

# Format for LightRAG graph data
graph_payload = {
    'nodes': [
        {
            'id': 'ragimoff_site_2026',
            'type': 'project',
            'name': 'ragimoff.org',
            'description': project_data['description'],
            'labels': ['project', 'production', 'website']
        }
    ],
    'relationships': []
}

print("Registering ragimoff.org in LightRAG...")
print(f"API Key: {api_key[:20]}...")
print(f"Direct URL: {base_url_direct}")
print(f"Proxy URL: {base_url_proxy}")
print(f"Project: {project_data['project_name']}")
print()

# Try multiple endpoints and URLs
endpoints = [
    ('/graphs', base_url_direct, graph_payload),
    ('/api/graphs', base_url_direct, graph_payload),
    ('/graphs', base_url_proxy, graph_payload),
    ('/api/graphs', base_url_proxy, graph_payload),
]

success = False
for endpoint, url, payload in endpoints:
    try:
        full_url = f'{url.rstrip("/")}{endpoint}'
        print(f"Trying: POST {full_url}")
        
        response = requests.post(
            full_url,
            json=payload,
            headers=headers,
            timeout=5
        )
        
        print(f"  Status: {response.status_code}")
        if response.text:
            print(f"  Response: {response.text[:200]}")
        
        if response.status_code in [200, 201]:
            print("\n✓ Project successfully registered!")
            success = True
            break
            
    except requests.exceptions.Timeout:
        print(f"  Timeout")
    except requests.exceptions.ConnectionError:
        print(f"  Connection failed")
    except Exception as e:
        print(f"  Error: {type(e).__name__}")

if not success:
    print("\n⚠ Could not connect to any LightRAG endpoint")
    print("But project metadata is ready to be logged")
    print("Try from browser: https://chesscoin.app/rag/")

sys.exit(0)

#!/usr/bin/env python3
"""Analyze OpenAPI schema for query format"""

import requests
import json

api_key = 'chesscoin_rag_secret_2026'
headers = {'X-API-Key': api_key}

print('Fetching OpenAPI schema...\n')

try:
    r = requests.get('http://185.203.116.131:9622/openapi.json', headers=headers, timeout=5)
    
    if r.status_code == 200:
        schema = r.json()
        
        print('Available endpoints:')
        if 'paths' in schema:
            for path in sorted(schema['paths'].keys()):
                methods = schema['paths'][path]
                method_list = [m.upper() for m in methods.keys() if m.upper() in ['GET', 'POST', 'PUT', 'DELETE']]
                print(f'  {path:30} -> {", ".join(method_list)}')
        
        print('\n' + '='*50)
        print('\nQuery endpoint details:')
        
        if '/query' in schema['paths'] and 'post' in schema['paths']['/query']:
            post_schema = schema['paths']['/query']['post']
            
            if 'requestBody' in post_schema:
                print('\nRequest Body Schema:')
                rb = post_schema['requestBody']
                if 'content' in rb and 'application/json' in rb['content']:
                    json_schema = rb['content']['application/json']['schema']
                    print(json.dumps(json_schema, indent=2)[:500])
            
            if 'parameters' in post_schema:
                print('\nQuery Parameters:')
                for param in post_schema['parameters']:
                    print(f'  - {param.get("name")}: {param.get("schema", {}).get("type")}')
    else:
        print(f'Failed to fetch schema: {r.status_code}')
        
except Exception as e:
    print(f'Error: {e}')

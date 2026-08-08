#!/usr/bin/env python3
"""
LightRAG Integration for ragimoff.org
Track project changes and maintain development history in LightRAG
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List

class RagimoffLightRAGClient:
    """Client for logging ragimoff.org changes to LightRAG"""
    
    API_KEY = 'chesscoin_rag_secret_2026'
    BASE_URL = 'http://185.203.116.131:9622'
    PROJECT_ID = 'ragimoff_site_2026'
    PROJECT_LABEL = 'ragimoff.org'
    
    def __init__(self):
        self.headers = {
            'X-API-Key': self.API_KEY,
            'Content-Type': 'application/json'
        }
    
    def log_change(self,
                   change_type: str,
                   description: str,
                   files_modified: Optional[List[str]] = None) -> bool:
        """
        Log a change to the project
        
        Args:
            change_type: Type of change (feature, bugfix, design, refactor, doc)
            description: Detailed description of the change
            files_modified: List of affected files
        
        Returns:
            True if successful
        """
        timestamp = datetime.now().isoformat()
        
        # Build the text description
        text_content = f"[{change_type.upper()}] {description}\nTimestamp: {timestamp}"
        
        if files_modified:
            text_content += f"\nFiles: {', '.join(files_modified)}"
        
        payload = {
            'text': text_content,
            'nodes': [
                {
                    'id': f'change_{timestamp.replace(":", "-")}',
                    'label': f'{change_type}: {description[:50]}',
                    'type': 'change',
                    'properties': {
                        'type': change_type,
                        'description': description,
                        'timestamp': timestamp,
                        'files': files_modified or []
                    }
                },
                {
                    'id': 'ragimoff_site',
                    'label': 'ragimoff.org'
                }
            ],
            'edges': [
                {
                    'source': f'change_{timestamp.replace(":", "-")}',
                    'target': 'ragimoff_site',
                    'type': 'modifies'
                }
            ]
        }
        
        try:
            response = requests.post(
                f'{self.BASE_URL}/insert/{self.PROJECT_ID}',
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('status') == 'success':
                    track_id = result.get('track_id', 'unknown')
                    print(f'✓ {change_type.upper()}: {description}')
                    print(f'  Track ID: {track_id}')
                    return True
            
            print(f'✗ Failed to log change: {response.status_code}')
            return False
            
        except Exception as e:
            print(f'✗ Error: {e}')
            return False
    
    def log_feature(self, name: str, description: str, files: Optional[List[str]] = None) -> bool:
        """Log a new feature"""
        return self.log_change('feature', f'{name}: {description}', files)
    
    def log_bugfix(self, issue: str, fix: str, files: Optional[List[str]] = None) -> bool:
        """Log a bug fix"""
        return self.log_change('bugfix', f'Fixed {issue}: {fix}', files)
    
    def log_design_update(self, update: str, components: Optional[List[str]] = None) -> bool:
        """Log a design system update"""
        text = update
        if components:
            text += f' ({", ".join(components)})'
        return self.log_change('design', text, None)
    
    def test_connection(self) -> bool:
        """Test connection to LightRAG"""
        try:
            r = requests.get(
                f'{self.BASE_URL}/health',
                headers=self.headers,
                timeout=5
            )
            if r.status_code == 200:
                health = r.json()
                projects = health.get('projects', [])
                print(f'✓ Connected to LightRAG')
                print(f'  Active projects: {", ".join(projects)}')
                return True
        except Exception as e:
            print(f'✗ Connection failed: {e}')
        return False


# Example usage
if __name__ == '__main__':
    client = RagimoffLightRAGClient()
    
    print('Testing LightRAG connection for ragimoff.org...\n')
    
    if client.test_connection():
        print('\nLogging sample changes...\n')
        
        # Log initial registration
        client.log_feature(
            'LightRAG Integration',
            'Integrated project with LightRAG for change history tracking',
            ['lightrag_client.py', 'register_project.py']
        )
        
        print('\n✓ ragimoff.org is now connected to LightRAG')
        print('  View at: https://chesscoin.app/rag/')
    else:
        print('\nFailed to connect to LightRAG')

#!/usr/bin/env python3
"""
CLI tool for logging changes to ragimoff.org in LightRAG
Usage: python log_changes.py <type> <description> [--files file1,file2,...]
"""

import sys
import argparse
from lightrag_client import RagimoffLightRAGClient


def main():
    parser = argparse.ArgumentParser(
        description='Log changes to ragimoff.org project history in LightRAG',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python log_changes.py feature "Mobile menu fix" --files index.html,shared.js
  python log_changes.py bugfix "Fixed hero image on mobile" --files index.html
  python log_changes.py design "Unified 8px spacing grid"
  python log_changes.py refactor "Removed duplicate CSS" --files shared.css
  python log_changes.py docs "Updated DESIGN_MASTERPLAN.md"
        '''
    )
    
    parser.add_argument('type', 
                       choices=['feature', 'bugfix', 'design', 'refactor', 'docs'],
                       help='Type of change',
                       metavar='TYPE')
    
    parser.add_argument('description', 
                       help='Description of the change',
                       metavar='DESCRIPTION')
    
    parser.add_argument('--files', '-f', 
                       help='Comma-separated list of modified files',
                       default='',
                       metavar='FILES')
    
    args = parser.parse_args()
    
    # Parse files
    files = None
    if args.files:
        files = [f.strip() for f in args.files.split(',')]
    
    # Create client and log
    client = RagimoffLightRAGClient()
    
    print(f'Logging {args.type} to ragimoff.org...\n')
    
    # Log based on type
    if args.type == 'feature':
        success = client.log_feature(
            name=args.description.split(':')[0],
            description=args.description,
            files=files
        )
    elif args.type == 'bugfix':
        success = client.log_bugfix(
            issue='See description',
            fix=args.description,
            files=files
        )
    elif args.type == 'design':
        success = client.log_design_update(
            update=args.description,
            components=files
        )
    else:
        # Generic refactor or docs
        success = client.log_change(
            change_type=args.type,
            description=args.description,
            files_modified=files
        )
    
    if success:
        print(f'\n✓ Successfully logged to LightRAG')
        print(f'  View at: https://chesscoin.app/rag/')
        sys.exit(0)
    else:
        print(f'\n✗ Failed to log change')
        sys.exit(1)


if __name__ == '__main__':
    main()

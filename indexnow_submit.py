#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
IndexNow / WebSub / Ping script for faster search engine indexing.
Supports: IndexNow (Bing, Yandex, Seznam), Google Indexing API, WebSub hubs.
"""
import sys, io, os, json, hashlib, hmac, time, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = os.path.dirname(os.path.abspath(__file__))

# Configuration
KEY_FILE = os.path.join(ROOT, 'indexnow_key.txt')
KEY_URL = 'https://ragimoff.org/indexnow_key.txt'  # Publicly accessible key location
HOST = 'ragimoff.org'

# IndexNow endpoints
INDEXNOW_ENDPOINTS = [
    'https://api.indexnow.org/indexnow',  # Bing, Yandex, Seznam
    'https://www.bing.com/indexnow',      # Bing direct
    'https://yandex.com/indexnow',        # Yandex direct
]

# WebSub hubs (for real-time push)
WEBSUB_HUBS = [
    'https://pubsubhubbub.appspot.com/',  # Google's hub
    'https://push.superfeedr.com/',       # Superfeedr
]

# Sitemap URLs to ping
SITEMAPS = [
    'https://ragimoff.org/sitemap.xml',
    'https://ragimoff.org/klinik-psixiatriya/sitemap.xml',
]

def get_or_create_key():
    """Get or create IndexNow key"""
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'r') as f:
            return f.read().strip()
    
    # Generate new key (128-bit hex)
    key = hashlib.sha256(os.urandom(32)).hexdigest()[:64]
    with open(KEY_FILE, 'w') as f:
        f.write(key)
    print(f'Generated new IndexNow key: {key}')
    print(f'Make sure it\'s accessible at: {KEY_URL}')
    return key

def build_url_list(limit=10000):
    """Build list of URLs to submit from sitemap and known pages"""
    urls = []
    
    # Main sitemap
    sitemap_path = os.path.join(ROOT, 'sitemap.xml')
    if os.path.exists(sitemap_path):
        import xml.etree.ElementTree as ET
        try:
            tree = ET.parse(sitemap_path)
            root = tree.getroot()
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for url_elem in root.findall('sm:url', ns):
                loc = url_elem.find('sm:loc', ns)
                if loc is not None and loc.text:
                    urls.append(loc.text)
        except Exception as e:
            print(f'Warning: Could not parse sitemap.xml: {e}')
    
    # Book sitemap
    book_sitemap = os.path.join(ROOT, 'klinik-psixiatriya', 'sitemap.xml')
    if os.path.exists(book_sitemap):
        try:
            tree = ET.parse(book_sitemap)
            root = tree.getroot()
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            for url_elem in root.findall('sm:url', ns):
                loc = url_elem.find('sm:loc', ns)
                if loc is not None and loc.text:
                    urls.append(loc.text)
        except Exception as e:
            print(f'Warning: Could not parse book sitemap: {e}')
    
    # Add known important pages if not in sitemap
    important_pages = [
        'https://ragimoff.org/',
        'https://ragimoff.org/index.html',
        'https://ragimoff.org/haqqimda.html',
        'https://ragimoff.org/tehsil.html',
        'https://ragimoff.org/xidmetler.html',
        'https://ragimoff.org/depressiya.html',
        'https://ragimoff.org/panik-ataklar.html',
        'https://ragimoff.org/sosial-fobiya.html',
        'https://ragimoff.org/enurez.html',
        'https://ragimoff.org/aile-terapiyasi.html',
        'https://ragimoff.org/aile-terapiyasi-usaq.html',
        'https://ragimoff.org/klinik-psixiatriya/',
        'https://ragimoff.org/en/',
        'https://ragimoff.org/ru/',
    ]
    for p in important_pages:
        if p not in urls:
            urls.append(p)
    
    return urls[:limit]

def submit_indexnow(urls, key):
    """Submit URLs to IndexNow endpoints"""
    if not urls:
        print('No URLs to submit')
        return
    
    payload = {
        'host': HOST,
        'key': key,
        'keyLocation': KEY_URL,
        'urlList': urls
    }
    
    import urllib.request, urllib.error
    
    for endpoint in INDEXNOW_ENDPOINTS:
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(payload).encode('utf-8'),
                headers={'Content-Type': 'application/json; charset=utf-8'},
                method='POST'
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = resp.read().decode('utf-8')
                print(f'  IndexNow {endpoint}: {resp.status} - {result}')
        except urllib.error.HTTPError as e:
            print(f'  IndexNow {endpoint}: HTTP {e.code} - {e.read().decode()}')
        except Exception as e:
            print(f'  IndexNow {endpoint}: Error - {e}')

def ping_sitemaps():
    """Ping search engines with sitemap URLs"""
    ping_endpoints = [
        'https://www.google.com/ping?sitemap=',
        'https://www.bing.com/ping?sitemap=',
        'https://webmaster.yandex.com/ping?sitemap=',
    ]
    
    import urllib.request
    
    for sitemap in SITEMAPS:
        for endpoint in ping_endpoints:
            try:
                url = endpoint + urllib.parse.quote(sitemap, safe='')
                with urllib.request.urlopen(url, timeout=15) as resp:
                    print(f'  Ping {endpoint}{sitemap}: {resp.status}')
            except Exception as e:
                print(f'  Ping {endpoint}{sitemap}: Error - {e}')

def publish_websub(urls):
    """Publish to WebSub hubs"""
    import urllib.request, urllib.parse
    
    for hub in WEBSUB_HUBS:
        for url in urls:
            try:
                data = urllib.parse.urlencode({
                    'hub.mode': 'publish',
                    'hub.url': url
                }).encode('utf-8')
                
                req = urllib.request.Request(
                    hub,
                    data=data,
                    headers={'Content-Type': 'application/x-www-form-urlencoded'},
                    method='POST'
                )
                with urllib.request.urlopen(req, timeout=15) as resp:
                    print(f'  WebSub {hub} for {url}: {resp.status}')
            except Exception as e:
                print(f'  WebSub {hub} for {url}: Error - {e}')

def google_indexing_api(urls):
    """
    Submit to Google Indexing API (requires service account credentials).
    Set GOOGLE_INDEXING_CREDENTIALS env var to path of service account JSON.
    """
    creds_path = os.environ.get('GOOGLE_INDEXING_CREDENTIALS')
    if not creds_path or not os.path.exists(creds_path):
        print('Google Indexing API: Skipped (no credentials)')
        return
    
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        
        SCOPES = ['https://www.googleapis.com/auth/indexing']
        credentials = service_account.Credentials.from_service_account_file(
            creds_path, scopes=SCOPES)
        service = build('indexing', 'v3', credentials=credentials)
        
        for url in urls:
            try:
                body = {'url': url, 'type': 'URL_UPDATED'}
                service.urlNotifications().publish(body=body).execute()
                print(f'  Google Indexing API: {url} - OK')
            except Exception as e:
                print(f'  Google Indexing API: {url} - Error: {e}')
    except ImportError:
        print('Google Indexing API: Skipped (google-api-python-client not installed)')
    except Exception as e:
        print(f'Google Indexing API: Error - {e}')

def main():
    print('=== IndexNow / WebSub / Ping Script ===\n')
    
    # Get key
    key = get_or_create_key()
    print(f'Using IndexNow key: {key[:16]}...\n')
    
    # Build URL list
    print('Building URL list from sitemaps...')
    urls = build_url_list()
    print(f'Found {len(urls)} URLs\n')
    
    # Submit to IndexNow
    print('Submitting to IndexNow...')
    submit_indexnow(urls, key)
    print()
    
    # Ping sitemaps
    print('Pinging sitemaps...')
    ping_sitemaps()
    print()
    
    # Publish to WebSub
    print('Publishing to WebSub hubs...')
    publish_websub(urls[:100])  # Limit for WebSub
    print()
    
    # Google Indexing API (if configured)
    print('Google Indexing API...')
    google_indexing_api(urls[:200])  # Daily limit ~200
    print()
    
    print('=== Done ===')

if __name__ == '__main__':
    main()
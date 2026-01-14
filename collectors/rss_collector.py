"""
zkHetz RSS Collector
Collects from all configured RSS sources.
Deduplication by URL prevents re-adding existing items.
"""

import feedparser
import requests
import ssl
import certifi
from datetime import datetime
from config.sources import get_all_sources, get_sources_by_category, SourceCategory
from utils.db import save_raw_items

# Fix SSL for Mac
ssl._create_default_https_context = lambda: ssl.create_default_context(cafile=certifi.where())

# Settings
TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"


def get_source_type(source) -> str:
    """Determine source type for dashboard display based on source name/url."""
    name_lower = source.name.lower()
    url_lower = source.url.lower()
    
    # Government sources
    if any(x in name_lower for x in ['cisa', 'ncsc', 'cert', 'bsi', 'anssi', 'enisa', 'nist', 'fbi', 'acsc', 'jpcert', 'jvn', 'ipa', 'incd', 'krcert', 'cccs']):
        return "GOVERNMENT"
    if any(x in url_lower for x in ['.gov', '.go.jp', '.go.kr', '.gc.ca', 'europa.eu', 'bund.de']):
        return "GOVERNMENT"
    
    # Academic sources
    if any(x in name_lower for x in ['arxiv', 'ieee', 'acm', 'usenix', 'iacr']):
        return "ACADEMIC"
    
    # Non-profit / Think tanks
    if any(x in name_lower for x in ['eff', 'epic', 'fido', 'carnegie', 'brookings', 'rand', 'cfr', 'chatham', 'atlantic council', 'csis', 'belfer', 'stimson', 'access now']):
        return "NON-PROFIT"
    
    # Independent security researchers
    if any(x in name_lower for x in ['krebs', 'schneier', 'troy hunt', 'graham cluley', 'risky business', 'lawfare']):
        return "INDEPENDENT"
    
    # Commercial/vendor sources
    if any(x in name_lower for x in ['crowdstrike', 'mandiant', 'microsoft', 'google', 'kaspersky', 'sophos', 
                                      'sentinelone', 'palo alto', 'unit 42', 'cisco', 'talos', 'fortinet', 
                                      'checkpoint', 'check point', 'trend micro', 'cloudflare', 'aws', 
                                      'hashicorp', 'proofpoint', 'recorded future', 'eset', 'bitdefender',
                                      'zscaler', 'dragos', 'volexity', 'red canary', 'binary defense',
                                      'intezer', 'huntress', 'cybereason', 'flashpoint', 'intel471',
                                      'sekoia', 'ahnlab', 'thales', 'aware', 'onelogin', 'jumpcloud',
                                      'curity', 'auth0', 'lac security', 'malwarebytes', 'tenable',
                                      'qualys', 'elastic', 'sans']):
        return "COMMERCIAL"
    
    # Media sources
    if any(x in name_lower for x in ['times', 'herald', 'post', 'news', 'bleeping', 'hacker news',
                                      'dark reading', 'securityweek', 'threatpost', 'infosecurity',
                                      'sc media', 'register', 'wired', 'ars technica', 'verge',
                                      'techcrunch', 'mit technology', 'spectrum', 'crunchbase',
                                      'finsmes', 'alleywatch', 'eu-startups', 'silicon', 'euractiv',
                                      'politico', 'zdnet', 'bloter', 'daily nk', 'nk news',
                                      'the record', 'cyberscoop', 'fedscoop', 'nextgov', 'statescoop',
                                      'meritalk', 'fcw', 'foreign affairs', 'war on the rocks',
                                      'gdpr today', 'dataguidance', 'privacy laws', 'calcalist',
                                      'ynet', 'i24', 'israel defense', 'nocamels']):
        return "MEDIA"
    
    return "MEDIA"


def fetch_feed_content(url):
    """Fetch feed content using requests with proper headers."""
    headers = {
        "User-Agent": USER_AGENT,
        "Accept": "application/rss+xml, application/xml, application/atom+xml, text/xml, */*",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
    }
    
    response = requests.get(url, headers=headers, timeout=TIMEOUT, verify=True)
    response.raise_for_status()
    return response.content


def fetch_single_feed(source):
    """Fetch items from a single RSS feed."""
    print(f"  Fetching: {source.name}...", end=" ", flush=True)
    
    try:
        # Fetch with requests first (better headers)
        content = fetch_feed_content(source.url)
        feed = feedparser.parse(content)
        
        if feed.bozo and not feed.entries:
            # Try direct feedparser as fallback
            feed = feedparser.parse(source.url)
            if feed.bozo and not feed.entries:
                print(f"FAIL (parse error)")
                return []
        
        if not feed.entries:
            print(f"EMPTY")
            return []
        
        items = []
        source_type = get_source_type(source)
        
        for entry in feed.entries[:15]:
            
            published = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published = datetime(*entry.published_parsed[:6]).isoformat()
                except:
                    pass
            elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                try:
                    published = datetime(*entry.updated_parsed[:6]).isoformat()
                except:
                    pass
            
            content = entry.get("summary", "") or entry.get("description", "")
            if hasattr(entry, 'content') and entry.content:
                content = entry.content[0].get('value', content)
            
            items.append({
                "title": entry.get("title", "No title")[:500],
                "content": content[:5000],
                "url": entry.get("link", ""),
                "source_name": source.name,
                "source_type": source_type,
                "category": source.category.value,
                "published_at": published,
                "collected_at": datetime.now().isoformat()
            })
        
        print(f"OK ({len(items)} items)")
        return items
    
    except requests.exceptions.Timeout:
        print(f"TIMEOUT")
        return []
    except requests.exceptions.HTTPError as e:
        print(f"HTTP {e.response.status_code}")
        return []
    except Exception as e:
        print(f"FAIL ({type(e).__name__})")
        return []


def collect_all_feeds(category_filter=None, priority_filter=None):
    """Collect from all configured feeds."""
    
    if category_filter:
        try:
            cat = SourceCategory(category_filter)
            sources = get_sources_by_category(cat)
        except ValueError:
            print(f"Unknown category: {category_filter}")
            return []
    else:
        sources = get_all_sources()
    
    if priority_filter:
        sources = [s for s in sources if s.priority <= priority_filter]
    
    print("=" * 60)
    print("zkHetz RSS Collector")
    print("=" * 60)
    print(f"Sources: {len(sources)} | Timeout: {TIMEOUT}s")
    if category_filter:
        print(f"Category: {category_filter}")
    print("=" * 60 + "\n")
    
    all_items = []
    success_count = 0
    fail_count = 0
    
    for source in sources:
        items = fetch_single_feed(source)
        if items:
            all_items.extend(items)
            success_count += 1
        else:
            fail_count += 1
    
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"OK: {success_count} | Failed: {fail_count} | Items: {len(all_items)}")
    
    if all_items:
        saved = save_raw_items(all_items)
        print(f"Saved to database: {saved} (new items, duplicates skipped)")
    
    print("=" * 60)
    
    return all_items


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="zkHetz RSS Collector")
    parser.add_argument("--category", "-c", type=str, help="Collect specific category only")
    parser.add_argument("--priority", "-p", type=int, help="Collect priority <= N only")
    args = parser.parse_args()
    
    collect_all_feeds(
        category_filter=args.category,
        priority_filter=args.priority
    )
"""
Test file for failed RSS sources - potential correct URLs
Run: python test_feeds.py

Based on search results, these are potential working URLs for sources that failed.
"""

import feedparser
import requests

TIMEOUT = 15
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"

# Format: (name, new_url_to_test)
FEEDS_TO_TEST = [
    # UK NCSC - found new API URLs
    ("UK NCSC News", "https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml"),
    ("UK NCSC Blog", "https://www.ncsc.gov.uk/api/1/services/v1/blog-post-rss-feed.xml"),
    ("UK NCSC All", "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml"),
    
    # CERT-EU - try different URL formats
    ("CERT-EU Old Format", "http://cert.europa.eu/rss?type=category&id=CERT-LatestNews&language=all&duplicates=false"),
    
    # BSI Germany - try alternative URLs
    ("BSI CERT-Bund WID", "https://wid.cert-bund.de/content/public/securityAdvisory/rss"),
    ("BSI Buerger CERT", "https://www.bsi.bund.de/SiteGlobals/Functions/RSSFeed/RSSNewsfessBSIFB/RSSNewsfeed_BuergerCERT.xml"),
    
    # FBI - try different paths
    ("FBI News", "https://www.fbi.gov/news/rss.xml"),
    
    # Cisco Talos - found working URL
    ("Cisco Talos Feedburner", "https://feeds.feedburner.com/feedburner/Talos"),
    ("Cisco Security Blog", "https://feeds.feedburner.com/CiscoBlogSecurity"),
    
    # Sophos - found working URL
    ("Sophos News", "https://news.sophos.com/en-us/feed/"),
    ("Sophos Threat Research", "https://news.sophos.com/en-us/category/threat-research/feed/"),
    
    # Proofpoint
    ("Proofpoint Threat Insight", "https://www.proofpoint.com/us/blog/threat-insight/feed"),
    
    # Volexity
    ("Volexity Blog", "https://www.volexity.com/blog/feed/"),
    
    # Dragos
    ("Dragos Feed", "https://www.dragos.com/feed/"),
    
    # Zscaler
    ("Zscaler ThreatLabz RSS", "https://www.zscaler.com/blogs/security-research/rss.xml"),
    
    # Bitdefender
    ("Bitdefender Labs", "https://www.bitdefender.com/blog/labs/feed/"),
    
    # Binary Defense
    ("Binary Defense", "https://www.binarydefense.com/feed/"),
    
    # SC Media / SC World
    ("SC World", "https://www.scworld.com/feed"),
    
    # Sekoia
    ("Sekoia Blog", "https://blog.sekoia.io/feed/"),
    
    # USENIX
    ("USENIX Blog", "https://www.usenix.org/blog/feed"),
    
    # Lawfare
    ("Lawfare RSS", "https://www.lawfaremedia.org/rss.xml"),
    
    # The Verge
    ("The Verge All", "https://www.theverge.com/rss/index.xml"),
    
    # Google Cloud
    ("Google Cloud Blog", "https://cloudblog.withgoogle.com/rss/"),
    
    # Brookings
    ("Brookings Cyber", "https://www.brookings.edu/topic/cybersecurity/feed/"),
    
    # Chatham House
    ("Chatham House", "https://www.chathamhouse.org/rss"),
    
    # Times of Israel
    ("Times of Israel All", "https://www.timesofisrael.com/feed/"),
    
    # Euractiv
    ("Euractiv All", "https://www.euractiv.com/feed/"),
    
    # Korea sources
    ("Boan News Security", "https://www.boannews.com/media/news_rss.xml"),
    ("IT Chosun", "https://it.chosun.com/site/data/rss/rss.xml"),
    ("KISA/KrCERT", "https://www.boho.or.kr/kr/rss/secNotice.do"),
    
    # Japan sources
    ("IPA Security", "https://www.ipa.go.jp/security/announce/rss.xml"),
    ("LAC Security", "https://www.lac.co.jp/lacwatch/rss.xml"),
    
    # EU-Startups
    ("EU-Startups", "https://eu-startups.com/feed/"),
    
    # AlleyWatch
    ("AlleyWatch", "https://alleywatch.com/feed/"),
    
    # Additional sources to add
    ("Troy Hunt", "https://www.troyhunt.com/rss/"),
    ("Graham Cluley", "https://grahamcluley.com/feed/"),
    ("Naked Security", "https://news.sophos.com/en-us/category/naked-security/feed/"),
    ("SANS ISC", "https://isc.sans.edu/rssfeed.xml"),
    ("Malwarebytes Labs", "https://www.malwarebytes.com/blog/feed"),
    ("WeLiveSecurity", "https://www.welivesecurity.com/en/rss/feed/"),
    ("Tenable Blog", "https://www.tenable.com/blog/feed"),
    ("Qualys Blog", "https://blog.qualys.com/feed"),
    ("Rapid7 Blog", "https://www.rapid7.com/blog/feed/"),
    ("NCC Group", "https://research.nccgroup.com/feed/"),
    ("Palo Alto Threat Brief", "https://www.paloaltonetworks.com/blog/feed/"),
    ("Elastic Security", "https://www.elastic.co/security-labs/rss/feed.xml"),
    ("38 North (NK)", "https://www.38north.org/feed/"),
    ("Haaretz Tech", "https://www.haaretz.com/srv/haaretz-latest-headlines-technology"),
    ("NoCamels Israel", "https://nocamels.com/feed/"),
    ("Korea Herald IT", "https://www.koreaherald.com/rss/028000000000.xml"),
]


def test_feed(name, url):
    """Test if a feed URL works."""
    try:
        headers = {"User-Agent": USER_AGENT}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        
        if response.status_code != 200:
            return False, f"HTTP {response.status_code}"
        
        feed = feedparser.parse(response.content)
        
        if feed.bozo and not feed.entries:
            return False, "Parse error"
        
        if not feed.entries:
            return False, "Empty"
        
        return True, f"OK ({len(feed.entries)} items)"
    
    except requests.exceptions.Timeout:
        return False, "Timeout"
    except Exception as e:
        return False, str(type(e).__name__)


def main():
    print("=" * 70)
    print("Testing Failed RSS Sources - Potential Correct URLs")
    print("=" * 70 + "\n")
    
    results = []
    
    for name, url in FEEDS_TO_TEST:
        print(f"Testing: {name}...", end=" ", flush=True)
        
        success, message = test_feed(name, url)
        status = "✓" if success else "✗"
        print(f"{status} {message}")
        
        results.append((name, url, success, message))
    
    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    working = [(n, u) for n, u, s, m in results if s]
    failed = [(n, u, m) for n, u, s, m in results if not s]
    
    print(f"\nWORKING: {len(working)} | FAILED: {len(failed)}")
    
    print(f"\n--- WORKING ({len(working)}) ---")
    for name, url in working:
        print(f"  {name}: {url}")
    
    print(f"\n--- FAILED ({len(failed)}) ---")
    for name, url, msg in failed:
        print(f"  {name}: {msg}")


if __name__ == "__main__":
    main()
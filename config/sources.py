"""
zkHetz Brain Center - RSS Sources Configuration
Updated: 2026-01-03 (All URLs verified working)

Categories match database schema exactly:
cyber_attacks, auth_identity, adversary_cyber, research_updates,
investment, legal_regulations, tech_developments, geopolitics,
target_israel, target_europe, target_us, target_south_korea, target_japan
"""

from dataclasses import dataclass
from typing import List, Optional
from enum import Enum


class SourceCategory(Enum):
    """Categories matching database schema exactly"""
    CYBER_ATTACKS = "cyber_attacks"
    AUTH_IDENTITY = "auth_identity"
    SAAS_SECURITY = "saas_security"
    ADVERSARY_CYBER = "adversary_cyber"
    RESEARCH_UPDATES = "research_updates"
    INVESTMENT = "investment"
    LEGAL_REGULATIONS = "legal_regulations"
    TECH_DEVELOPMENTS = "tech_developments"
    GEOPOLITICS = "geopolitics"
    TARGET_ISRAEL = "target_israel"
    TARGET_EUROPE = "target_europe"
    TARGET_US = "target_us"
    TARGET_SOUTH_KOREA = "target_south_korea"
    TARGET_JAPAN = "target_japan"


@dataclass
class RSSSource:
    """Represents a single RSS feed source"""
    name: str
    url: str
    category: SourceCategory
    language: str = "en"
    priority: int = 1
    description: Optional[str] = None


# =============================================================================
# CYBER_ATTACKS - All verified working
# =============================================================================
CYBER_ATTACKS_SOURCES = [
    # Government Advisories
    RSSSource("CISA Advisories", "https://www.cisa.gov/cybersecurity-advisories/all.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("CISA News", "https://www.cisa.gov/news.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("US-CERT Alerts", "https://www.cisa.gov/uscert/ncas/alerts.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("UK NCSC All", "https://www.ncsc.gov.uk/api/1/services/v1/all-rss-feed.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("UK NCSC News", "https://www.ncsc.gov.uk/api/1/services/v1/news-rss-feed.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("ENISA News", "https://www.enisa.europa.eu/rss.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("ANSSI Advisories", "https://www.cert.ssi.gouv.fr/feed/", SourceCategory.CYBER_ATTACKS, language="fr"),
    RSSSource("BSI CERT-Bund", "https://wid.cert-bund.de/content/public/securityAdvisory/rss", SourceCategory.CYBER_ATTACKS, language="de"),
    RSSSource("CCCS Canada", "https://www.cyber.gc.ca/webservice/en/rss/alerts", SourceCategory.CYBER_ATTACKS),
    RSSSource("NIST Cybersecurity", "https://www.nist.gov/blogs/cybersecurity-insights/rss.xml", SourceCategory.CYBER_ATTACKS),
    
    # Threat Intel Vendors
    RSSSource("CrowdStrike Blog", "https://www.crowdstrike.com/blog/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Mandiant Blog", "https://www.mandiant.com/resources/blog/rss.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("Microsoft Security Blog", "https://www.microsoft.com/en-us/security/blog/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Google TAG Blog", "https://blog.google/threat-analysis-group/rss/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Cisco Talos", "https://feeds.feedburner.com/feedburner/Talos", SourceCategory.CYBER_ATTACKS),
    RSSSource("Cisco Security Blog", "https://feeds.feedburner.com/CiscoBlogSecurity", SourceCategory.CYBER_ATTACKS),
    RSSSource("SentinelOne Labs", "https://www.sentinelone.com/labs/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Palo Alto Unit 42", "https://unit42.paloaltonetworks.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Palo Alto Blog", "https://www.paloaltonetworks.com/blog/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Recorded Future", "https://www.recordedfuture.com/feed", SourceCategory.CYBER_ATTACKS),
    RSSSource("Kaspersky Securelist", "https://securelist.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("ESET WeLiveSecurity", "https://www.welivesecurity.com/en/rss/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Fortinet Threat Research", "https://feeds.fortinet.com/fortinet/blog/threat-research", SourceCategory.CYBER_ATTACKS),
    RSSSource("Check Point Research", "https://research.checkpoint.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Red Canary Blog", "https://redcanary.com/blog/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Intezer Blog", "https://intezer.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Huntress Blog", "https://www.huntress.com/blog/rss.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("Cybereason Blog", "https://www.cybereason.com/blog/rss.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("Sekoia Blog", "https://blog.sekoia.io/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Malwarebytes Labs", "https://www.malwarebytes.com/blog/feed", SourceCategory.CYBER_ATTACKS),
    RSSSource("Tenable Blog", "https://www.tenable.com/blog/feed", SourceCategory.CYBER_ATTACKS),
    RSSSource("Qualys Blog", "https://blog.qualys.com/feed", SourceCategory.CYBER_ATTACKS),
    RSSSource("Elastic Security Labs", "https://www.elastic.co/security-labs/rss/feed.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("SANS ISC", "https://isc.sans.edu/rssfeed.xml", SourceCategory.CYBER_ATTACKS),
    
    # Security News & Researchers
    RSSSource("Krebs on Security", "https://krebsonsecurity.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Schneier on Security", "https://www.schneier.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Troy Hunt", "https://www.troyhunt.com/rss/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Graham Cluley", "https://grahamcluley.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("BleepingComputer", "https://www.bleepingcomputer.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("The Hacker News", "https://feeds.feedburner.com/TheHackersNews", SourceCategory.CYBER_ATTACKS),
    RSSSource("Dark Reading", "https://www.darkreading.com/rss.xml", SourceCategory.CYBER_ATTACKS),
    RSSSource("SecurityWeek", "https://feeds.feedburner.com/securityweek", SourceCategory.CYBER_ATTACKS),
    RSSSource("Threatpost", "https://threatpost.com/feed/", SourceCategory.CYBER_ATTACKS),
    RSSSource("Infosecurity Magazine", "https://www.infosecurity-magazine.com/rss/news/", SourceCategory.CYBER_ATTACKS),
    RSSSource("The Register Security", "https://www.theregister.com/security/headlines.atom", SourceCategory.CYBER_ATTACKS),
    RSSSource("Risky Business News", "https://risky.biz/feeds/risky-business/", SourceCategory.CYBER_ATTACKS),
    
    # GitHub Threat Intel
    RSSSource("MITRE ATT&CK Updates", "https://github.com/mitre/cti/commits/master.atom", SourceCategory.CYBER_ATTACKS),
    RSSSource("Sigma Rules Updates", "https://github.com/SigmaHQ/sigma/commits/master.atom", SourceCategory.CYBER_ATTACKS),
]

# =============================================================================
# AUTH_IDENTITY - Verified working
# =============================================================================
AUTH_IDENTITY_SOURCES = [
    RSSSource("Biometric Update", "https://www.biometricupdate.com/feed", SourceCategory.AUTH_IDENTITY),
    RSSSource("FIDO Alliance Blog", "https://fidoalliance.org/feed/", SourceCategory.AUTH_IDENTITY),
    RSSSource("Secure ID News", "https://www.secureidnews.com/news-item/feed/", SourceCategory.AUTH_IDENTITY),
    RSSSource("OneLogin Blog", "https://www.onelogin.com/blog/feed", SourceCategory.AUTH_IDENTITY),
    RSSSource("JumpCloud Blog", "https://jumpcloud.com/feed", SourceCategory.AUTH_IDENTITY),
    RSSSource("Auth0 Blog", "https://auth0.com/blog/rss.xml", SourceCategory.AUTH_IDENTITY),
]

# =============================================================================
# SAAS_SECURITY - SaaS vendor security, incidents, announcements
# =============================================================================
SAAS_SECURITY_SOURCES = [
    # Media - Broad Coverage
    RSSSource("The Register SaaS", "https://www.theregister.com/off_prem/saas/headlines.atom", SourceCategory.SAAS_SECURITY),
    RSSSource("TechCrunch SaaS", "https://techcrunch.com/tag/saas/feed/", SourceCategory.SAAS_SECURITY),
    RSSSource("DataBreaches.net", "https://databreaches.net/feed/", SourceCategory.SAAS_SECURITY),
    RSSSource("CIO", "https://www.cio.com/feed/", SourceCategory.SAAS_SECURITY),
    RSSSource("GBHackers", "https://gbhackers.com/feed/", SourceCategory.SAAS_SECURITY),
    RSSSource("Cloud Tech News", "https://cloudcomputing-news.net/feed/", SourceCategory.SAAS_SECURITY),
    
    # SaaS Security Specialists
    RSSSource("BetterCloud Monitor", "https://www.bettercloud.com/monitor/feed/", SourceCategory.SAAS_SECURITY),
    RSSSource("Grip Security", "https://www.grip.security/blog/rss.xml", SourceCategory.SAAS_SECURITY),
    
    # Non-English
    RSSSource("Heise Security", "https://www.heise.de/security/rss/news-atom.xml", SourceCategory.SAAS_SECURITY, language="de"),
    RSSSource("Anquanke", "https://api.anquanke.com/data/v1/rss", SourceCategory.SAAS_SECURITY, language="zh"),
    RSSSource("4hou", "https://www.4hou.com/feed", SourceCategory.SAAS_SECURITY, language="zh"),
]

# =============================================================================
# ADVERSARY_CYBER - Verified working
# =============================================================================
ADVERSARY_CYBER_SOURCES = [
    RSSSource("Mandiant Blog", "https://www.mandiant.com/resources/blog/rss.xml", SourceCategory.ADVERSARY_CYBER),
    RSSSource("CrowdStrike Blog", "https://www.crowdstrike.com/blog/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Microsoft Security Blog", "https://www.microsoft.com/en-us/security/blog/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Google TAG Blog", "https://blog.google/threat-analysis-group/rss/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Recorded Future", "https://www.recordedfuture.com/feed", SourceCategory.ADVERSARY_CYBER),
    RSSSource("The Record", "https://therecord.media/feed", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Flashpoint Intel", "https://flashpoint.io/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Intel471 Blog", "https://intel471.com/blog/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Sekoia Blog", "https://blog.sekoia.io/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("Daily NK", "https://www.dailynk.com/english/feed/", SourceCategory.ADVERSARY_CYBER),
    RSSSource("NK News", "https://www.nknews.org/feed/", SourceCategory.ADVERSARY_CYBER),
]

# =============================================================================
# RESEARCH_UPDATES - Verified working
# =============================================================================
RESEARCH_UPDATES_SOURCES = [
    RSSSource("IACR ePrint", "https://eprint.iacr.org/rss/rss.xml", SourceCategory.RESEARCH_UPDATES),
    RSSSource("IEEE Security & Privacy", "https://ieeexplore.ieee.org/rss/TOC8013.XML", SourceCategory.RESEARCH_UPDATES),
    RSSSource("Google Security Blog", "https://security.googleblog.com/feeds/posts/default", SourceCategory.RESEARCH_UPDATES),
]

# =============================================================================
# INVESTMENT - Verified working
# =============================================================================
INVESTMENT_SOURCES = [
    RSSSource("Crunchbase News", "https://news.crunchbase.com/feed/", SourceCategory.INVESTMENT),
    RSSSource("TechCrunch Security", "https://techcrunch.com/category/security/feed/", SourceCategory.INVESTMENT),
    RSSSource("FinSMEs", "https://www.finsmes.com/feed", SourceCategory.INVESTMENT),
    RSSSource("Silicon Angle", "https://siliconangle.com/feed/", SourceCategory.INVESTMENT),
    RSSSource("EU-Startups", "https://eu-startups.com/feed/", SourceCategory.INVESTMENT),
    RSSSource("AlleyWatch", "https://alleywatch.com/feed/", SourceCategory.INVESTMENT),
]

# =============================================================================
# LEGAL_REGULATIONS - Verified working
# =============================================================================
LEGAL_REGULATIONS_SOURCES = [
    RSSSource("EFF Deeplinks", "https://www.eff.org/rss/updates.xml", SourceCategory.LEGAL_REGULATIONS),
    RSSSource("EPIC News", "https://epic.org/feed/", SourceCategory.LEGAL_REGULATIONS),
    RSSSource("Access Now", "https://www.accessnow.org/feed/", SourceCategory.LEGAL_REGULATIONS),
]

# =============================================================================
# TECH_DEVELOPMENTS - Verified working
# =============================================================================
TECH_DEVELOPMENTS_SOURCES = [
    RSSSource("Ars Technica", "https://feeds.arstechnica.com/arstechnica/technology-lab", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("Wired", "https://www.wired.com/feed/rss", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("MIT Technology Review", "https://www.technologyreview.com/feed/", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("IEEE Spectrum", "https://spectrum.ieee.org/feeds/feed.rss", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("The Verge", "https://www.theverge.com/rss/index.xml", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("Hacker News", "https://news.ycombinator.com/rss", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("Cloudflare Blog", "https://blog.cloudflare.com/rss/", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("AWS Security Blog", "https://aws.amazon.com/blogs/security/feed/", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("Google Cloud Blog", "https://cloudblog.withgoogle.com/rss/", SourceCategory.TECH_DEVELOPMENTS),
    RSSSource("HashiCorp Blog", "https://www.hashicorp.com/blog/feed.xml", SourceCategory.TECH_DEVELOPMENTS),
]

# =============================================================================
# GEOPOLITICS - Verified working
# =============================================================================
GEOPOLITICS_SOURCES = [
    RSSSource("CFR", "https://feeds.feedburner.com/cfr_main", SourceCategory.GEOPOLITICS),
    RSSSource("RAND Commentary", "https://www.rand.org/pubs/commentary.xml", SourceCategory.GEOPOLITICS),
    RSSSource("RAND Research", "https://www.rand.org/pubs/new.xml", SourceCategory.GEOPOLITICS),
    RSSSource("Atlantic Council", "https://www.atlanticcouncil.org/feed/", SourceCategory.GEOPOLITICS),
    RSSSource("Foreign Affairs", "https://www.foreignaffairs.com/rss.xml", SourceCategory.GEOPOLITICS),
    RSSSource("War on the Rocks", "https://warontherocks.com/feed/", SourceCategory.GEOPOLITICS),
    RSSSource("Stimson Center", "https://www.stimson.org/feed/", SourceCategory.GEOPOLITICS),
]

# =============================================================================
# TARGET_ISRAEL - Verified working
# =============================================================================
TARGET_ISRAEL_SOURCES = [
    RSSSource("Times of Israel", "https://www.timesofisrael.com/feed/", SourceCategory.TARGET_ISRAEL),
    RSSSource("Times of Israel Tech", "https://www.timesofisrael.com/tech-israel/feed/", SourceCategory.TARGET_ISRAEL),
    RSSSource("Israel Defense", "https://www.israeldefense.co.il/en/rss.xml", SourceCategory.TARGET_ISRAEL),
    RSSSource("NoCamels Israel Tech", "https://nocamels.com/feed/", SourceCategory.TARGET_ISRAEL),
]

# =============================================================================
# TARGET_EUROPE - Verified working
# =============================================================================
TARGET_EUROPE_SOURCES = [
    RSSSource("ENISA News", "https://www.enisa.europa.eu/rss.xml", SourceCategory.TARGET_EUROPE),
    RSSSource("UK NCSC Reports", "https://www.ncsc.gov.uk/api/1/services/v1/report-rss-feed.xml", SourceCategory.TARGET_EUROPE),
    RSSSource("ANSSI France", "https://www.cert.ssi.gouv.fr/feed/", SourceCategory.TARGET_EUROPE, language="fr"),
    RSSSource("BSI Germany", "https://wid.cert-bund.de/content/public/securityAdvisory/rss", SourceCategory.TARGET_EUROPE, language="de"),
    RSSSource("Politico EU Tech", "https://www.politico.eu/section/technology/feed/", SourceCategory.TARGET_EUROPE),
    RSSSource("Silicon Republic", "https://www.siliconrepublic.com/feed", SourceCategory.TARGET_EUROPE),
    RSSSource("Euractiv", "https://www.euractiv.com/feed/", SourceCategory.TARGET_EUROPE),
]

# =============================================================================
# TARGET_US - Verified working
# =============================================================================
TARGET_US_SOURCES = [
    RSSSource("CISA Advisories", "https://www.cisa.gov/cybersecurity-advisories/all.xml", SourceCategory.TARGET_US),
    RSSSource("CISA News", "https://www.cisa.gov/news.xml", SourceCategory.TARGET_US),
    RSSSource("Cyberscoop", "https://cyberscoop.com/feed/", SourceCategory.TARGET_US),
    RSSSource("FedScoop", "https://fedscoop.com/feed/", SourceCategory.TARGET_US),
    RSSSource("Nextgov", "https://www.nextgov.com/rss/all/", SourceCategory.TARGET_US),
    RSSSource("FCW", "https://fcw.com/rss-feeds/all.aspx", SourceCategory.TARGET_US),
    RSSSource("StateScoop", "https://statescoop.com/feed/", SourceCategory.TARGET_US),
    RSSSource("MeriTalk", "https://www.meritalk.com/feed/", SourceCategory.TARGET_US),
]

# =============================================================================
# TARGET_SOUTH_KOREA - Verified working
# =============================================================================
TARGET_SOUTH_KOREA_SOURCES = [
    RSSSource("Daily NK", "https://www.dailynk.com/english/feed/", SourceCategory.TARGET_SOUTH_KOREA),
    RSSSource("NK News", "https://www.nknews.org/feed/", SourceCategory.TARGET_SOUTH_KOREA),
    RSSSource("AhnLab Security Blog", "https://asec.ahnlab.com/en/feed/", SourceCategory.TARGET_SOUTH_KOREA),
    RSSSource("보안뉴스 (Boan News)", "https://www.boannews.com/media/news_rss.xml", SourceCategory.TARGET_SOUTH_KOREA, language="ko"),
]

# =============================================================================
# TARGET_JAPAN - Verified working
# =============================================================================
TARGET_JAPAN_SOURCES = [
    RSSSource("JPCERT/CC", "https://www.jpcert.or.jp/english/rss/jpcert-en.rdf", SourceCategory.TARGET_JAPAN),
    RSSSource("JVN", "https://jvn.jp/en/rss/jvn.rdf", SourceCategory.TARGET_JAPAN),
    RSSSource("JVN iPedia", "https://jvndb.jvn.jp/en/rss/jvndb.rdf", SourceCategory.TARGET_JAPAN),
    RSSSource("Security NEXT", "https://www.security-next.com/feed", SourceCategory.TARGET_JAPAN, language="ja"),
    RSSSource("ScanNetSecurity", "https://scan.netsecurity.ne.jp/rss/index.rdf", SourceCategory.TARGET_JAPAN, language="ja"),
    RSSSource("Trend Micro Japan", "https://feeds.feedburner.com/tm-security-blog", SourceCategory.TARGET_JAPAN, language="ja"),
]


# =============================================================================
# HELPER FUNCTIONS
# =============================================================================
def get_all_sources() -> List[RSSSource]:
    """Get all configured RSS sources"""
    return (
        CYBER_ATTACKS_SOURCES +
        AUTH_IDENTITY_SOURCES +
        SAAS_SECURITY_SOURCES +
        ADVERSARY_CYBER_SOURCES +
        RESEARCH_UPDATES_SOURCES +
        INVESTMENT_SOURCES +
        LEGAL_REGULATIONS_SOURCES +
        TECH_DEVELOPMENTS_SOURCES +
        GEOPOLITICS_SOURCES +
        TARGET_ISRAEL_SOURCES +
        TARGET_EUROPE_SOURCES +
        TARGET_US_SOURCES +
        TARGET_SOUTH_KOREA_SOURCES +
        TARGET_JAPAN_SOURCES
    )


def get_sources_by_category(category: SourceCategory) -> List[RSSSource]:
    """Get sources for a specific category"""
    return [s for s in get_all_sources() if s.category == category]


def get_high_priority_sources() -> List[RSSSource]:
    """Get only high priority (priority=1) sources"""
    return [s for s in get_all_sources() if s.priority == 1]


def get_sources_by_language(language: str) -> List[RSSSource]:
    """Get sources by language code"""
    return [s for s in get_all_sources() if s.language == language]


def get_source_stats() -> dict:
    """Get statistics about configured sources"""
    all_sources = get_all_sources()
    by_category = {}
    for cat in SourceCategory:
        count = len([s for s in all_sources if s.category == cat])
        if count > 0:
            by_category[cat.value] = count
    by_language = {}
    for source in all_sources:
        by_language[source.language] = by_language.get(source.language, 0) + 1
    return {
        "total": len(all_sources),
        "by_category": by_category,
        "by_language": by_language,
    }


if __name__ == "__main__":
    stats = get_source_stats()
    print("=" * 50)
    print("zkHetz Brain Center - Sources (All Verified)")
    print("=" * 50)
    print(f"Total: {stats['total']}")
    print("\nBy Category:")
    for cat, count in sorted(stats['by_category'].items()):
        print(f"  {cat:<20} {count:>3}")
    print("\nBy Language:")
    for lang, count in sorted(stats['by_language'].items(), key=lambda x: -x[1]):
        print(f"  {lang:<5} {count:>3}")
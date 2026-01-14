import feedparser

# Test with one feed
url = "https://feeds.arstechnica.com/arstechnica/technology-lab"

print(f"Fetching: {url}")
feed = feedparser.parse(url)

print(f"Bozo (error flag): {feed.bozo}")
if feed.bozo:
    print(f"Bozo exception: {feed.bozo_exception}")

print(f"Feed title: {feed.feed.get('title', 'NO TITLE')}")
print(f"Number of entries: {len(feed.entries)}")

if feed.entries:
    print(f"First entry: {feed.entries[0].get('title', 'NO TITLE')}")
else:
    print("No entries found")
    print(f"Raw status: {getattr(feed, 'status', 'no status')}")
    print(f"Headers: {getattr(feed, 'headers', 'no headers')}")
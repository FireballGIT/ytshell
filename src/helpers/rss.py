import feedparser
from datetime import datetime

class RSSFetchError(Exception):
  pass

def fetch_rss(url):
  try:
    feed = feedparser.parse(url)

    if feed.bozo():
      raise RSSFetchError(f"Failed to fetch RSS feed: {feed.bozo_exception}")

    uploads = []

    for entry in feed.entries:
      try:
        title = entry.title;
        link = entry.link;
        if hasattr(entry, 'published_parsed'):
          date = datetime(*entry.published_parsed[:6])
        else:
          date = datetime.now()

        uploads.append({
          "title": title,
          "link": link,
          "date": date
        })

      except Exception as e:
        print(f"[rss] Skipping entry due to error: {e}")

    return uploads
  except Exception as e:
    raise RSSFetchError(f"RSS fetch error: {e}")

def latest_upload(url):
  uploads = fetch_rss(url)
  if not uploads:
    return None

  latest = max(uploads, key=lambda x: x["date"])
  return latest

def fetch_multiple(feeds):
  results = {}
  for url in feeds:
    try:
      results[url] = fetch_rss(url)
    except RSSFetchError as e:
      print(f"[rss] Failed to fetch {url}: {e}")
      results[url] = []
  return results

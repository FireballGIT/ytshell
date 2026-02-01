import json
from datetime import datetime
from pathlib import Path

class StorageError(Exception):
  pass

def _seralize_upload(upload):
  return {
    "title": upload["title"],
    "link": upload.get("link"),
    "date": upload["date"].isoformat()
    if isinstance(upload["date"], datetime)
    else upload["date"],
  }

def _deseralize_upload(upload):
  return {
    "title": upload["title"],
    "link": upload.get("link"),
    "date": datetime.fromisoformat(upload["date"]),
  }

def save_data(path, data):
  try:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    seralized = {}
    for channel, uploads in data.items():
      seralized[channel] = [_seralize_upload(u) for u in uploads]

    with path.open("w", encoding="utf-8") as f:
      json.dump(seralized, f, indent=2)
  except Exception as e:
    raise StorageError(f"Failed to save data: {e}")

def load_data(path):
  try:
    path = Path(path)
    if not path.exists():
      return {}

    with path.open("r", encoding="utf-8") as f:
      raw = json.load(f)

    data = {}
    for channel, uploads in raw.items():
      data[channel] = [_deseralize_upload(u) for u in uploads]

    return data

  except Exception as e:
    raise StorageError(f"Failed to load data: {e}")

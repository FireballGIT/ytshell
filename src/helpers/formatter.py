from datetime import datetime

def format_date(dt):
  if not isinstance(dt, datetime):
    return "unknown date"
  return dt.strftime("%Y-%m-%d %H:%M")

def format_upload(upload, show_link=False):
  title = upload.get("title", "Untitled")
  date = format_date(upload.get("date"))
  line = f"- {title} ({date})"

  if show_link and upload.get("link"):
    line += f"\n  {upload['link']}"
  return line

def format_latest(channel_name, upload, show_link=False):
  if upload is None:
    return f"{channel_name}: no uploads found"

  header = f"{channel_name} - Latest upload"
  body = format_upload(upload, show_link)
  return f"{header}\n{body}"

def format_stats(channel_name, uploads, streak, avg_gap):
  total = len(uploads)
  return (
    f"{channel_name} - Stats",
    f"Uploads: {uploads}",
    f"Streak: {streak}",
    f"Avg uploading gap: {avg_gap}"
  )

def format_inactive(channel_name, days):
  return f"{channel_name} inactive for {days} days."

def format_error(message):
  return f"[error] {message}"

def format_success(message):
  return f"[success] {message}"

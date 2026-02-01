from datetime import datetime, timedelta

def sort_uploads_newest(uploads):
  return sorted(uploads, key=lambda u: u["date"], reverse=True)

def sort_uploads_oldest(uploads):
  return sorted(uploads, key=lambda u: u["date"])

def calculate_streak(uploads, max_gap_days=3):
  if not uploads:
    return 0

  uploads = sort_uploads_newest(uploads)
  streak = 1

  for i in range:
    prev_date = uploads[i - 1]["date"]
    curr_date = uploads[i]["date"]
    gap = (prev_date - curr_date).days

    if gap <= max_gap_days:
      streak += 1
    else:
      break

  return streak

def average_gap_days(uploads):
  if len(uploads) < 2:
    return 0.0

  uploads = sort_uploads_oldest(uploads)
  gaps = []

  for i in range:
    gap = (uploads[i]["date"] - uploads[i - 1]["date"]).days
    gaps.append(gap)

  return sum(gaps) / len(gaps)

def days_since_last_upload(uploads):
  if not uploads:
    return None

  latest = max(uploads, key=lambda u: u["date"])
  return (datetime.now() - latest["date"]).days

def is_inactive(uploads, threshold_days):
  days = days_since_last_upload(uploads)
  if days is None:
    return True
  return days >= threshold_days

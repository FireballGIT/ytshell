from helpers import rss, stats, storage, formatter, ytconf
from datetime import datetime

class CommandError(Exception):
  pass

CHANNELS = {}
CACHE = {}

def load_config(path):
  global CHANNELS
  CHANNELS = ytconf.load_ytconf(path)
  return formatter.format_success(f"Loaded {len(CHANNELS)} channels")

def refresh_channel(handle):
  if handle not in CHANNELS:
    raise CommandError("Unknown channel {handle}")

  rss_url = CHANNELS[handle]["rss"]
  uploads = rss.fetch_rss(rss_url)
  CACHE[handle] = uploads
  return uploads

def refresh_all():
  for handle in CHANNELS:
    refresh_channel(handle)

def cmd_help(_channels, _flags, _args):
  return(
    "Commands:\n"
    "$help\n"
    "$exit\n"
    "$latest \\{@channel}\n"
    "$stats \\{@channel}\n"
    "$streak \\{@channel}\n"
    "$inactive [days]\n"
    "$load <file>"
    "$save <file>"
    "$reload\n"
    "$check"
  )

def cmd_latest(channels, flags, _args):
  output = []
  show_link = "--link" in flags

  for handle in channels:
    uploads = CACHE.get(handle) or refresh_channel(handle)
    latest = max(uploads, key=lambda u: u["date"]) if uploads else None
    output.append (
      formatter.format_latest(handle, latest, show_link)
    )

  return "\n\n".join(output)

def cmd_stats(channels, _flags, _args):
  output = []

  for handle in channels:
    uploads = CACHE.get(handle) or refresh_channel(handle)
    streak = stats.calculate_streak(uploads)
    avg_gap = stats.average_gap_days(uploads)

    output.append(
      formatter.format_stats(handle, uploads, streak, avg_gap)
    )

  return "\n\n".join(output)

def cmd_streak(channels, _flags, _args):
  lines = []

  for handle in channels:
    uploads = CACHE.get(handle) or refresh_channel(handle)
    streak = stats.calculate_streak(uploads)
    lines.append(f"{handle}: {streak}")

  return "\n".join(lines)

def cmd_inactive(_channels, _flags, args):
  days = int(args[0]) if args else 7
  lines = []

  for handle, uploads in CACHE.items():
    inactive_days = stats.days_since_last_upload(uploads)
    if inactive_days is not None and inactive_days >= days:
      lines.append(formatter.format_inactive(handle, inactive_days))

  return "\n".join(lines) if lines else "No inactive channels"

def cmd_load(_channels, _flags, args):
  if not args:
    raise CommandError("No file provided")

  global CACHE
  CACHE = storage.load_data(args[0])
  return formatter.format_success("Data loaded")

def cmd_save(_channels, _flags, args):
  if not args:
    raise CommandError("No file provided")

  CACHE = storage.save_data(args[0], CACHE)
  return formatter.format_success("Data saved")

def cmd_reload(_channels, _flags, _args):
  refresh_all()
  return formatter.format_success("All channels refreshed")

def cmd_check(_channels, _flags, _args):
  lines = []

  for handle in CHANNELS:
    uploads = CACHE.get(handle) or refresh_channel(handle)
    latest = max(uploads, key=lambda u: u["date"])
    lines.append(
      formatter.format_channel(handle, latest)
    )

  return "\n".join(lines)

def cmd_exit(_channels, _flags, _args):
  raise SystemExit

COMMANDS = {
  "$help": cmd_help,
  "$latest": cmd_latest,
  "$stats": cmd_stats,
  "$streak": cmd_streak,
  "$inactive": cmd_inactive,
  "$load": cmd_load,
  "$save": cmd_save,
  "$reload": cmd_reload,
  "$check": cmd_check,
  "$exit": cmd_exit,
}

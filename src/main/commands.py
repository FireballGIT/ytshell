import sys
import json
from datetime import datetime, timedelta

watchlist = {}

def cmd_help():
    print("Available commands:")
    print("$help       - Show this message")
    print("$exit       - Exit YTShell")
    print("$latest     - Show latest upload of a channel")
    print("$stats      - Show stats for a channel")
    print("$streak     - Show current upload streak")
    print("$inactive   - Show channels inactive for N days")
    print("$load       - Load watchlist/config from file")
    print("$reload     - Reload watchlist/config")
    print("$save       - Save watchlist/config to file")
    print("$check      - Check all watched channels")

def cmd_exit():
    print("Exiting YTShell...")
    sys.exit(0)

def cmd_latest(args):
    if not args:
        print("Usage: $latest {<channel>}")
        return
    channel = args[0].strip("{}")
    if channel not in watchlist:
        print(f"{channel} has no data.")
        return
    latest = max(watchlist[channel], key=lambda x: x["date"])
    print(f"Latest upload for {channel}:")
    print(f"Title: {latest['title']}")
    print(f"Date: {latest['date'].strftime('%Y-%m-%d %H:%M:%S')}")

def cmd_stats(args):
    if not args:
        print("Usage: $stats {<channel>}")
        return
    channel = args[0].strip("{}")
    if channel not in watchlist:
        print(f"{channel} has no data.")
        return
    uploads = watchlist[channel]
    num_uploads = len(uploads)
    if num_uploads < 2:
        avg_gap = "N/A"
        streak = num_uploads
    else:
        dates = sorted([u["date"] for u in uploads])
        gaps = [(dates[i] - dates[i-1]).days for i in range(1, len(dates))]
        avg_gap = sum(gaps)/len(gaps)
        streak = sum(1 for g in gaps if g <= 3) + 1
    print(f"Stats for {channel}:")
    print(f"Total uploads: {num_uploads}")
    print(f"Average gap (days): {avg_gap}")
    print(f"Current streak: {streak}")

def cmd_streak(args):
    if not args:
        print("Usage: $streak {<channel>}")
        return
    channel = args[0].strip("{}")
    if channel not in watchlist:
        print(f"{channel} has no data.")
        return
    uploads = sorted([u["date"] for u in watchlist[channel]], reverse=True)
    streak = 0
    for i in range(len(uploads)):
        if i == 0:
            streak += 1
            continue
        gap = (uploads[i-1] - uploads[i]).days
        if gap <= 3:
            streak += 1
        else:
            break
    print(f"{channel} upload streak: {streak}")

def cmd_inactive(args):
    days_threshold = 7
    if args:
        try:
            days_threshold = int(args[0])
        except ValueError:
            print("Usage: $inactive [days]")
            return
    cutoff = datetime.now() - timedelta(days=days_threshold)
    inactive_channels = [ch for ch, uploads in watchlist.items() if max(u["date"] for u in uploads) < cutoff]
    if not inactive_channels:
        print(f"No channels inactive for {days_threshold} days.")
    else:
        print(f"Channels inactive for {days_threshold} days or more:")
        for ch in inactive_channels:
            last_date = max(u["date"] for u in watchlist[ch])
            print(f"- {ch} (last upload: {last_date.strftime('%Y-%m-%d')})")

def cmd_load(args):
    global watchlist
    if not args:
        print("Usage: $load <file>")
        return
    file_path = args[0]
    try:
        with open(file_path, "r") as f:
            data = json.load(f)
        watchlist = {ch: [{"title": u["title"], "date": datetime.fromisoformat(u["date"])} for u in uploads] 
                     for ch, uploads in data.items()}
        print(f"Loaded watchlist from {file_path}")
    except Exception as e:
        print(f"Failed to load {file_path}: {e}")

def cmd_reload(args):
    cmd_load(args)

def cmd_save(args):
    if not args:
        print("Usage: $save <file>")
        return
    file_path = args[0]
    try:
        data = {ch: [{"title": u["title"], "date": u["date"].isoformat()} for u in uploads] for ch, uploads in watchlist.items()}
        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)
        print(f"Saved watchlist to {file_path}")
    except Exception as e:
        print(f"Failed to save {file_path}: {e}")

def cmd_check(args):
    if not watchlist:
        print("No channel data available.")
        return
    print("Tracked channels:")
    for ch, uploads in watchlist.items():
        latest = max(uploads, key=lambda x: x["date"])
        print(f"- {ch}: Latest upload '{latest['title']}' on {latest['date'].strftime('%Y-%m-%d')}")

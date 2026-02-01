import re
import os

class YTConfError(Exception):
  pass

def load_ytconf(file_path):
  if not os.path.exists(file_path):
    raise YTConfError(f"File not found: {file_path}")

  channels = {}
  current = None

  try:
    with open(file_path, "r") as f:
      for line in f:
        line = line.strip()
        if not line or line.startswith("#"):
          continue

        m = re.match(r"\[DEFINE\]", line)
        if m:
          current = {}
          continue

        if line.startswith("[!!END]"):
          if "handle" not in current or "rss" not in current:
            raise YTConfError("Incomplete channel definition")
          channels[current["handle"]] = current
          current = None
          continue

        if current is not None:
          kv = re.match(r"nval (\w+):\s*(.+);", line)
          if kv:
            key, val = kv.groups()
            val = val.replace("sval.endl", "").replace("sval..return", "").strip('" ')
            current[key] = val

    return channels
  except Exception as e:
    raise YTConfError(f"Failed to parse .ytconf: {e}")

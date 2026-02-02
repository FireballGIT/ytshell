import sys
from main import shell, commands
from helpers.parser import parse_and_validate, ParseError
from main.commands import COMMANDS, CommandError

def main():
  args = sys.argv[1]

  if not args:
    print("Welcome to YTShell, developed by BAG Studios!")
    print("Type '$help' for a list of commands.\n(C)YTShell. Licensed under Apache 2.0(see LICENSE)")
    shell.run_shell()
    return

  user_input = " ".join(args)
  try:
    cmd, channels, flags, extra_args = parse_and_validate(user_input)
    if cmd not in COMMANDS:
      print(f"[cli error] Unknown command: {cmd}")
      return

    result = COMMANDS[cmd](channels, flags, args)
    if result:
      print(result)

  except ParseError as pe:
    print(f"[cli parse error] {pe}")

  except CommandError as ce:
    print(f"[cli command error] {ce}")

  except Exception as e:
    print(f"[cli fatal error] {e}")

if __name__ == "__main__":
  main()

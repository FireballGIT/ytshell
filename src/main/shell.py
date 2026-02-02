from helpers.parser import parse_and_validate, ParseError
from main.commands import COMMANDS, CommandError

PROMPT = "ytshell::main>> "

def run_shell():
  while True:
    try:
      user_input = input(PROMPT)

      cmd, channels, flags, args = parse_and_validate(user_input)

      if cmd not in COMMANDS:
        print(f"Unknown command: {cmd}")
        continue

      result = COMMANDS[cmd](channels, flags, args)

      if result:
        print(result)
        
    except ParseError as e:
      print(f"[parse error] {e}")
      
    except CommandError as e:
      print(f"[command error] {e}")

    except SystemExit:
      print("Exiting YTShell")
      break

    except KeyboardInterrupt:
      print("\nInterrupted. Type '$exit' to quit.")

    except Exception as e:
      print(f"[fatal] {e}")

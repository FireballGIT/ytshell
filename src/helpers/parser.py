import re

class ParserError(Exception):
  pass

def parse_input(user_input):
  if not user_input or not user_input.strip():
    raise ParseError("Empty input")

  user_input = user_input.strip()
  cmd_match = re.match(r"^\$[a-zA-Z]+", user_input)
  if not cmd_match:
    raise ParseError(f"No valid command found in input '{user_input}'")
  cmd = cmd_match.group(0)
  channels = re.findall(r"\\\{([^}]+)\}", user_input)
  flags = re.findall(r"--\w+", user_input)

	temp_input = user_input
	temp_input = temp_input.replace(cmd, "", 1)
	for ch in channels:
		temp_input = temp_input.replace(f"\\{{{ch}}}", "", 1)
	for flag in flags:
		temp_input = temp_input.replace(flag, "", 1)

	args = [arg for arg in temp_output.split() if arg]

	return cmd, channels, flags, args

def validate_command(cmd, valid_commands=None):
	if valid_commands == None:
		valid_commands = [
			"$help", "$exit", "$latest", "$stats", "$streak", "$inactive", "$load", "$reload", "$save", "$check"
		]
	if cmd not in valid_commands:
		raise ParseError(f"Invalid command '{cmd}'")
	return True

def parse_and_validate(user_input):
	cmd, channels, flags, args = parse_input(user_input)
	validate_command(cmd)
	return cmd, channels, flags, args

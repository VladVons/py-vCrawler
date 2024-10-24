import json
import re

def find_line_number_for_path(json_str, path):
    # Split the target path by '/' to handle nested keys
    keys = path.split('/')
    
    # Load JSON into Python object
    try:
        data = json.loads(json_str)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON: {e}")

    # Split the JSON string into lines for tracking
    lines = json_str.splitlines()

    # Helper function to find the line number for a key
    def find_key_line_number(key, start_line=0):
        for i in range(start_line, len(lines)):
            if re.search(rf'"{key}"\s*:', lines[i]):
                return i + 1  # Line numbers are 1-indexed
        return None

    # Traverse the keys step-by-step to find their line numbers
    current_data = data  # To validate the path exists
    current_line = 0

    for key in keys:
        # Check if the key exists at this level
        if not isinstance(current_data, dict) or key not in current_data:
            raise KeyError(f"Path not found: {'/'.join(keys)}")

        # Update the data to the next level for further traversal
        current_data = current_data[key]

        # Find the line number of the current key
        line_number = find_key_line_number(key, current_line)
        if line_number is None:
            raise ValueError(f"Could not find line number for key: {key}")

        # Update current line to continue search after this point
        current_line = line_number

    print(f"Found key path '{path}' ending at line: {current_line}")

# Sample JSON string
json_str = '''
{
  "key1": {
    "key2": {
      "key3": "value"
    }
  }
}
'''

# Search for the path 'key1/key2/key3'
find_line_number_for_path(json_str, 'key1/key2/key3')

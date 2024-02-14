"""This python file takes a string command line argument and prints all lines in 'activity.log' with that string """
import subprocess
import sys

# Define the search string and the log file path
search_string = script_name = sys.argv[1]
log_file_path = "activity.log"

# Build the findstr command
command = f'findstr "{search_string}" "{log_file_path}"'

# Run the command
process = subprocess.run(command, capture_output=True, text=True, shell=True)


history = process.stdout.split('\n')
for record in history:
    print(record)
    

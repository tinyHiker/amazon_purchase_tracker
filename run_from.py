import subprocess

python_interpreter = "python"  
option = "-u"
script_path = "grep.py"
arguments = ["Taha"]

command = [python_interpreter, option, script_path] + arguments

result = subprocess.run(command, capture_output=True, text=True)


if result.returncode == 0:
    print(result.stdout)
else:
    print("Error running script:")
    print(result.stderr)
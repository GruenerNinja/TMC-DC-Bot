import subprocess

# List of required packages
required_packages = [
    'discord.py',
    'discord-py-interactions'
]

# Install required packages
for package in required_packages:
    subprocess.check_call(['pip3', 'install', package])

print("Dependencies installed successfully.")

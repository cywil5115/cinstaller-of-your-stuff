# Installation Script

## Description
This script is designed to install applications and execute custom commands on a Linux system using various package managers. It automatically detects the available package manager and performs the installations and commands defined by the user. It now supports specifying a preferred package manager, including 'brew' for macOS users or Linux systems with Homebrew.

## Usage
The script can be run with default files (`apps.txt` for applications and `custom_commands.txt` for commands), or you can specify custom files and a preferred package manager via command line arguments.

### Using the Bash Script
You can also use the provided `install.sh` script to run the Python script with more ease. This Bash script allows you to specify custom files or run with default settings without directly interacting with the Python script.

#### Bash Script Arguments
- `--apps-file`: Specifies the applications file (optional). Default is `apps.txt`.
- `--commands-file`: Specifies the custom commands file (optional). Default is `custom_commands.txt`.
- `--package-manager`: Specify the preferred package manager to use (optional).

#### Bash Script Examples
Run the script with default files:
```
./install.sh
```

Run the script with custom files and specify a package manager:
```
./install.sh --apps-file custom_apps.txt --commands-file custom_commands.txt --package-manager manager_name
```

### Python Script Arguments
- `--apps-file`: Specifies the file from which application names to install will be read. Defaults to `apps.txt`.
- `--commands-file`: Specifies the file from which custom commands will be read. Defaults to `custom_commands.txt`.
- `--package-manager`: Specify the preferred package manager to use (optional).

### Python Script Examples
Run the script with default files:
```
python3 Installation_Script.py
```

Run the script with custom files and a specific package manager:
```
python3 Installation_Script.py --apps-file custom_apps.txt --commands-file custom_commands.txt --package-manager manager_name
```

### Help
To display options and help for the Python script, use:
```
python3 Installation_Script.py -h
```
For the Bash script, use:
```
./install.sh -h
```
To comment app or command use '#' in apps or custom_commands file. Example:
```
app1
#app2
app3
```

## Requirements
The script requires appropriate package managers to be installed and accessible on the system, as well as Python 3 with the `argparse` module.

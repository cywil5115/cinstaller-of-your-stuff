#!/bin/bash

if [ "$EUID" -ne 0 ]
  then echo "Please run this awesome cywil's script as root (superuser)." && echo "You can type now: sudo !!"
  exit
fi

# List of required tools
required_tools=("python3" "curl" "git")

check_requirements() {
    for tool in "${required_tools[@]}"; do
        if ! which "$tool" > /dev/null 2>&1; then
            echo "Error: Required tool '$tool' is not installed."
            return 1
        fi
    done
    echo "All required tools are installed."
    sleep 2
}

if ! check_requirements; then
    echo "Please install the missing tools before running the script."
    exit 1
fi

# Initialize variables to indicate if the files were set
APPS_FILE=""
COMMANDS_FILE=""
PACKAGE_MANAGER=""

# Check for arguments and update file names if provided
while [ "$#" -gt 0 ]; do
  case "$1" in
    --apps-file)
      APPS_FILE="$2"
      shift 2
      ;;
    --commands-file)
      COMMANDS_FILE="$2"
      shift 2
      ;;
    --package-manager)
      PACKAGE_MANAGER="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: ./install.sh [--apps-file APPS_FILE] [--commands-file COMMANDS_FILE] [--package-manager PACKAGE_MANAGER]"
      echo "  --apps-file        Specify the applications file (optional)"
      echo "  --commands-file    Specify the custom commands file (optional)"
      echo "  --package-manager  Specify the preferred package manager to use (optional)"
      echo "  -h, --help         Display this help message"
      exit 0
      ;;
    *)
      echo "Error: Unsupported flag $1" >&2
      echo "Use -h or --help for usage information."
      exit 1
      ;;
  esac
done

# Execute the Python script with the specified or default file names
CMD_ARGS=""
[ -n "$APPS_FILE" ] && CMD_ARGS+=" --apps-file $APPS_FILE"
[ -n "$COMMANDS_FILE" ] && CMD_ARGS+=" --commands-file $COMMANDS_FILE"
[ -n "$PACKAGE_MANAGER" ] && CMD_ARGS+=" --package-manager $PACKAGE_MANAGER"

if [ -n "$CMD_ARGS" ]; then
    python3 Installation_Script.py $CMD_ARGS
else
    python3 Installation_Script.py
fi

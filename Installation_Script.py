import os
import subprocess
import shutil
import argparse
import time
import sys

def user_confirmation():
    response = input("Do you want to continue? [y,t,yes,tak/N]: ")
    # To continue press: "t", "tak", "y", "yes"
    return response.strip().lower() in ["y", "yes", "t", "tak"]

def get_script_path():
    return os.path.dirname(os.path.realpath(__file__))

def create_file_as_user(file_path):
    if not os.path.exists(file_path):
        open(file_path, 'w').close()  # Create the file
        # Fetch the original user's UID and GID if available
        uid = int(os.getenv('SUDO_UID', os.getuid()))
        gid = int(os.getenv('SUDO_GID', os.getgid()))
        os.chown(file_path, uid, gid)  # Change ownership

def read_app_list(file_path):
    file_path = os.path.join(get_script_path(), file_path)
    create_file_as_user(file_path)
    with open(file_path, 'a') as f:
        if os.path.getsize(file_path) == 0: # Only write if file is empty
            #f.write("# Example applications (uncomment to install):\n")
            f.write("tldr\n")
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            apps = [line.strip() for line in content.split() if line.strip() and not line.startswith('#')]
            if apps:
                print("Scheduled to install the following applications:")
                for app in apps:
                    print(f"- {app}")
                if not user_confirmation():
                    print("Operation aborted by user.")
                    pass
            else:
                print("No applications to install.")
            time.sleep(1)
            return apps
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {str(e)}")

def check_package_manager(preferred_manager=None):
    managers = {
        'nala': ['nala', ['nala', '--version']],
        'apt': ['apt-get', ['apt-get', '--version']],
        'dnf': ['dnf', ['dnf', '--version']],
        'pacman': ['pacman', ['-S', '--version']],
        'zypper': ['zypper', ['zypper', '--version']],
        'apx': ['apx', ['apx', '--version']],
        'brew': ['brew', ['brew', '--version']]
    }
    if preferred_manager and preferred_manager in managers and shutil.which(managers[preferred_manager][0]):
        return preferred_manager
    for manager, commands in managers.items():
        base_command, version_command = commands
        if shutil.which(base_command):
            if subprocess.run(['which', base_command], stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                return base_command
            elif subprocess.run(version_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode == 0:
                return base_command
    raise EnvironmentError("No supported package manager found on this system.")

def install_applications(applications, package_manager):
    command_base = [package_manager, 'install'] if package_manager not in ['pacman'] else [package_manager, '-S']
    for app in applications:
        command = command_base + [app, '-y']
        try:
            subprocess.run(command, check=True)
        except subprocess.CalledProcessError:
            print(f"Warning: Failed to install {app}. Continuing with other installations.")
            time.sleep(1)

def execute_custom_commands(file_path, execute_commands):
    file_path = os.path.join(get_script_path(), file_path)
    create_file_as_user(file_path)
    if execute_commands:
        try:
            with open(file_path, 'r') as file:
                commands = [line.strip() for line in file if line.strip() and not line.startswith('#')]
            if commands:
                print("Scheduled to execute the following commands:")
                for command in commands:
                    print(f"- {command}")
                if not user_confirmation():
                    print("Operation aborted by user.")
                    sys.exit()
            else:
                print("No custom commands to execute.")
            time.sleep(1)
            for command in commands:
                subprocess.run(command, shell=True, check=True)
        except Exception as e:
            print(f"Error executing command. Details: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Install applications and execute commands from specified files.')
    parser.add_argument('--apps-file', default='apps.txt', help='File containing list of applications to install')
    parser.add_argument('--commands-file', default='custom_commands.txt', help='File containing custom commands to execute')
    parser.add_argument('--package-manager', help='Preferred package manager to use')
    args = parser.parse_args()

    package_manager = check_package_manager(args.package_manager)
    apps = read_app_list(args.apps_file)
    install_applications(apps, package_manager)
    execute_custom_commands(args.commands_file, execute_commands=True)

if __name__ == '__main__':
    main()

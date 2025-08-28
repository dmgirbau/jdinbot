#!/usr/bin/env python3
import os
import sys
import subprocess
from typing import List

def main() -> None:
    # Check if running as root (UID 0)
    if os.getuid() == 0:
        # Get APP_USER from environment or default to 1001
        app_user = os.environ.get('APP_USER', '1001')
        
        try:
            # Try to get UID and GID for the specified user
            user_id = subprocess.run(['id', '-u', app_user], 
                                   capture_output=True, text=True, check=True).stdout.strip()
            group_id = subprocess.run(['id', '-g', app_user],
                                    capture_output=True, text=True, check=True).stdout.strip()
        except subprocess.CalledProcessError:
            # Fallback to 1001 if user doesn't exist
            user_id = '1001'
            group_id = '1001'
        
        # Change ownership of /app directory
        subprocess.run(['chown', '-R', f'{user_id}:{group_id}', '/app'], check=False)
        
        # Execute the command as the specified user
        cmd = sys.argv[1:]
        try:
            subprocess.run(['su-exec', f'{user_id}:{group_id}'] + cmd, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)
    else:
        # If not root, execute the command directly
        cmd = sys.argv[1:]
        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            sys.exit(e.returncode)

if __name__ == '__main__':
    main()
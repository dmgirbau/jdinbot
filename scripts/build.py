#!/usr/bin/env python3
import os
import subprocess
import sys
from typing import Optional

def run_docker_compose(mode: str) -> None:
    """Run docker-compose with the appropriate configuration."""
    try:
        # Set environment variables
        env_vars = {
            'DEV_MODE': 'true' if mode == 'dev' else 'false',
            'ENV': 'development' if mode == 'dev' else 'production'
        }
        
        # Update current environment
        os.environ.update(env_vars)
        
        print(f"Starting {mode} container with environment:")
        for key, value in env_vars.items():
            print(f"  {key}={value}")
        
        # Run docker-compose
        result = subprocess.run(
            ['docker-compose', 'up', '--build'],
            check=False,  # Don't raise exception on non-zero exit
            env=os.environ  # Pass current environment
        )
        
        if result.returncode != 0:
            print(f"docker-compose exited with code {result.returncode}")
            sys.exit(result.returncode)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
        sys.exit(130)
    except FileNotFoundError:
        print("Error: docker-compose not found. Is Docker installed?")
        sys.exit(127)
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

def main() -> None:
    """Main function to handle command line arguments and execution."""
    # Parse command line arguments
    if len(sys.argv) > 2:
        print("Usage: script.py [dev|prod]")
        sys.exit(1)
    
    mode = sys.argv[1] if len(sys.argv) > 1 else 'dev'
    mode = mode.lower()
    
    if mode not in ['dev', 'prod']:
        print("Usage: script.py [dev|prod]")
        print(f"Error: Invalid mode '{mode}'")
        sys.exit(1)
    
    run_docker_compose(mode)

if __name__ == '__main__':
    main()

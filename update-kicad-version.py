#!/usr/bin/env python3
"""
KiCad Git Version Updater
Updates KiCad project files with current git version information.
Usage: python3 update_kicad_version.py [project_file.kicad_pro]
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def get_git_info():
    """Get git information for the current repository."""

    try:
        subprocess.run(['git', 'status'], check=True, capture_output=True)
        
        git_info = {}
        
        result = subprocess.run(['git', 'rev-parse', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_HASH'] = result.stdout.strip()
        
        result = subprocess.run(['git', 'rev-parse', '--short', 'HEAD'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_SHORT_HASH'] = result.stdout.strip()
        
        result = subprocess.run(['git', 'branch', '--show-current'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_BRANCH'] = result.stdout.strip()
        
        result = subprocess.run(['git', 'describe', '--tags', '--exact-match'], 
                              capture_output=True, text=True)
        git_info['GIT_TAG'] = result.stdout.strip() if result.returncode == 0 else ""
        
        result = subprocess.run(['git', 'log', '-1', '--format=%cd', '--date=short'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_DATE'] = result.stdout.strip()
        
        result = subprocess.run(['git', 'log', '-1', '--format=%an'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_AUTHOR'] = result.stdout.strip()
        
        result = subprocess.run(['git', 'status', '--porcelain'], 
                              capture_output=True, text=True, check=True)
        git_info['GIT_DIRTY'] = "dirty" if result.stdout.strip() else "clean"

        return git_info
        
    except subprocess.CalledProcessError:
        print("Error: Not in a git repository or git command failed")
        return None

def update_kicad_project(project_file, git_info):
    """Update a KiCad project file with git information."""

    try:
        with open(project_file, 'r') as f:
            data = json.load(f)
        
        # Ensure text_variables section exists
        if 'text_variables' not in data:
            data['text_variables'] = {}
        
        # Update all git variables
        for key, value in git_info.items():
            data['text_variables'][key] = value
        
        # Write back to file
        with open(project_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Updated {project_file} with git information:")
        for key, value in git_info.items():
            print(f"  {key}: {value}")
        
        return True
        
    except Exception as e:
        print(f"Error updating {project_file}: {e}")
        return False


def find_kicad_projects():
    """Find all .kicad_pro files in the current directory and subdirectories."""
    return list(Path('.').rglob('*.kicad_pro'))




def main():
    # Get git information
    git_info = get_git_info()

    if not git_info:
        sys.exit(1)
    
    if len(sys.argv) > 1:
        # Update specific project file
        project_file = sys.argv[1]
        if not os.path.exists(project_file):
            print(f"Error: Project file '{project_file}' not found")
            sys.exit(1)
        update_kicad_project(project_file, git_info)

    else:
        # Update all project files found
        projects = find_kicad_projects()
        if not projects:
            print("No .kicad_pro files found in current directory or subdirectories")
            sys.exit(1)
        
        print(f"Found {len(projects)} KiCad project(s):")
        for project in projects:
            update_kicad_project(project, git_info)

if __name__ == "__main__":
    main()


import os
import json
from pathlib import Path

CONFIG_FILE = '.env.sh'

def load_api_keys():
    """Load API keys from config file if it exists"""
    config_path = Path(CONFIG_FILE)
    if config_path.exists():
        with open(CONFIG_FILE, 'r') as f:
            lines = f.readlines()
            keys = {}
            for line in lines:
                if '=' in line:
                    key, value = line.strip().split('=')
                    keys[key] = value.strip('"')
            return keys
    return None

def save_api_keys(gemini_key, github_key):
    """Save API keys to config file"""
    with open(CONFIG_FILE, 'w') as f:
        f.write(f'GEMINI_API_KEY="{gemini_key}"\n')
        f.write(f'GITHUB_API_KEY="{github_key}"\n')

def remove_api_keys():
    """Remove the config file containing API keys"""
    try:
        os.remove(CONFIG_FILE)
        print("API keys have been removed successfully.")
    except FileNotFoundError:
        print("No API keys found.")

def main():
    keys = load_api_keys()
    
    if keys:
        print("\nExisting API keys found!")
        choice = input("Do you want to:\n1. Continue with existing keys\n2. Remove existing keys\n3. Update keys\nChoice (1/2/3): ")
        
        if choice == '2':
            remove_api_keys()
            return
        elif choice == '3':
            pass  # Continue to key input
        elif choice == '1':
            return keys
        else:
            print("Invalid choice!")
            return None
    
    print("\nPlease enter your API keys:")
    gemini_key = input("Gemini API Key: ").strip()
    github_key = input("GitHub API Key: ").strip()
    
    if gemini_key and github_key:
        save_api_keys(gemini_key, github_key)
        print("API keys saved successfully!")
        return {"GEMINI_API_KEY": gemini_key, "GITHUB_API_KEY": github_key}
    else:
        print("Both API keys are required!")
        return None

if __name__ == "__main__":
    api_keys = main()
    if api_keys:
        print("\nAPI Keys loaded successfully!")
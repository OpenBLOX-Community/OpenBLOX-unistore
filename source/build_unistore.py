import json
import os
import glob
from datetime import datetime

def get_store_info():
    """Return the store info directly"""
    return {
        "storeName": "OpenBLOX Maps",
        "storeAuthor": "OpenBLOX Community",
        "storeVersion": "1.0.0",
        "storeDescription": "A collection of classic Roblox maps for OpenBLOX",
        "storeURL": "https://github.com/OpenBLOX-Community/rbxl-maps"
    }

def load_apps():
    """Load all app JSON files from the apps directory"""
    # Get the script's directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(script_dir, 'apps')
    
    print(f"Looking for apps in: {apps_dir}")
    apps = []
    app_files = glob.glob(os.path.join(apps_dir, '*.json'))
    print(f"Found app files: {app_files}")
    
    for app_file in app_files:
        print(f"Loading app file: {app_file}")
        with open(app_file, 'r') as f:
            app_data = json.load(f)
            apps.append(app_data)
    
    return apps

def build_unistore():
    """Build the complete UniStore JSON"""
    store_info = get_store_info()
    apps = load_apps()
    
    # Sort apps to ensure core/required apps are first
    apps.sort(key=lambda x: (
        'core' not in x['info'].get('category', []),
        'required' not in x['info'].get('category', []),
        x['info']['title']
    ))
    
    unistore = {
        "storeInfo": store_info,
        "storeContent": apps
    }
    
    return unistore

def save_unistore(unistore):
    """Save the UniStore to a file"""
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'openblox.unistore')
    
    print(f"Saving unistore to: {output_path}")
    
    # Create a backup of the existing file if it exists
    if os.path.exists(output_path):
        backup_path = f"{output_path}.bak"
        print(f"Creating backup at: {backup_path}")
        os.replace(output_path, backup_path)
    
    # Save the new UniStore
    with open(output_path, 'w') as f:
        json.dump(unistore, f, indent=2)
    
    # Verify the file was created
    if os.path.exists(output_path):
        print(f"Successfully created unistore file at: {output_path}")
    else:
        print(f"Failed to create unistore file at: {output_path}")
    
    return output_path

def main():
    print("Building OpenBlox UniStore...")
    print(f"Current working directory: {os.getcwd()}")
    
    try:
        unistore = build_unistore()
        output_path = save_unistore(unistore)
        print("UniStore built successfully!")
        print(f"Output saved to: {output_path}")
    except Exception as e:
        print(f"Error building UniStore: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
import json

import os
import glob
from datetime import datetime

def load_categories():
    """Load the categories from categories.json"""
    with open('categories.json', 'r') as f:
        return json.load(f)

def load_store_info():
    """Load the store info from store_info.json"""
    store_info_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'store_info.json')
    with open(store_info_path, 'r') as f:
        return json.load(f)

def load_apps():
    """Load all app JSON files from the apps directory"""
    apps = []
    app_files = glob.glob('apps/*.json')
    
    for app_file in app_files:
        with open(app_file, 'r') as f:
            app_data = json.load(f)
            apps.append(app_data)
    
    return apps

def validate_categories(apps, categories):
    """Validate that all categories used in apps are defined in categories.json"""
    valid_categories = set(categories.keys())
    errors = []
    
    for app in apps:
        app_categories = app['info'].get('category', [])
        for category in app_categories:
            if category not in valid_categories:
                errors.append(f"Invalid category '{category}' in {app['info']['title']}")
    
    return errors

def build_unistore():
    """Build the complete UniStore JSON"""
    store_info = load_store_info()
    apps = load_apps()
    categories = load_categories()
    
    # Validate categories
    errors = validate_categories(apps, categories)
    if errors:
        print("Category validation errors:")
        for error in errors:
            print(f"  - {error}")
        raise ValueError("Invalid categories found in apps")
    
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
    output_path = '../openblox.unistore'
    
    # Create a backup of the existing file if it exists
    if os.path.exists(output_path):
        backup_path = f"{output_path}.bak"
        os.replace(output_path, backup_path)
    
    # Save the new UniStore
    with open(output_path, 'w') as f:
        json.dump(unistore, f, indent=2)

def main():
    print("Building OpenBlox UniStore...")
    
    try:
        unistore = build_unistore()
        save_unistore(unistore)
        print("UniStore built successfully!")
        print(f"Output saved to: {os.path.abspath('../openblox.unistore')}")
    except Exception as e:
        print(f"Error building UniStore: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 
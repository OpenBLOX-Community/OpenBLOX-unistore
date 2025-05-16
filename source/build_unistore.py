import json
import os
import glob
import subprocess
from datetime import datetime

def get_store_info():
    return {
        "storeName": "OpenBLOX Maps",
        "storeAuthor": "OpenBLOX Community",
        "storeVersion": "1.0.0",
        "storeDescription": "A collection of classic Roblox maps for OpenBLOX",
        "storeURL": "https://github.com/OpenBLOX-Community/rbxl-maps"
    }

def load_apps():
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
    store_info = get_store_info()
    apps = load_apps()

    apps.sort(key=lambda x: (
        'core' not in x['info'].get('category', []),
        'required' not in x['info'].get('category', []),
        x['info']['title']
    ))

    return {
        "storeInfo": store_info,
        "storeContent": apps
    }

def save_unistore(unistore):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, 'openblox.unistore')

    print(f"Saving unistore to: {output_path}")
    if os.path.exists(output_path):
        backup_path = f"{output_path}.bak"
        print(f"Creating backup at: {backup_path}")
        os.replace(output_path, backup_path)

    with open(output_path, 'w') as f:
        json.dump(unistore, f, indent=2)

    if os.path.exists(output_path):
        print(f"✅ UniStore file created: {output_path}")
    else:
        print(f"❌ Failed to create unistore file!")

    return output_path

def generate_t3x():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    t3s_path = os.path.join(script_dir, 'openblox.t3s')
    t3x_path = os.path.join(script_dir, 'openblox.t3x')

    if not os.path.exists(t3s_path):
        print(f"❌ Cannot generate T3X: {t3s_path} does not exist.")
        return

    print(f"🎨 Generating T3X from: {t3s_path}")
    try:
        subprocess.run(['tex3ds', '-i', t3s_path, '-o', t3x_path], check=True)
        print(f"✅ Created {t3x_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ tex3ds failed: {e}")

def main():
    print("🔧 Building OpenBLOX UniStore and generating icons...")
    print(f"Current working directory: {os.getcwd()}")

    try:
        generate_t3x()
        unistore = build_unistore()
        output_path = save_unistore(unistore)
        print(f"✅ All done! UniStore saved to: {output_path}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())
 
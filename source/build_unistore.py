import json
import os
import glob
import subprocess

def get_store_info():
    return {
        "storeName": "OpenBLOX Maps",
        "storeAuthor": "OpenBLOX Community",
        "storeVersion": "1.0.0",
        "storeDescription": "A collection of classic Roblox maps for OpenBLOX",
        "storeURL": "https://github.com/OpenBLOX-Community/rbxl-maps",
        "file": "openblox.unistore",
        "sheet": "openblox.t3x",
        "sheetURL": "https://openblox-community.github.io/OpenBLOX-unistore/openblox.t3x",
        "version": 3,
        "revision": 1
    }

def load_apps():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(script_dir, 'apps')

    print(f"🔍 Looking for apps in: {apps_dir}")
    apps = []
    app_files = glob.glob(os.path.join(apps_dir, '*.json'))
    print(f"📄 Found app files: {app_files}")

    for app_file in app_files:
        print(f"📥 Loading: {app_file}")
        with open(app_file, 'r', encoding='utf-8') as f:
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

def save_unistore(unistore, output_dir):
    output_path = os.path.join(output_dir, 'openblox.unistore')

    print(f"💾 Saving UniStore to: {output_path}")
    if os.path.exists(output_path):
        backup_path = f"{output_path}.bak"
        print(f"🗂️ Backing up old UniStore to: {backup_path}")
        os.replace(output_path, backup_path)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(unistore, f, indent=2)

    if os.path.exists(output_path):
        print(f"✅ UniStore created at: {output_path}")
    else:
        print(f"❌ Failed to write UniStore!")
    return output_path

def generate_t3x(output_dir):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    t3s_path = os.path.join(script_dir, 'openblox.t3s')
    t3x_path = os.path.join(output_dir, 'openblox.t3x')

    if not os.path.exists(t3s_path):
        print(f"❌ Missing spritesheet source: {t3s_path}")
        return

    print(f"🎨 Running tex3ds: {t3s_path} -> {t3x_path}")
    try:
        subprocess.run(['tex3ds', '-i', t3s_path, '-o', t3x_path], check=True)
        print(f"✅ Created: {t3x_path}")
    except subprocess.CalledProcessError as e:
        print(f"❌ tex3ds failed: {e}")

def main():
    print("🛠️ Building OpenBLOX UniStore...")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(script_dir, '..'))  # Go up one level

    print(f"📂 Output directory: {output_dir}")

    try:
        generate_t3x(output_dir)
        unistore = build_unistore()
        output_path = save_unistore(unistore, output_dir)
        print(f"\n🚀 Done! Files saved to: {output_dir}")
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return 1

    return 0

if __name__ == "__main__":
    exit(main())

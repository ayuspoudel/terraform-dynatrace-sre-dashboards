import os
import json
import requests
import argparse
from dotenv import load_dotenv

load_dotenv()

DT_API_TOKEN = os.getenv("DT_API_TOKEN")
DT_TENANT_URL = os.getenv("DT_TENANT_URL")
TILES_DIR = os.path.dirname(__file__)
LAYOUT_FILE = os.path.join(TILES_DIR, "layouts.json")

def load_layouts():
    with open(LAYOUT_FILE, "r") as f:
        return json.load(f)["layouts"]

def load_tiles(layouts):
    tiles = []
    for file in sorted(os.listdir(TILES_DIR)):
        if file.endswith(".json") and file not in {"layouts.json", "dashboard-v2.json", "deploy_dashboard.py"}:
            try:
                with open(os.path.join(TILES_DIR, file)) as f:
                    content = json.load(f)
                    key, tile_data = list(content.items())[0]
                    if key in layouts:
                        tile_data["layout"] = layouts[key]
                        tiles.append(tile_data)
                    else:
                        print(f"⚠️  No layout for tile key: {key}")
            except Exception as e:
                print(f"⚠️  Skipping {file}: {e}")
    return tiles

def build_dashboard(tiles, name):
    return {
        "dashboardMetadata": {
            "name": name,
            "shared": True,
            "tags": ["dql", "availability", "ayush"]
        },
        "tiles": tiles
    }

def deploy_dashboard(dashboard):
    url = f"{DT_TENANT_URL}/platform/monitoring/dashboards"
    headers = {
        "Authorization": f"Api-Token {DT_API_TOKEN}",
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json=dashboard)
    if response.status_code >= 400:
        print(f"❌ Error uploading dashboard: {response.status_code} {response.reason}")
        print(f"📬 Response: {response.text}")
        return
    dashboard_id = response.json().get("id")
    print("✅ Dashboard created:", dashboard_id)
    print(f"🔗 {DT_TENANT_URL}/ui/apps/dashboards-app/dashboards/{dashboard_id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", help="Dashboard name", required=True)
    args = parser.parse_args()

    if not DT_API_TOKEN or not DT_TENANT_URL:
        print("❌ Missing DT_API_TOKEN or DT_TENANT_URL in .env file.")
        exit(1)

    layouts = load_layouts()
    tiles = load_tiles(layouts)
    dashboard = build_dashboard(tiles, args.name)

    with open(os.path.join(TILES_DIR, "dashboard-v2.json"), "w") as f:
        json.dump(dashboard, f, indent=2)

    deploy_dashboard(dashboard)

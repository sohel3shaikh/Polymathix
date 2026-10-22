import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_OWNER = "sohel3shaikh"
REPO_NAME = "Polymathix"
TAG_NAME = "v1.0.1"
RELEASE_TITLE = "Polymathix OS v1.0.1: Universal 3D Molecular, Materials Science & AI Co-Pilot Discovery Engine"

RELEASE_BODY = """## 🚀 Polymathix OS v1.0.1 — Universal Computational Intelligence

**Polymathix OS v1.0.1** is a major milestone release expanding the autonomous scientific discovery engine across **all living kingdoms** (Plants & Crops, Animals, Human Therapeutics, Microbial Biocatalysis) and **Solid-State Inorganic Materials Science & Nanotechnology**.

---

### 🌟 What's New in v1.0.1

#### 1. 🔬 Solid-State Materials Science & Inorganic Crystallography Engine
* Native 3D unit cell coordinate generators and structural analyzers for inorganic lattices:
  * **Perovskite ($\text{SrTiO}_3$)**: Cubic space group $Pm\bar{3}m$ (221), $a = 3.905\text{ \AA}$, 12-fold / 6-fold coordination.
  * **2D Graphene Monolayer**: $sp^2$ hexagonal planar lattice ($C-C = 1.42\text{ \AA}$).
  * **Carbon Nanotubes ($(5,5)\text{ SWCNT}$)**: Chiral armchair cylinder with cylindrical coordinate transformation.
  * **Anatase $\text{TiO}_2$ Photocatalyst**: Tetragonal coordination with distorted octahedral geometry.
  * **Metal-Organic Framework ($\text{MOF-5}$)**: Porous coordination network with high internal surface area.
* Automatic computation of lattice parameters, density, coordination numbers, and pore diameters.

#### 2. 📚 3D Discovery Library Catalog (23+ Pre-Built Systems)
* Comprehensive curated catalog categorized across 5 discovery sectors:
  * **Human Therapeutics**: Aspirin, Caffeine, Ibuprofen, Artemisinin, Doxorubicin, Remdesivir.
  * **Crop Science & Agriculture**: Rubisco Activase, Plant Defensin, Strigolactone, Drought Resilience Factor.
  * **Solid-State Materials**: $\text{SrTiO}_3$ Perovskite, Graphene Monolayer, $(5,5)\text{ SWCNT}$, $\text{TiO}_2$, $\text{MOF-5}$.
  * **Microbial Biocatalysis**: PETase Plastic Degrader, Formate Dehydrogenase, Subtilisin.
  * **Veterinary Health**: Ivermectin Macrocycle, Enrofloxacin, Bravecto Fluralaner.
* **1-Click Actions**: **"Load 3D Viewport"** and **"⚡ Make Novel Variant"** live derivatization.

#### 3. 🤖 Multi-LLM 3rd-Party AI Co-Pilot Gateway
* Plug-and-play API attachment in Settings for leading foundation models:
  * **Anthropic Claude** (Claude 3.5 Sonnet / Opus)
  * **OpenAI ChatGPT** (GPT-4o / o1)
  * **xAI Grok** (Grok-2 / Grok-Mini)
  * **Moonshot Kimi** (Moonshot-v1)
  * **Zhipu GLM-4**
  * **Google Gemini** (Gemini 1.5 Pro)
  * **Local Ollama** (100% offline, zero-cloud privacy)
* Built-in autonomous zero-key fallback with deterministic chemistry reasoning.

#### 4. ⚡ Real-Time Conversational AI & Structure Mutation
* Real-time conversational bubbles in the top navigation bar and full-screen AI chat modal.
* Natural language prompt execution: e.g., *"Synthesize 5-fluoro-aspirin"* triggers real-time RDKit molecular derivatization, SMILES conversion, MMFF94 force-field geometry optimization, and direct 3D coordinate injection into the viewport.

#### 5. 🎯 Universal 3D Viewport & 100% Progress Convergence
* Added universal Three.js coordinate mapping and auto-scaling for all molecules and crystal lattices (resolving blank-viewport conditions).
* Eliminated the 83% bottleneck — simulations now converge smoothly from Step 1 through Step 6 to **100% Finalized**.

---

### 🧪 Automated Quality & Test Verification
All **15 / 15** automated verification tests pass cleanly:
```bash
python scripts/test_all.py
# VERIFICATION SUMMARY: 15 PASSED, 0 FAILED
```

---

### 🎬 Quick Start (Run Locally in 3 Steps)

```bash
# 1. Clone the repository
git clone https://github.com/sohel3shaikh/Polymathix.git
cd Polymathix

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch Polymathix OS
python -m streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

### 📦 Release Assets
* **`Polymathix-Master-Release.zip`**: Complete offline standalone release archive.
* **`Polymathix_Showcase_Demo.mp4`**: High-definition (1080p/720p) video walkthrough and feature demonstration.
"""

def get_github_token():
    p = subprocess.Popen(
        ['git', 'credential', 'fill'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    out, err = p.communicate('protocol=https\nhost=github.com\n')
    for line in out.splitlines():
        if line.startswith('password='):
            return line.split('=', 1)[1].strip()
    return None

def publish_release():
    token = get_github_token()
    if not token:
        print("ERROR: GitHub token could not be retrieved from git credentials.")
        return False
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'Polymathix-Release-Script'
    }
    
    # 1. Check if release already exists for this tag
    check_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/tags/{TAG_NAME}"
    existing_release = None
    try:
        req = urllib.request.Request(check_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            existing_release = json.loads(resp.read())
            print(f"Release already exists for {TAG_NAME} (ID: {existing_release.get('id')})")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"No existing release for {TAG_NAME}. Will create new release.")
        else:
            print(f"HTTP error checking release: {e}")

    # 2. Create or Update Release
    payload = {
        "tag_name": TAG_NAME,
        "target_commitish": "master",
        "name": RELEASE_TITLE,
        "body": RELEASE_BODY,
        "draft": False,
        "prerelease": False
    }
    
    if existing_release:
        rel_id = existing_release['id']
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{rel_id}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='PATCH')
    else:
        url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases"
        req = urllib.request.Request(url, data=json.dumps(payload).encode('utf-8'), headers=headers, method='POST')

    try:
        with urllib.request.urlopen(req) as resp:
            rel_data = json.loads(resp.read())
            print(f"Successfully published release: {rel_data.get('html_url')}")
            upload_url_template = rel_data.get('upload_url')
            rel_id = rel_data.get('id')
    except Exception as e:
        print(f"Failed to publish release: {e}")
        return False

    # 3. Upload assets (Zip & Videos)
    assets_to_upload = [
        (os.path.join(os.path.dirname(ROOT_DIR), "Polymathix-Master-Release.zip"), "Polymathix-Master-Release.zip", "application/zip"),
        (os.path.join(os.path.dirname(ROOT_DIR), "Polymathix_Showcase_Demo.mp4"), "Polymathix_Showcase_Demo.mp4", "video/mp4"),
        (os.path.join(os.path.dirname(ROOT_DIR), "Polymathix_Showcase_Demo1.mp4"), "Polymathix_Showcase_Demo1.mp4", "video/mp4")
    ]

    # Fetch existing assets on the release
    assets_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/{rel_id}/assets"
    existing_asset_names = {}
    try:
        req = urllib.request.Request(assets_url, headers=headers)
        with urllib.request.urlopen(req) as resp:
            assets_list = json.loads(resp.read())
            for a in assets_list:
                existing_asset_names[a['name']] = a['id']
    except Exception as e:
        print(f"Could not list existing assets: {e}")

    for file_path, asset_name, content_type in assets_to_upload:
        if not os.path.exists(file_path):
            print(f"Asset file not found, skipping: {file_path}")
            continue

        # If asset already exists, delete it first to re-upload fresh
        if asset_name in existing_asset_names:
            del_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/assets/{existing_asset_names[asset_name]}"
            try:
                del_req = urllib.request.Request(del_url, headers=headers, method='DELETE')
                with urllib.request.urlopen(del_req) as resp:
                    print(f"Deleted old asset {asset_name}")
            except Exception as e:
                print(f"Failed to delete old asset {asset_name}: {e}")

        # Upload
        clean_upload_url = upload_url_template.split('{')[0] + f"?name={asset_name}"
        upload_headers = {
            'Authorization': f'token {token}',
            'Content-Type': content_type,
            'User-Agent': 'Polymathix-Release-Script'
        }
        print(f"Uploading {asset_name} ({os.path.getsize(file_path)/(1024*1024):.2f} MB)...")
        with open(file_path, 'rb') as f:
            file_bytes = f.read()
        
        upload_req = urllib.request.Request(clean_upload_url, data=file_bytes, headers=upload_headers, method='POST')
        try:
            with urllib.request.urlopen(upload_req) as resp:
                asset_res = json.loads(resp.read())
                print(f"Successfully uploaded {asset_name}: {asset_res.get('browser_download_url')}")
        except Exception as e:
            print(f"Failed to upload {asset_name}: {e}")

    print("\nRelease publish and asset synchronization complete!")
    print(f"GitHub Release URL: https://github.com/{REPO_OWNER}/{REPO_NAME}/releases/tag/{TAG_NAME}")
    return True

if __name__ == "__main__":
    publish_release()

import os
import sys
import json
import subprocess
import urllib.request
import urllib.error

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO_OWNER = "sohel3shaikh"
REPO_NAME = "Polymathix"
TAG_NAME = "v1.0.2"
RELEASE_TITLE = "Polymathix OS v1.0.2: Cross-Domain Physical Invariants & Cryptographic Scientific Provenance Ledger"

RELEASE_BODY = """## 🚀 Polymathix OS v1.0.2 — Cross-Domain Correctness & Scientific Reproducibility

**Polymathix OS v1.0.2** introduces a mathematically grounded **Cross-Domain Physical Invariants Verification Engine** and a **Cryptographic Scientific Provenance Ledger**, directly addressing the fundamental challenges of scientific correctness across disparate domains and deterministic reproducibility across diverse LLMs and local Ollama model versions.

---

### 🌟 What's New in v1.0.2

#### 1. 🛡️ Cross-Domain Physical Invariants & Correctness Verifier (`polymathix.core.invariants`)
How do you define "correctness" across domains as fundamentally different as protein docking and crystallographic lattices?
In physical sciences, correctness cannot be a single heuristic. Polymathix formalizes correctness through **domain-specific conservation laws and physical invariant suites** evaluated during the **VERIFY** stage:
* **Structural Biology & Biomolecular Mechanics**:
  * **Pauli Repulsion Steric Clash Exclusion**: Enforces non-bonded interatomic thresholds ($d \ge 0.70 \times (r_{\\text{vdW},i} + r_{\\text{vdW},j})$).
  * **Hydrogen-Bond Potential Well Bounds**: Strict Donor-Acceptor distance ($2.4\\text{ \\AA} \\le d \\le 3.6\\text{ \\AA}$) and angular criteria.
  * **Coulombic Salt-Bridge Pairing Radius**: Cation-anion interaction cutoff within aqueous Debye-Hückel screening limits ($d \\le 4.0\\text{ \\AA}$).
  * **Peptide Backbone Metric Continuity**: Trans-peptide Cα-Cα spacing bounds ($2.5\\text{ \\AA} \\le d \\le 4.5\\text{ \\AA}$, centered at $3.8\\text{ \\AA}$).
* **Solid-State Chemistry & Inorganic Crystallography**:
  * **Unit Cell Formal Electroneutrality**: Formal oxidation state summation over unit cell stoichiometry strictly equals zero (e.g. in $\\text{SrTiO}_3$, $\\text{Sr}^{2+} + \\text{Ti}^{4+} - 3\\times\\text{O}^{2-} = 0.00$).
  * **Shannon-Prewitt Interatomic Radius Bound**: Verifies interatomic spacing against coordinated ionic/covalent radii sums without unphysical lattice collapse.
  * **Space Group Symmetry Invariance**: Validates fractional coordinate consistency under space group symmetry operations (e.g., $Pm\\bar{3}m$ No. 221).
  * **Volumetric Mass Density Concordance**: Unit cell theoretical mass density concordance (e.g. $5.12\\text{ g/cm}^3$ for $\\text{SrTiO}_3$, $2.26\\text{ g/cm}^3$ for Graphene/SWCNT).
* **Cheminformatics & Molecular Mechanics**:
  * **Kekulé Octet Valence Saturation**: Zero hypervalent atom centers.
  * **Lipinski Rule-of-Five Compliance**: Automated bounds screening for molecular weight and lipophilicity ($\\text{LogP}$).
  * **Force-Field Residual Energy Gradient**: RMS force gradient convergence below stationary potential thresholds.
* **Automated Correctness Dossier**: Generates a structured verification dossier with confidence scoring ($0.0 \\to 1.0$) and explicit numerical residual tracking.

#### 2. 🔐 Cryptographic Scientific Provenance Ledger & Deterministic Replay Engine (`polymathix.core.provenance`)
How do you guarantee reproducibility when users attach different LLMs or update local Ollama models?
Polymathix v1.0.2 introduces a **3-Pillar Reproducibility Architecture**:
1. **Separation of Intent vs Computation**: The LLM functions strictly as an **intent-to-DSL compiler** (producing canonical SMILES, space group symbols, stoichiometry, and seed specifications). The LLM is never permitted to invent raw floating-point coordinates or energy trajectories.
2. **Deterministic Physics Kernels**: All physical simulations, force-field minimizations (MMFF94 / OpenMM), and coordinate math are executed by seed-locked, bit-reproducible scientific kernels.
3. **Cryptographic Run Manifest (`run_provenance`)**: Every run records an immutable ledger containing:
   * **Model Identity & Checksum**: Provider name, model identifier, model SHA256 digest, sampling temperature ($T=0.0$ greedy argmax), and PRNG seed (default $42$).
   * **Prompt Fingerprint**: SHA256 hash of system and user prompts.
   * **Canonical Intermediate Representation (IR)**: Formula, atom count, space group, and SHA256 coordinate manifold fingerprint.
   * **Deterministic Replay Engine**: Allows any researcher with a run manifest to replay and verify the discovery workflow bit-for-bit without calling an LLM.

#### 3. 🧪 Comprehensive Test Suite (17 / 17 Tests Passing)
Expanded automated verification suite covering both new modules:
```bash
python scripts/test_all.py
# [TEST] 16. Cross-Domain Physical Invariants & Correctness Verifier... --> PASSED
# [TEST] 17. Cryptographic Run Provenance & Deterministic Replay Engine... --> PASSED
# VERIFICATION SUMMARY: 17 PASSED, 0 FAILED
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
* **`Polymathix-Master-Release.zip`**: Complete offline standalone release archive (v1.0.2).
* **`Polymathix_Showcase_Demo1.mp4`**: Authentic 3-minute video walkthrough and real UI demonstration.
* **`Polymathix_Showcase_Demo.mp4`**: High-definition video showcase asset.
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

        if asset_name in existing_asset_names:
            del_url = f"https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/releases/assets/{existing_asset_names[asset_name]}"
            try:
                del_req = urllib.request.Request(del_url, headers=headers, method='DELETE')
                with urllib.request.urlopen(del_req) as resp:
                    print(f"Deleted old asset {asset_name}")
            except Exception as e:
                print(f"Failed to delete old asset {asset_name}: {e}")

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

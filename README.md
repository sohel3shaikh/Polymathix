# 🧬 POLYMATHIX OS — Autonomous AI for Scientific Discovery
> **Universal Computational Intelligence for Life Sciences: Plants & Crops, Animals, Human Therapeutics & Microbial Biocatalysis.**

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B.svg)](https://streamlit.io)
[![Three.js](https://img.shields.io/badge/Three.js-r160-black.svg)](https://threejs.org/)
[![RDKit](https://img.shields.io/badge/RDKit-2023+-green.svg)](https://www.rdkit.org/)
[![OpenMM](https://img.shields.io/badge/OpenMM-8.0+-purple.svg)](https://openmm.org/)

---

## 🌟 Overview

**Polymathix OS** is an open-source, AI-orchestrated scientific intelligence operating system designed to accelerate discoveries across **all living beings**:
* 🌾 **Agricultural & Crop Sciences**: Protein thermal adaptation, drought resilience, Rubisco engineering, natural plant defense metabolites.
* 🐾 **Veterinary & Animal Health**: Zoonotic disease targets, species-specific pharmacokinetics, non-toxic veterinary therapeutics.
* 🧪 **Human Health & De-Novo Drug Design**: Small-molecule bioisostere generation, Lipinski Rule-of-Five screening, target pocket docking.
* 🦠 **Microbial & Environmental Biocatalysis**: Catalytic triad optimization (Ser-His-Asp), plastic-degrading enzymes (PETase), carbon-capture metalloenzymes.

Rather than acting as a static dashboard, Polymathix introduces a **closed-loop AI Orchestrator** following the **Plan ➔ Execute ➔ Verify** methodology.

```
                         RESEARCHER
                             │
                      Natural Language
                             │
                             ▼
                  ┌─────────────────────┐
                  │   AI ORCHESTRATOR   │
                  └──────────┬──────────┘
                             │
             ┌───────────────┼───────────────┐
             ▼               ▼               ▼
           PLAN           EXECUTE         VERIFY
             │               │               │
             ▼               ▼               ▼
          Protocol         MCP/API        Analysis
          Manager          Router          Engine
             │               │               │
             └───────────────┼───────────────┘
                             ▼
                 EXTERNAL SCIENTIFIC ENGINES
                             │
        ┌──────────────┬─────┴────────┬──────────────┐
        ▼              ▼              ▼              ▼
      RDKit          OpenMM        PyMOL/RCSB     Kernel PCA
        │              │              │              │
        └──────────────┼──────────────┴──────────────┘
                       ▼
                 DATA PIPELINE
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
     Real-Time      Three.js 3D    Automated
    Terminal Logs    Viewport       Dossier
```

---

## ⚡ Key Capabilities

### 1. 🧠 Natural Language AI Orchestrator
* **Intent-Driven Protocol Selection**: Type natural research prompts (e.g., *"Run Crop Proteome & Thermal Adaptation"*, *"Synthesize novel drug with RDKit"*, *"Load Ubiquitin 1UBQ"*, *"Autonomous energy minimization"*).
* **Calibrated Protocols**: Pre-calibrated protocols for membrane dynamics, de-novo pharmacophores, non-linear PCA trajectory unfolding, and binding pocket contact mapping.
* **Autonomous Session Management**: Multi-session lifecycle with live progress calculation and execution pause/stop/resume gates.

### 2. 🔬 Multi-Kingdom Discovery Engines
* **RDKit Cheminformatics**: Automated bioisostere fragmentation, Lipinski Rule-of-Five profiling (MW ≤ 500, LogP ≤ 5, HBD ≤ 5, HBA ≤ 10, TPSA ≤ 140 Å², Rotatable Bonds ≤ 10), and 2D chemical structure synthesis.
* **Deep Non-Linear Trajectory PCA**: Overcomes linear PCA limitations by deploying RBF Kernel PCA to unroll high-dimensional protein conformational manifolds.
* **OpenMM Self-Healing Physics**: Autonomous PDB topology verification, hydrogen addition at pH 7.4, TIP3P solvation, and potential energy minimization with convergence tracking.
* **Live RCSB PDB Ingestion**: Direct fetching and atomic parsing of any entry from the Protein Data Bank (e.g., `1UBQ`, `4HHB`, `6LU7`, `1CRN`).

### 3. 🎨 High-Performance 3D WebGL Molecular Viewer
* **Multi-Representation Engine**: Live switching between **Cartoon Ribbon** (multi-color rainbow CA backbone), **Surface** (van der Waals envelope), **Sticks** (atomic bonds), **Sphere** (space-filling CPK), and **Mesh** (wireframe).
* **Active Site Contact Profiling**: Euclidean residue-ligand distance calculations with interaction classification (Hydrogen bond, Hydrophobic, Electrostatic, π-π stacking).
* **Multi-Format 3D Exporters**: Export models to **OBJ** (Blender), **STL** (3D printing), **GLB/GLTF** (Web & XR), and **PLY** (CAD/Point Clouds).

### 4. 📊 Multi-Tab Research Workspace
* **3D Viewer**: Full orbit controls, focus, camera reset, snapshot download.
* **Sequence Viewer**: Primary amino acid sequence chips with residue numbering and secondary structure color coding.
* **Trajectory Timeline**: Dynamic frame scrubber with RMSD and energy stability tracking.
* **Properties Table**: Molecular weight, atom count, formula, chains, resolution, and isoelectric point (pI).
* **Analysis**: Comparative plots for latent space manifold projections and minimization trajectories.

---

## 🚀 Quick Start & Installation

### Prerequisites
* Python 3.10 or higher
* [Conda](https://docs.conda.io/en/latest/) or `pip`

### Step 1: Clone the Repository
```bash
git clone https://github.com/YourUsername/Polymathix.git
cd Polymathix
```

### Step 2: Create Environment & Install Dependencies
```bash
# Using conda (Recommended for OpenMM and RDKit)
conda create -n polymathix python=3.10 -y
conda activate polymathix
conda install -c conda-forge rdkit openmm pdbfixer -y
pip install -r requirements.txt
```

### Step 3: Run the Live Application
```bash
python -m streamlit run app.py
```
Open your browser at **`http://localhost:8501`**.

---

## 🧪 Comprehensive Verification Suite

Run the full end-to-end automated verification suite to test all scientific engines:
```bash
python scripts/test_all.py
```

Expected output:
```
============================================================
POLYMATHIX OS — COMPREHENSIVE END-TO-END VERIFICATION
============================================================
[TEST] 1. Polymathix Orchestrator Initialization & PDB Parsing... --> PASSED
[TEST] 2. De-Novo Drug Synthesis Engine (RDKit Backend)...       --> PASSED
[TEST] 3. Deep Trajectory PCA & Manifold Learning Engine...      --> PASSED
[TEST] 4. Self-Healing Energy Minimization & OBJ Exporter...     --> PASSED
[TEST] 5. Quick Action Handlers & Session Lifecycle...           --> PASSED
[TEST] 6. Agent Controls (Pause, Stop, Run)...                   --> PASSED
[TEST] 7. Tool Connector Router & Toggle Logic...                 --> PASSED
[TEST] 8. Frontend Scientific Assets Synchronization...           --> PASSED
[TEST] 9. Frontend Index HTML & Three.js 3D Engine Integrity...  --> PASSED
[TEST] 10. Streamlit Master Application Compilation...            --> PASSED
============================================================
VERIFICATION SUMMARY: 10 PASSED, 0 FAILED
============================================================
```

---

## 📁 Repository Structure

```
Polymathix/
├── app.py                     # Master Streamlit entry point
├── polymathix/                # Core Python scientific intelligence backend
│   ├── orchestrator.py        # AI Orchestrator (Plan -> Execute -> Verify)
│   ├── core/                  # Multiscale dynamics
│   └── modules/               # Domain-specific scientific tools
│       ├── drug_hunting/      # RDKit de-novo synthesis & Lipinski screening
│       ├── quick_pca/         # Deep Kernel PCA non-linear manifold learning
│       ├── data_resilience/   # Potential energy graphing engine
│       └── visual_factory/    # PDB to OBJ 3D mesh exporter
├── polymathix_ui/             # Bidirectional Streamlit Custom Component
│   ├── __init__.py            # Python-to-JavaScript component bridge
│   └── frontend/              # Glassmorphic 3D dashboard
│       ├── index.html         # Three.js WebGL dashboard & layout
│       └── assets/            # Live scientific plots, models & renders
├── scripts/                   # Automated testing & deployment scripts
│   └── test_all.py            # End-to-end test suite
├── 1CRN.pdb                   # Benchmark reference (Crambin plant seed protein)
├── requirements.txt           # Python package requirements
└── README.md                  # Comprehensive scientific documentation
```

---

## 🤝 Contributing

We welcome contributions from structural biologists, bioinformaticians, agronomists, veterinary researchers, and machine learning engineers!
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/NewDiscoveryEngine`)
3. Commit your Changes (`git commit -m 'Add Crop Drought Resilience Module'`)
4. Push to the Branch (`git push origin feature/NewDiscoveryEngine`)
5. Open a Pull Request

---

## 📜 Citation & License

Distributed under the **MIT License**. Free for academic, industrial, and open-source scientific research.

```bibtex
@software{polymathix2026,
  author = {Polymathix Open-Source Contributors},
  title = {Polymathix OS: Autonomous AI for Multi-Kingdom Scientific Discovery},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/YourUsername/Polymathix}
}
```

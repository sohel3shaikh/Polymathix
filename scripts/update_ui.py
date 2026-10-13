import os
import re

html_path = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Add extra CSS for panels and inputs
extra_css = """
/* ================= ENHANCED WORKSPACE PANELS & INPUTS ================= */
.searchMainInput {
    width: 100%;
    background: transparent;
    border: none;
    outline: none;
    color: #f2f7ff;
    font-size: 14px;
    font-family: inherit;
    font-weight: 500;
}
.searchMainInput::placeholder {
    color: #65819e;
}

.workspacePanel {
    position: relative;
    min-height: 0;
    overflow-y: auto;
    margin: 0 9px;
    padding: 18px;
    border-radius: 12px;
    background: radial-gradient(circle at 50% 45%, rgba(14,78,128,.15), transparent 45%), #010811;
    display: none;
    color: #e2e8f0;
}

.workspacePanel.active {
    display: block;
}

.seqGrid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(52px, 1fr));
    gap: 8px;
    margin-top: 14px;
}

.seqChip {
    padding: 8px 4px;
    text-align: center;
    border-radius: 8px;
    background: rgba(14, 38, 64, 0.7);
    border: 1px solid rgba(56, 189, 248, 0.2);
    font-size: 11px;
    transition: all 0.2s;
    cursor: pointer;
}
.seqChip:hover {
    border-color: #38bdf8;
    background: rgba(20, 75, 130, 0.8);
    transform: translateY(-2px);
}
.seqResName {
    font-weight: bold;
    color: #38bdf8;
}
.seqResNum {
    font-size: 9px;
    color: #94a3b8;
    margin-top: 2px;
}

.propTable {
    width: 100%;
    border-collapse: collapse;
    margin-top: 14px;
}
.propTable th, .propTable td {
    padding: 10px 14px;
    text-align: left;
    border-bottom: 1px solid rgba(90, 178, 255, 0.15);
    font-size: 12px;
}
.propTable th {
    color: #7dd3fc;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 10px;
    letter-spacing: 0.5px;
}
.propTable td {
    color: #f1f5f9;
}

.analysisPlotPreview {
    max-width: 100%;
    border-radius: 10px;
    border: 1px solid rgba(56, 189, 248, 0.3);
    box-shadow: 0 0 20px rgba(0, 120, 255, 0.2);
    margin-top: 12px;
}
"""

# Inject extra_css before </style>
html = html.replace("</style>", extra_css + "\n</style>", 1)

# 2. Replace Search bar text with interactive input
old_search_text = """        <div class="searchText">
            <div class="searchMain">
                Ask Polymathix anything...
            </div>

            <div class="searchExample">
                e.g. "Show glucose binding site and identify residues within 4 Å"
            </div>
        </div>"""

new_search_text = """        <div class="searchText">
            <input type="text" class="searchMainInput" id="aiInput" placeholder="Ask Polymathix anything... (e.g., 'Run Membrane MD v2.4' or 'Synthesize novel drug with RDKit')" onkeydown="if(event.key==='Enter') runAI()" />
            <div class="searchExample">
                e.g. "Run Membrane MD v2.4" | "Synthesize de-novo drug with RDKit" | "Deep Trajectory PCA" | "Autonomous OpenMM Minimization"
            </div>
        </div>"""

if old_search_text in html:
    html = html.replace(old_search_text, new_search_text, 1)

# 3. Add IDs and triggers to Session, Protocol, Status, Workflow
html = html.replace('<div class="sessionName">\n            MembraneONE\n        </div>', '<div class="sessionName" id="sessionNameDisplay">MembraneONE</div>', 1)
html = html.replace('<div class="sessionName">\n            Membrane MD v2.4\n        </div>', '<div class="sessionName" id="protocolNameDisplay">Membrane MD v2.4</div>', 1)
html = html.replace('<span class="status">\n            <span class="statusDot"></span>\n            Active\n        </span>', '<span class="status" id="sessionStatusDisplay"><span class="statusDot"></span>Active</span>', 1)
html = html.replace('<span>Estimated time remaining: 2h 14m</span>', '<span id="timeRemainingDisplay">Estimated time remaining: 2h 14m</span>', 1)
html = html.replace('<div class="resultGrid">', '<div class="resultGrid" id="resultGrid">', 1)

# Replace Agent buttons with trigger functions
html = html.replace('<button class="agentButton" onclick="pauseJob()">', '<button class="agentButton" onclick="triggerAgentControl(\'pause\')">', 1)
html = html.replace('<button class="agentButton" onclick="stopJob()">', '<button class="agentButton" onclick="triggerAgentControl(\'stop\')">', 1)
html = html.replace('<button class="agentButton" onclick="runAI()">', '<button class="agentButton" onclick="triggerAgentControl(\'run\')">', 1)

# Replace Quick Action buttons
html = html.replace('onclick="newSession()"', 'onclick="triggerQuickAction(\'new_session\')"', 1)
html = html.replace('onclick="runProtocol()"', 'onclick="triggerQuickAction(\'run_protocol\')"', 1)
html = html.replace('onclick="analyzeData()"', 'onclick="triggerQuickAction(\'analyze_data\')"', 1)
html = html.replace('onclick="generatePlot()"', 'onclick="triggerQuickAction(\'generate_plot\')"', 1)
html = html.replace('onclick="createReport()"', 'onclick="triggerQuickAction(\'create_report\')"', 1)

# 4. Add interactive tabs to Workspace
old_tabs = """    <div class="tabs">

        <div class="tab active">
            3D Viewer
        </div>

        <div class="tab">
            Sequence
        </div>

        <div class="tab">
            Trajectory
        </div>

        <div class="tab">
            Surfaces
        </div>

        <div class="tab">
            Properties
        </div>

        <div class="tab">
            Analysis
        </div>

    </div>"""

new_tabs = """    <div class="tabs">
        <div class="tab active" onclick="switchWorkspaceTab('viewer', this)">3D Viewer</div>
        <div class="tab" onclick="switchWorkspaceTab('sequence', this)">Sequence</div>
        <div class="tab" onclick="switchWorkspaceTab('trajectory', this)">Trajectory</div>
        <div class="tab" onclick="switchWorkspaceTab('surfaces', this)">Surfaces</div>
        <div class="tab" onclick="switchWorkspaceTab('properties', this)">Properties</div>
        <div class="tab" onclick="switchWorkspaceTab('analysis', this)">Analysis</div>
    </div>"""

if old_tabs in html:
    html = html.replace(old_tabs, new_tabs, 1)

# Wrap canvas in ID and add sibling panels
old_canvas = '<div class="canvasWrap">'
new_canvas_and_panels = """<div class="canvasWrap" id="threeCanvasWrap">"""
html = html.replace(old_canvas, new_canvas_and_panels, 1)

# Add panels right after </canvasWrap>
panels_html = """
    <!-- SEQUENCE PANEL -->
    <div class="workspacePanel" id="sequencePanel">
        <div style="font-size:14px;font-weight:700;color:#38bdf8;display:flex;justify-content:space-between;align-items:center;">
            <span>Primary Sequence (1CRN - Chain A)</span>
            <span style="font-size:11px;color:#94a3b8;">46 Residues | High Resolution</span>
        </div>
        <div class="seqGrid" id="seqGridContainer">
            <!-- Populated dynamically from PDB data -->
        </div>
    </div>

    <!-- TRAJECTORY PANEL -->
    <div class="workspacePanel" id="trajectoryPanel">
        <div style="font-size:14px;font-weight:700;color:#38bdf8;">Molecular Dynamics Trajectory Timeline</div>
        <div style="margin-top:10px;font-size:12px;color:#94a3b8;">Frames: 1500 / 1500 | Timestep: 2.0 fs | Ensemble: NPT (300K, 1 bar)</div>
        <div style="margin-top:18px;display:flex;align-items:center;gap:12px;">
            <button class="styleBtn" onclick="toggleTrajectoryPlay()">▶ Play / Pause</button>
            <input type="range" min="0" max="1500" value="750" style="flex:1" id="trajSlider" oninput="document.getElementById('trajFrame').innerText = this.value" />
            <span id="trajFrame" style="font-size:12px;font-family:monospace;min-width:60px;">750</span>
        </div>
        <div style="margin-top:20px;padding:14px;background:rgba(10,31,57,0.6);border-radius:10px;border:1px solid rgba(56,189,248,0.2);">
            <div style="font-size:12px;color:#7dd3fc;font-weight:600;">RMSD & Energy Stability</div>
            <div style="font-size:11px;color:#cbd5e1;margin-top:6px;">Average Backbone RMSD: 0.84 ± 0.05 Å. System maintains stable crystallographic fold throughout production run.</div>
        </div>
    </div>

    <!-- SURFACES PANEL -->
    <div class="workspacePanel" id="surfacesPanel">
        <div style="font-size:14px;font-weight:700;color:#38bdf8;">Molecular Surfaces & Potentials</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:14px;">
            <div style="padding:14px;background:rgba(10,31,57,0.6);border-radius:10px;border:1px solid rgba(56,189,248,0.2);cursor:pointer;" onclick="toggleSurface()">
                <div style="font-weight:600;color:#38bdf8;">Solvent Accessible Surface (SASA)</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">Probe radius: 1.4 Å | Conolly analytical rolling ball algorithm</div>
            </div>
            <div style="padding:14px;background:rgba(10,31,57,0.6);border-radius:10px;border:1px solid rgba(56,189,248,0.2);cursor:pointer;" onclick="showToast('Surface','Electrostatic potential map loaded')">
                <div style="font-weight:600;color:#ff4d67;">Poisson-Boltzmann Electrostatics</div>
                <div style="font-size:11px;color:#94a3b8;margin-top:4px;">Coulombic charge mapping (-10 kT/e to +10 kT/e)</div>
            </div>
        </div>
    </div>

    <!-- PROPERTIES PANEL -->
    <div class="workspacePanel" id="propertiesPanel">
        <div style="font-size:14px;font-weight:700;color:#38bdf8;">Physicochemical Properties</div>
        <table class="propTable" id="propertiesTable">
            <tbody>
                <tr><th>Structure</th><td>1CRN (Crambin)</td></tr>
                <tr><th>Resolution</th><td>1.50 Å (X-Ray Diffraction)</td></tr>
                <tr><th>Molecular Weight</th><td>4720.5 Da</td></tr>
                <tr><th>Total Atoms</th><td>327 Atoms (Chain A)</td></tr>
                <tr><th>Residues</th><td>46 Amino Acids</td></tr>
                <tr><th>Formula</th><td>C202 H315 N55 O64 S6</td></tr>
                <tr><th>Disulfide Bridges</th><td>3 Bonds (CYS3-CYS40, CYS4-CYS32, CYS16-CYS26)</td></tr>
                <tr><th>Isoelectric Point (pI)</th><td>8.85</td></tr>
            </tbody>
        </table>
    </div>

    <!-- ANALYSIS PANEL -->
    <div class="workspacePanel" id="analysisPanel">
        <div style="font-size:14px;font-weight:700;color:#38bdf8;">Active Scientific Analysis</div>
        <div style="margin-top:10px;font-size:12px;color:#94a3b8;">Autonomous Deep Non-Linear Manifold Projection & Energy Convergence</div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;margin-top:14px;">
            <div style="background:rgba(10,31,57,0.6);padding:12px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);">
                <div style="font-size:11px;color:#7dd3fc;font-weight:600;">Deep Latent Space (Kernel PCA)</div>
                <img src="/assets/deep_pca_comparison.png" class="analysisPlotPreview" onerror="this.style.display='none'" />
            </div>
            <div style="background:rgba(10,31,57,0.6);padding:12px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);">
                <div style="font-size:11px;color:#7dd3fc;font-weight:600;">Energy Minimization Trajectory</div>
                <img src="/assets/energy_plot.png" class="analysisPlotPreview" onerror="this.style.display='none'" />
            </div>
        </div>
    </div>
"""

# Insert panels before viewerBottom
html = html.replace('    <div class="viewerBottom">', panels_html + '\n    <div class="viewerBottom">', 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("HTML Structure updated successfully!")

import os

html_path = r"C:\Users\sohel\Downloads\GitHub T1\Polymathix\polymathix_ui\frontend\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Update CDN tags in <head> to three@0.128.0 where all files exist
old_cdn = """<!-- Three.js -->
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/exporters/OBJExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/exporters/STLExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.160.0/examples/js/exporters/GLTFExporter.js"></script>"""

new_cdn = """<!-- Three.js v0.128 (Full Non-Module Suite: OrbitControls & Exporters) -->
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/OBJExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/STLExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/GLTFExporter.js"></script>"""

if old_cdn in html:
    html = html.replace(old_cdn, new_cdn, 1)

# 2. Add Fullscreen CSS for 3D Viewer and Session Modal
fullscreen_css = """
/* ================= FULLSCREEN 3D VIEWER & SESSION MODAL ================= */
.viewer.fullscreenMode {
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    width: 100vw !important;
    height: 100vh !important;
    z-index: 999999 !important;
    margin: 0 !important;
    border-radius: 0 !important;
    background: #010812 !important;
    border: none !important;
    display: flex !important;
    flex-direction: column !important;
}
.viewer.fullscreenMode .canvasWrap {
    flex: 1 !important;
    height: auto !important;
    margin: 0 10px !important;
}

.exitFullscreenBtn {
    position: absolute;
    top: 14px;
    right: 14px;
    z-index: 1000000;
    background: rgba(220, 38, 38, 0.85);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.3);
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 11px;
    font-weight: 600;
    cursor: pointer;
    display: none;
    backdrop-filter: blur(8px);
}
.viewer.fullscreenMode .exitFullscreenBtn {
    display: block !important;
}

/* SESSION FULLSCREEN MODAL */
.sessionModalOverlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    background: rgba(1, 8, 18, 0.88);
    backdrop-filter: blur(20px);
    z-index: 9999999;
    display: none;
    align-items: center;
    justify-content: center;
    padding: 24px;
    box-sizing: border-box;
}
.sessionModalOverlay.show {
    display: flex;
}
.sessionModalBox {
    width: 900px;
    max-width: 95vw;
    max-height: 90vh;
    background: linear-gradient(145deg, rgba(8,30,55,0.96), rgba(4,18,34,0.94));
    border: 1px solid rgba(56, 189, 248, 0.35);
    border-radius: 20px;
    box-shadow: 0 0 50px rgba(0, 150, 255, 0.25);
    display: flex;
    flex-direction: column;
    overflow: hidden;
}
.sessionModalHeader {
    padding: 18px 24px;
    border-bottom: 1px solid rgba(90, 178, 255, 0.15);
    display: flex;
    align-items: center;
    justify-content: space-between;
}
.sessionModalBody {
    padding: 24px;
    overflow-y: auto;
    flex: 1;
}
"""

# Insert CSS before </style>
html = html.replace("</style>", fullscreen_css + "\n</style>", 1)

# 3. Add Fullscreen buttons in 3D Viewer Toolbar & Bottom Bar
old_viewer_tools = """        <div class="viewerTools">

            <button class="viewerTool" onclick="resetCamera()">↖</button>
            <button class="viewerTool" onclick="focusMolecule()">◎</button>
            <button class="viewerTool" onclick="toggleSurface()">◉</button>
            <button class="viewerTool" onclick="randomizeMolecule()">✣</button>
            <button class="viewerTool" onclick="showToast('Binding site selected','4 Å interaction radius applied')">⌖</button>
            <button class="viewerTool" onclick="takeSnapshot()">▣</button>
            <button class="viewerTool" onclick="openExport()">↓</button>

        </div>"""

new_viewer_tools = """        <div class="viewerTools">
            <button class="viewerTool" onclick="resetCamera()" title="Reset Camera View">↖</button>
            <button class="viewerTool" onclick="focusMolecule()" title="Focus Center">◎</button>
            <button class="viewerTool" onclick="toggleSurface()" title="Toggle Molecular Surface">◉</button>
            <button class="viewerTool" onclick="randomizeMolecule()" title="Reorient Structure">✣</button>
            <button class="viewerTool" onclick="showToast('Active Site Contact Network','Cutoff 4.0 Å active')" title="Active Pocket">⌖</button>
            <button class="viewerTool" onclick="takeSnapshot()" title="Download PNG Snapshot">📷</button>
            <button class="viewerTool" onclick="toggleViewerFullscreen()" title="Fullscreen 3D View">⛶</button>
            <button class="viewerTool" onclick="openExport()" title="Export 3D Geometry">↓</button>
        </div>
        <button class="exitFullscreenBtn" onclick="toggleViewerFullscreen()">✕ Exit Fullscreen (Esc)</button>"""

if old_viewer_tools in html:
    html = html.replace(old_viewer_tools, new_viewer_tools, 1)

# Replace ⛶ in viewerBottom with toggleViewerFullscreen()
html = html.replace("""        <button class="controlBtn" onclick="openExport()">
            ⛶
        </button>""", """        <button class="controlBtn" onclick="toggleViewerFullscreen()" title="Fullscreen 3D Mode">
            ⛶ Fullscreen 3D
        </button>""", 1)

# 4. Add Fullscreen Session button to Agent Panel
old_agent_header = """    <div class="panelTitle">

        <span>🧠 AI Agent Control Center</span>

        <span class="status">"""

new_agent_header = """    <div class="panelTitle">
        <span>🧠 AI Agent Control Center</span>
        <button class="controlBtn" onclick="openSessionModal()" style="margin-left:auto;margin-right:8px;padding:3px 8px;font-size:10px;" title="Deep Dive Fullscreen Session">⛶ Fullscreen Session</button>
        <span class="status">"""

if old_agent_header in html:
    html = html.replace(old_agent_header, new_agent_header, 1)

# 5. Add the Session Fullscreen Modal DOM
session_modal_html = """
<!-- ================= SESSION DEEP DIVE FULLSCREEN MODAL ================= -->
<div class="sessionModalOverlay" id="sessionModalOverlay">
    <div class="sessionModalBox">
        <div class="sessionModalHeader">
            <div style="display:flex;align-items:center;gap:12px;">
                <span style="font-size:22px;">🧠</span>
                <div>
                    <div style="font-size:16px;font-weight:700;color:#f8fafc;" id="modalSessionTitle">Research Session: MembraneONE</div>
                    <div style="font-size:11px;color:#38bdf8;" id="modalSessionSubtitle">Protocol: Membrane MD v2.4 | Model: AI Research Agent</div>
                </div>
            </div>
            <button class="modalClose" onclick="closeSessionModal()" style="font-size:20px;cursor:pointer;background:none;border:none;color:#94a3b8;">✕</button>
        </div>
        <div class="sessionModalBody">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-bottom:20px;">
                <div style="background:rgba(10,31,57,0.6);padding:16px;border-radius:12px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:11px;color:#7dd3fc;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Active Protocol & Target</div>
                    <div style="font-size:18px;font-weight:700;margin-top:6px;color:#fff;" id="modalProtocolName">Membrane MD v2.4</div>
                    <div style="font-size:12px;color:#94a3b8;margin-top:4px;">POPC Lipid Bilayer | AMBER14 Force Field | Solvation pH 7.4</div>
                </div>
                <div style="background:rgba(10,31,57,0.6);padding:16px;border-radius:12px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:11px;color:#7dd3fc;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Computational Status</div>
                    <div style="font-size:18px;font-weight:700;margin-top:6px;color:#00f59b;" id="modalSessionStatus">● Active Running</div>
                    <div style="font-size:12px;color:#94a3b8;margin-top:4px;" id="modalTimeRemaining">Estimated time remaining: 1h 45m</div>
                </div>
            </div>

            <!-- Workflow Checklist -->
            <div style="font-size:13px;font-weight:700;color:#e2e8f0;margin-bottom:10px;">Automated Protocol Execution Pipeline</div>
            <div id="modalWorkflowSteps" style="display:flex;flex-direction:column;gap:8px;">
                <!-- Populated dynamically -->
            </div>

            <!-- Controls in Modal -->
            <div style="display:flex;gap:10px;margin-top:24px;border-top:1px solid rgba(90,178,255,0.15);padding-top:18px;">
                <button class="quickBtn" onclick="triggerAgentControl('pause')">⏸ Pause Session</button>
                <button class="quickBtn" onclick="triggerAgentControl('stop')">■ Stop Session</button>
                <button class="quickBtn" onclick="triggerAgentControl('run')">▶ Resume Execution</button>
                <button class="quickBtn" style="margin-left:auto;" onclick="triggerQuickAction('create_report')">▤ Export Dossier</button>
            </div>
        </div>
    </div>
</div>
"""

# Insert modal before </body>
html = html.replace("</body>", session_modal_html + "\n</body>", 1)

# 6. JavaScript Functions for Fullscreen & Fallback Mouse Orbit
js_additions = """
/* ================= FULLSCREEN & SESSION MODAL LOGIC ================= */

function toggleViewerFullscreen(){
    const viewer = document.querySelector('.viewer');
    if (!viewer) return;
    
    viewer.classList.toggle('fullscreenMode');
    const isFull = viewer.classList.contains('fullscreenMode');
    
    showToast('3D Viewer', isFull ? 'Fullscreen 3D Mode Activated (Esc to exit)' : 'Normal View Restored');
    
    setTimeout(() => {
        resizeThree();
    }, 100);
}

function openSessionModal(){
    const overlay = document.getElementById('sessionModalOverlay');
    if (!overlay) return;

    // Sync titles
    const sName = document.getElementById('sessionNameDisplay')?.innerText || 'MembraneONE';
    const pName = document.getElementById('protocolNameDisplay')?.innerText || 'Membrane MD v2.4';
    
    document.getElementById('modalSessionTitle').innerText = 'Research Session: ' + sName;
    document.getElementById('modalSessionSubtitle').innerText = 'Protocol: ' + pName + ' | Model: AI Research Agent';
    document.getElementById('modalProtocolName').innerText = pName;
    
    // Copy steps
    const stepsSrc = document.querySelector('.workflow');
    const stepsDst = document.getElementById('modalWorkflowSteps');
    if (stepsSrc && stepsDst) {
        stepsDst.innerHTML = stepsSrc.innerHTML.replace('<div class="workflowTitle">Workflow Steps</div>', '');
    }

    overlay.classList.add('show');
}

function closeSessionModal(){
    const overlay = document.getElementById('sessionModalOverlay');
    if (overlay) overlay.classList.remove('show');
}

// ESC Key closes fullscreens and modals
document.addEventListener('keydown', function(e){
    if (e.key === 'Escape') {
        const viewer = document.querySelector('.viewer');
        if (viewer && viewer.classList.contains('fullscreenMode')) {
            viewer.classList.remove('fullscreenMode');
            resizeThree();
        }
        closeSessionModal();
        closeExport();
    }
});

/* ================= FAIL-SAFE MOUSE ORBIT FALLBACK ================= */
function setupSimpleControls(cam, domElem){
    let isDragging = false;
    let prevMouse = { x: 0, y: 0 };
    
    domElem.addEventListener('mousedown', function(e){
        isDragging = true;
        prevMouse = { x: e.clientX, y: e.clientY };
    });
    
    window.addEventListener('mouseup', function(){ isDragging = false; });
    
    window.addEventListener('mousemove', function(e){
        if (!isDragging || !moleculeGroup) return;
        const deltaX = e.clientX - prevMouse.x;
        const deltaY = e.clientY - prevMouse.y;
        
        moleculeGroup.rotation.y += deltaX * 0.008;
        moleculeGroup.rotation.x += deltaY * 0.008;
        
        prevMouse = { x: e.clientX, y: e.clientY };
    });
    
    domElem.addEventListener('wheel', function(e){
        if (!cam) return;
        cam.position.z += e.deltaY * 0.02;
        cam.position.z = Math.max(5, Math.min(150, cam.position.z));
    }, { passive: true });
}
"""

html = html.replace("</script>", js_additions + "\n</script>", 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Viewer, Fullscreen & Session modal logic successfully applied!")

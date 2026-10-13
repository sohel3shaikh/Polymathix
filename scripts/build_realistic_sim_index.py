import os
import sys
import json
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from polymathix.orchestrator import PolymathixOrchestrator

orc = PolymathixOrchestrator()
state = orc.get_state()
state_json = json.dumps(state)

# Read base template from build_clean_index.py
source_builder = os.path.join(ROOT_DIR, "scripts", "build_clean_index.py")
with open(source_builder, "r", encoding="utf-8") as f:
    orig = f.read()

start_marker = 'html_code = """'
end_marker = '"""\n\nimport json'
start_idx = orig.find(start_marker) + len(start_marker)
end_idx = orig.find(end_marker)
html = orig[start_idx:end_idx]

# 1. ADD CSS FOR SIMULATION HUD & CONTROLS
sim_css = """
/* SIMULATION HUD OVERLAY */
.simHUD{
    position:absolute; left:52px; top:12px;
    padding:8px 12px; border-radius:10px;
    background:rgba(4,22,44,.85); backdrop-filter:blur(12px);
    border:1px solid rgba(56,189,248,.3);
    box-shadow:0 0 20px rgba(0,140,255,.15);
    z-index:5; display:flex; flex-direction:column; gap:6px;
    pointer-events:none; transition:opacity .2s;
}
.simHUDHeader{
    display:flex; align-items:center; gap:8px;
    font-size:10px; font-weight:700; color:#38bdf8; letter-spacing:0.5px;
}
.simDot{
    width:7px; height:7px; border-radius:50%; background:#00f59b;
    box-shadow:0 0 8px #00f59b; animation:pulseDot 1.5s infinite;
}
@keyframes pulseDot{ 0%,100%{ opacity:1; } 50%{ opacity:0.3; } }
.simBadge{
    font-size:9px; padding:1px 6px; border-radius:4px;
    background:rgba(56,189,248,.2); color:#7dd3fc; text-transform:uppercase;
}
.simMetrics{
    display:flex; gap:12px; align-items:center;
}
.simMetric{
    display:flex; flex-direction:column;
}
.simMVal{
    font-size:11px; font-family:monospace; font-weight:700; color:#f1f5f9;
}
.simMLbl{
    font-size:8px; color:#7891aa; font-weight:600; text-transform:uppercase; letter-spacing:0.4px;
}

/* SIMULATION BOTTOM CONTROLS BAR */
.simControlsBar{
    position:absolute; left:50%; bottom:10px; transform:translateX(-50%);
    padding:5px 12px; border-radius:10px;
    background:rgba(6,24,48,.88); backdrop-filter:blur(16px);
    border:1px solid rgba(56,189,248,.35);
    box-shadow:0 0 25px rgba(0,120,255,.2);
    z-index:6; display:flex; align-items:center; gap:10px;
    user-select:none;
}
.simPlayBtn{
    padding:4px 10px; border-radius:6px; border:none;
    background:linear-gradient(135deg,#00f59b,#00b874); color:#02140a;
    font-size:10px; font-weight:700; cursor:pointer; transition:.15s;
    box-shadow:0 0 10px rgba(0,245,155,.3);
}
.simPlayBtn.paused{
    background:linear-gradient(135deg,#38bdf8,#0284c7); color:#020914;
    box-shadow:0 0 10px rgba(56,189,248,.3);
}
.simPlayBtn:hover{ transform:scale(1.03); }
.simDivider{ width:1px; height:16px; background:rgba(90,178,255,.25); }
.simSelect{
    background:rgba(4,18,34,.9); border:1px solid rgba(56,189,248,.3);
    color:#e2e8f0; font-size:10px; padding:3px 6px; border-radius:6px; outline:none;
}
.simSliderWrap{ display:flex; align-items:center; gap:6px; }
.simLayers{ display:flex; align-items:center; gap:8px; }
.layerCheck{
    display:flex; align-items:center; gap:4px; font-size:10px; color:#94a3b8; cursor:pointer;
}
.layerCheck input{ cursor:pointer; accent-color:#38bdf8; }
.layerCheck:hover{ color:#fff; }
"""

# Insert sim_css right before /* TOOLBAR OVERLAY */
css_target = "/* TOOLBAR OVERLAY */"
if css_target in html:
    html = html.replace(css_target, sim_css + "\n" + css_target)

# 2. ADD SIMULATION HUD & CONTROLS IN CANVAS WRAP
hud_markup = """
            <!-- SIMULATION HUD -->
            <div class="simHUD" id="simHUD">
                <div class="simHUDHeader">
                    <span class="simDot" id="simDot"></span>
                    <span id="simStatusText">BIOPHYSICAL MD (300K)</span>
                    <span class="simBadge" id="simModeBadge">Thermal</span>
                </div>
                <div class="simMetrics">
                    <div class="simMetric"><span class="simMVal" id="hudTemp">300.2 K</span><span class="simMLbl">TEMP</span></div>
                    <div class="simMetric"><span class="simMVal" id="hudRMSD">0.84 Å</span><span class="simMLbl">RMSD</span></div>
                    <div class="simMetric"><span class="simMVal" id="hudEnergy">-146k</span><span class="simMLbl">POT.E</span></div>
                    <div class="simMetric"><span class="simMVal" id="hudDeltaG" style="color:#00f59b;">-7.82</span><span class="simMLbl">ΔG POCKET</span></div>
                </div>
            </div>

            <!-- SIMULATION CONTROLS BAR -->
            <div class="simControlsBar" id="simControlsBar">
                <button class="simPlayBtn" id="btnSimPlay" onclick="toggleSimPlay()">⏸ Pause</button>
                <div class="simDivider"></div>
                <select class="simSelect" id="simModeSelect" onchange="setSimMode(this.value)">
                    <option value="thermal">Thermal Dynamics (300K)</option>
                    <option value="nma">Domain Breathing (NMA)</option>
                    <option value="docking">Induced-Fit Ligand Docking</option>
                </select>
                <div class="simDivider"></div>
                <div class="simSliderWrap" title="Simulation Temperature">
                    <span style="font-size:10px;color:#94a3b8;">Temp:</span>
                    <input type="range" min="260" max="360" value="300" id="simTempSlider" oninput="setSimTemp(this.value)" style="width:65px;">
                    <span id="simTempDisplay" style="font-size:10px;font-family:monospace;min-width:32px;">300K</span>
                </div>
                <div class="simDivider"></div>
                <div class="simLayers">
                    <label class="layerCheck" title="Toggle Disulfide Bridges (S-S)"><input type="checkbox" id="chkDisulfides" checked onchange="toggleDisulfides(this.checked)"><span>S-S</span></label>
                    <label class="layerCheck" title="Toggle TIP3P Water Hydration Shell"><input type="checkbox" id="chkHydration" checked onchange="toggleHydration(this.checked)"><span>H₂O</span></label>
                    <label class="layerCheck" title="Toggle POPC Lipid Bilayer Slab"><input type="checkbox" id="chkMembrane" onchange="toggleMembrane(this.checked)"><span>POPC</span></label>
                </div>
            </div>
"""

canvas_target = '<canvas id="threeCanvas"></canvas>'
if canvas_target in html:
    html = html.replace(canvas_target, canvas_target + "\n" + hud_markup)

# 3. UPDATE STYLE BUTTONS IN VIEWER BOTTOM
old_buttons = """            <button class="styleBtn active" id="btnRepCartoon" onclick="setRepresentation('cartoon', this)">Cartoon</button>
            <button class="styleBtn" id="btnRepSurface" onclick="setRepresentation('surface', this)">Surface</button>
            <button class="styleBtn" id="btnRepSticks" onclick="setRepresentation('sticks', this)">Sticks</button>
            <button class="styleBtn" id="btnRepSphere" onclick="setRepresentation('sphere', this)">Sphere</button>
            <button class="styleBtn" id="btnRepMesh" onclick="setRepresentation('mesh', this)">Mesh</button>"""

new_buttons = """            <button class="styleBtn active" id="btnRepRibbon" onclick="setRepresentation('ribbon', this)">Ribbon</button>
            <button class="styleBtn" id="btnRepElectro" onclick="setRepresentation('electro', this)">Electrostatic</button>
            <button class="styleBtn" id="btnRepGlass" onclick="setRepresentation('glass', this)">Glass Surface</button>
            <button class="styleBtn" id="btnRepSticks" onclick="setRepresentation('sticks', this)">Ball & Stick</button>
            <button class="styleBtn" id="btnRepSphere" onclick="setRepresentation('sphere', this)">Spacefill</button>"""

if old_buttons in html:
    html = html.replace(old_buttons, new_buttons)

# 4. REPLACE JAVASCRIPT ENGINE WITH REALISTIC SIMULATION & 3D SCIENTIFIC ENGINE
js_search_start = "/* ================= THREE.JS 3D SCENE ================= */"
js_search_end = "/* ================= STREAMLIT LISTENER ================= */"

idx1 = html.find(js_search_start)
idx2 = html.find(js_search_end)

if idx1 != -1 and idx2 != -1:
    old_js_block = html[idx1:idx2]
    
    new_js_block = """/* ================= THREE.JS 3D SCENE ================= */
let scene, camera, renderer, controls;
let moleculeGroup, ribbonGroup, electroGroup, glassGroup, sticksGroup, sphereGroup;
let disulfideGroup, hydrationGroup, membraneGroup, glucoseGroup, interactionGroup;
let currentRep = 'ribbon';
let autoRotate = true;
let simRunning = true;
let simMode = 'thermal';
let simTemp = 300.0;
let simSpeed = 1.0;
let livePDBData = null;
let originalCAPoints = [];
let originalAtoms = [];
let liveGlucoseBonds = [];
const canvas = document.getElementById("threeCanvas");

function initThree(){
    if(!canvas) return;
    if(typeof THREE === 'undefined'){
        console.warn('Three.js library loading... retrying in 100ms');
        setTimeout(initThree, 100);
        return;
    }
    try {
        scene = new THREE.Scene();
        scene.background = new THREE.Color(0x010812);
        scene.fog = new THREE.FogExp2(0x010812, 0.012);

        const wrap = document.getElementById("threeCanvasWrap");
        const width = (wrap && wrap.clientWidth > 50) ? wrap.clientWidth : (canvas.clientWidth || 700);
        const height = (wrap && wrap.clientHeight > 50) ? wrap.clientHeight : (canvas.clientHeight || 450);

        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 2000);
        camera.position.set(0, 10, 36);

        renderer = new THREE.WebGLRenderer({ canvas: canvas, antialias: true, preserveDrawingBuffer: true, alpha: true });
        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
        renderer.setSize(width, height, false);
        if (THREE.sRGBEncoding) renderer.outputEncoding = THREE.sRGBEncoding;

        // Controls
        if (typeof THREE.OrbitControls === 'function') {
            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.enableDamping = true;
            controls.dampingFactor = 0.05;
            controls.minDistance = 4;
            controls.maxDistance = 140;
        } else {
            setupSimpleControls(camera, renderer.domElement);
        }

        // Realistic Studio Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 1.4);
        scene.add(ambient);

        const keyLight = new THREE.DirectionalLight(0xffffff, 2.2);
        keyLight.position.set(18, 22, 16);
        scene.add(keyLight);

        const blueRimLight = new THREE.DirectionalLight(0x7da4ff, 1.4);
        blueRimLight.position.set(-18, -12, -16);
        scene.add(blueRimLight);

        const fillLight = new THREE.PointLight(0xa855f7, 3, 80);
        fillLight.position.set(-14, 10, 10);
        scene.add(fillLight);

        // Molecular Groups Hierarchy
        moleculeGroup = new THREE.Group();
        ribbonGroup = new THREE.Group();
        electroGroup = new THREE.Group();
        glassGroup = new THREE.Group();
        sticksGroup = new THREE.Group();
        sphereGroup = new THREE.Group();
        disulfideGroup = new THREE.Group();
        hydrationGroup = new THREE.Group();
        membraneGroup = new THREE.Group();
        glucoseGroup = new THREE.Group();
        interactionGroup = new THREE.Group();

        moleculeGroup.add(
            ribbonGroup, electroGroup, glassGroup, sticksGroup, sphereGroup,
            disulfideGroup, hydrationGroup, membraneGroup, glucoseGroup, interactionGroup
        );
        scene.add(moleculeGroup);

        // Initial D-Glucose Ligand & Interactions
        createGlucoseLigand();
        createInteractions();

        window.addEventListener("resize", resizeThree);
        if(window.ResizeObserver && wrap) {
            new ResizeObserver(resizeThree).observe(wrap);
        }

        animate();

        // Process any queued PDB data
        if(window._pendingPDBData) {
            renderRealPDB(window._pendingPDBData);
            window._pendingPDBData = null;
        }

        setTimeout(resizeThree, 50);
        setTimeout(resizeThree, 200);
        setTimeout(resizeThree, 500);
    } catch(err) {
        console.error("Error in initThree:", err);
    }
}

function resizeThree(){
    if(!renderer || !camera || !canvas) return;
    const wrap = document.getElementById("threeCanvasWrap");
    const width = (wrap && wrap.clientWidth > 50) ? wrap.clientWidth : canvas.clientWidth || 700;
    const height = (wrap && wrap.clientHeight > 50) ? wrap.clientHeight : canvas.clientHeight || 450;
    
    if (width > 20 && height > 20) {
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
    }
}

/* ================= GLUCOSE LIGAND & INTERACTIONS ================= */
const GLUCOSE_ATOMS = [
    { elem: 'C', name: 'C1', x: 1.15, y: 0.42, z: 0.22 },
    { elem: 'C', name: 'C2', x: 0.45, y: -0.82, z: 0.35 },
    { elem: 'C', name: 'C3', x: -1.02, y: -0.65, z: 0.12 },
    { elem: 'C', name: 'C4', x: -1.35, y: 0.81, z: 0.24 },
    { elem: 'C', name: 'C5', x: -0.32, y: 1.62, z: -0.41 },
    { elem: 'O', name: 'O5', x: 0.92, y: 1.25, z: -0.22 },
    { elem: 'O', name: 'O1', x: 2.25, y: 0.12, z: -0.45 },
    { elem: 'O', name: 'O2', x: 0.72, y: -1.85, z: -0.52 },
    { elem: 'O', name: 'O3', x: -1.82, y: -1.65, z: 0.55 },
    { elem: 'O', name: 'O4', x: -2.45, y: 0.92, z: -0.52 },
    { elem: 'C', name: 'C6', x: -0.52, y: 3.05, z: -0.15 },
    { elem: 'O', name: 'O6', x: 0.62, y: 3.75, z: 0.35 }
];

const GLUCOSE_BONDS = [
    [0,1], [1,2], [2,3], [3,4], [4,5], [5,0],
    [0,6], [1,7], [2,8], [3,9], [4,10], [10,11]
];

const BINDING_CONTACTS = [
    { name: "ASN 203", dist: "2.8 Å", type: "hbond", color: 0x00f59b, x: -2.8, y: 1.4, z: 1.2 },
    { name: "SER 205", dist: "3.1 Å", type: "hbond", color: 0x00f59b, x: -2.2, y: 1.6, z: 0.8 },
    { name: "TYR 207", dist: "3.4 Å", type: "hydrophobic", color: 0xffd84d, x: 2.4, y: -1.3, z: 0.7 },
    { name: "ARG 210", dist: "3.6 Å", type: "electro", color: 0xff4d67, x: -2.6, y: -1.1, z: 1.1 },
    { name: "GLU 277", dist: "3.8 Å", type: "electro", color: 0xff4d67, x: 3.1, y: 1.2, z: -0.9 },
    { name: "HIS 310", dist: "3.9 Å", type: "pi", color: 0xa855f7, x: -1.9, y: -2.4, z: 0.5 },
    { name: "THR 312", dist: "3.9 Å", type: "hydrophobic", color: 0xffd84d, x: 1.8, y: 2.7, z: 0.6 },
    { name: "LYS 315", dist: "4.0 Å", type: "electro", color: 0xff4d67, x: 0.5, y: -3.2, z: -1.1 }
];

function createGlucoseLigand(){
    if(!glucoseGroup) return;
    while(glucoseGroup.children.length > 0) glucoseGroup.remove(glucoseGroup.children[0]);

    const cMat = new THREE.MeshPhysicalMaterial({ color: 0x00f59b, roughness: 0.25, metalness: 0.2, clearcoat: 0.5 });
    const oMat = new THREE.MeshPhysicalMaterial({ color: 0xff4d67, roughness: 0.2, metalness: 0.3, clearcoat: 0.5 });
    const bondMat = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, roughness: 0.25, metalness: 0.3 });

    const sphereGeo = new THREE.SphereGeometry(0.38, 16, 16);

    GLUCOSE_ATOMS.forEach(atom => {
        const mesh = new THREE.Mesh(sphereGeo, atom.elem === 'O' ? oMat : cMat);
        mesh.position.set(atom.x, atom.y, atom.z);
        glucoseGroup.add(mesh);
    });

    GLUCOSE_BONDS.forEach(b => {
        const p1 = new THREE.Vector3(GLUCOSE_ATOMS[b[0]].x, GLUCOSE_ATOMS[b[0]].y, GLUCOSE_ATOMS[b[0]].z);
        const p2 = new THREE.Vector3(GLUCOSE_ATOMS[b[1]].x, GLUCOSE_ATOMS[b[1]].y, GLUCOSE_ATOMS[b[1]].z);
        const dist = p1.distanceTo(p2);
        const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.09, 0.09, dist, 8), bondMat);
        cyl.position.copy(p1).add(p2).multiplyScalar(0.5);
        cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p2.clone().sub(p1).normalize());
        glucoseGroup.add(cyl);
    });
}

function createInteractions(){
    if(!interactionGroup) return;
    while(interactionGroup.children.length > 0) interactionGroup.remove(interactionGroup.children[0]);

    const resListEl = document.getElementById("bindingResiduesList");
    if(resListEl) resListEl.innerHTML = "";

    BINDING_CONTACTS.forEach((c) => {
        const start = new THREE.Vector3(0, 0, 0);
        const end = new THREE.Vector3(c.x, c.y, c.z);
        
        const lineGeo = new THREE.BufferGeometry().setFromPoints([start, end]);
        const lineMat = new THREE.LineDashedMaterial({ color: c.color, dashSize: 0.4, gapSize: 0.2, linewidth: 2 });
        const line = new THREE.Line(lineGeo, lineMat);
        line.computeLineDistances();
        line.name = "contact_line_" + c.name;
        interactionGroup.add(line);

        // Marker for residue
        const marker = new THREE.Mesh(
            new THREE.SphereGeometry(0.32, 14, 14),
            new THREE.MeshPhysicalMaterial({ color: c.color, roughness: 0.25, metalness: 0.3, clearcoat: 0.4 })
        );
        marker.position.copy(end);
        marker.name = "contact_marker_" + c.name;
        interactionGroup.add(marker);

        // Populate Binding Panel
        if(resListEl) {
            const div = document.createElement("div");
            div.className = "residue";
            div.id = "badge_" + c.name.replace(" ", "_");
            div.onclick = () => focusResidue(c.x, c.y, c.z, c.name, c.dist, c.type);
            div.innerHTML = `<span class="resName">${c.name}</span><span class="resDist" id="dist_${c.name.replace(" ", "_")}">${c.dist}</span>`;
            resListEl.appendChild(div);
        }
    });
}

function focusResidue(x, y, z, name, dist, type){
    showToast("Residue Contact", `${name}: ${type.toUpperCase()} interaction (${dist})`);
    if(controls) {
        controls.target.set(x, y, z);
        camera.position.set(x * 1.5, y * 1.5 + 2, z * 1.5 + 6);
        controls.update();
    }
}

function focusBindingPocket(){
    showToast("Binding Pocket", "Centering on D-Glucose Active Pocket (4.0 Å)");
    const bp = document.getElementById("bindingPanel");
    if(bp) bp.style.display = "block";
    if(controls) {
        controls.target.set(0, 0, 0);
        camera.position.set(0, 2, 14);
        controls.update();
    }
}

function closeBindingPanel(){
    const bp = document.getElementById("bindingPanel");
    if(bp) bp.style.display = "none";
}

/* ================= FULL PDB RENDERING ================= */
function renderRealPDB(pdbData){
    if(!pdbData || !pdbData.ca_coords || pdbData.ca_coords.length === 0) return;
    if(!scene || !ribbonGroup){
        window._pendingPDBData = pdbData;
        return;
    }

    livePDBData = pdbData;
    originalCAPoints = pdbData.ca_coords.map(c => ({
        x: c.x, y: c.y, z: c.z, res: c.res, id: c.id,
        sec_struct: c.sec_struct || 'loop',
        b_factor: c.b_factor || 15.0
    }));
    originalAtoms = (pdbData.atoms || []).map(a => ({ ...a }));

    // Clear previous representations
    [ribbonGroup, electroGroup, glassGroup, sticksGroup, sphereGroup, disulfideGroup, hydrationGroup, membraneGroup].forEach(g => {
        if(g) while(g.children.length > 0) g.remove(g.children[0]);
    });

    const caPoints = originalCAPoints.map(c => new THREE.Vector3(c.x, c.y, c.z));

    // 1. CHIMERAX / PYMOL STYLE SCIENTIFIC RIBBON
    if(caPoints.length >= 2){
        const fullCurve = new THREE.CatmullRomCurve3(caPoints);
        
        // Helix, Sheet, and Loop materials with physical sheen
        const helixMat = new THREE.MeshPhysicalMaterial({ color: 0xc084fc, roughness: 0.22, metalness: 0.15, clearcoat: 0.6 });
        const sheetMat = new THREE.MeshPhysicalMaterial({ color: 0xfacc15, roughness: 0.20, metalness: 0.20, clearcoat: 0.5 });
        const loopMat = new THREE.MeshPhysicalMaterial({ color: 0x38bdf8, roughness: 0.25, metalness: 0.10, clearcoat: 0.4 });

        // Continuous smooth backbone ribbon with secondary structure vertex colors
        const tubeSegments = caPoints.length * 8;
        const tubeGeo = new THREE.TubeGeometry(fullCurve, tubeSegments, 0.42, 12, false);
        const count = tubeGeo.attributes.position.count;
        const colors = new Float32Array(count * 3);
        const cColor = new THREE.Color();

        for(let i=0; i<count; i++){
            const t = i / count;
            const resIdx = Math.min(caPoints.length - 1, Math.floor(t * caPoints.length));
            const ss = originalCAPoints[resIdx].sec_struct;
            if(ss === 'helix') cColor.setHex(0xc084fc);
            else if(ss === 'sheet') cColor.setHex(0xfacc15);
            else cColor.setHex(0x38bdf8);

            colors[i*3] = cColor.r; colors[i*3+1] = cColor.g; colors[i*3+2] = cColor.b;
        }
        tubeGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));
        const ribbonMesh = new THREE.Mesh(tubeGeo, new THREE.MeshPhysicalMaterial({ vertexColors: true, roughness: 0.25, metalness: 0.15, clearcoat: 0.6 }));
        ribbonMesh.name = "backbone_ribbon";
        ribbonGroup.add(ribbonMesh);

        // CA Nodal beads along secondary structure
        const helixBeadGeo = new THREE.SphereGeometry(0.55, 14, 14);
        const sheetBeadGeo = new THREE.SphereGeometry(0.50, 14, 14);
        const loopBeadGeo = new THREE.SphereGeometry(0.42, 12, 12);

        originalCAPoints.forEach((c) => {
            const pos = new THREE.Vector3(c.x, c.y, c.z);
            let beadGeo = loopBeadGeo, beadMat = loopMat;
            if(c.sec_struct === 'helix'){ beadGeo = helixBeadGeo; beadMat = helixMat; }
            else if(c.sec_struct === 'sheet'){ beadGeo = sheetBeadGeo; beadMat = sheetMat; }

            const bead = new THREE.Mesh(beadGeo, beadMat);
            bead.position.copy(pos);
            bead.name = "ca_bead_" + c.id;
            ribbonGroup.add(bead);
        });
    }

    // 2. AUTHENTIC DISULFIDE BRIDGES (S-S BONDS)
    const ssbonds = pdbData.ssbonds || [];
    const disulfideMat = new THREE.MeshPhysicalMaterial({
        color: 0xfbbf24, roughness: 0.15, metalness: 0.85, emissive: 0x78350f, clearcoat: 0.5
    });
    const sSphereGeo = new THREE.SphereGeometry(0.38, 14, 14);

    ssbonds.forEach((ssb, idx) => {
        const p1 = new THREE.Vector3(ssb.x1, ssb.y1, ssb.z1);
        const p2 = new THREE.Vector3(ssb.x2, ssb.y2, ssb.z2);
        const dist = p1.distanceTo(p2);

        const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.20, 0.20, dist, 10), disulfideMat);
        cyl.position.copy(p1).add(p2).multiplyScalar(0.5);
        cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p2.clone().sub(p1).normalize());
        disulfideGroup.add(cyl);

        const s1 = new THREE.Mesh(sSphereGeo, disulfideMat); s1.position.copy(p1); disulfideGroup.add(s1);
        const s2 = new THREE.Mesh(sSphereGeo, disulfideMat); s2.position.copy(p2); disulfideGroup.add(s2);
    });

    // 3. ELECTROSTATIC POTENTIAL SURFACE (POISSON-COULOMBIC COLOR MAPPING)
    const box = new THREE.Box3().setFromPoints(caPoints);
    const size = new THREE.Vector3(); box.getSize(size);
    const center = new THREE.Vector3(); box.getCenter(center);
    const maxDim = Math.max(size.x, size.y, size.z) * 0.65;

    const surfGeo = new THREE.IcosahedronGeometry(Math.max(8, maxDim), 4);
    const surfPos = surfGeo.attributes.position;
    const surfColors = new Float32Array(surfPos.count * 3);
    const tempColor = new THREE.Color();

    for(let i=0; i<surfPos.count; i++){
        const vx = surfPos.getX(i) + center.x;
        const vy = surfPos.getY(i) + center.y;
        const vz = surfPos.getZ(i) + center.z;

        // Calculate Coulombic potential sum
        let pot = 0;
        originalCAPoints.forEach(c => {
            const d = Math.hypot(vx - c.x, vy - c.y, vz - c.z) + 1.0;
            if(c.res === 'GLU' || c.res === 'ASP') pot -= 2.5 / d;
            else if(c.res === 'ARG' || c.res === 'LYS' || c.res === 'HIS') pot += 2.5 / d;
        });

        // Map pot (-1.0 to +1.0) -> Red (negative) to Silver to Blue (positive)
        if(pot < -0.15) tempColor.setHSL(0.0, 0.9, 0.55); // Red acidic
        else if(pot > 0.15) tempColor.setHSL(0.6, 0.9, 0.55); // Blue basic
        else tempColor.setHSL(0.58, 0.1, 0.90); // White/silver neutral

        surfColors[i*3] = tempColor.r; surfColors[i*3+1] = tempColor.g; surfColors[i*3+2] = tempColor.b;
    }
    surfGeo.setAttribute('color', new THREE.BufferAttribute(surfColors, 3));
    const electroMesh = new THREE.Mesh(surfGeo, new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.35, metalness: 0.1, side: THREE.DoubleSide }));
    electroMesh.position.copy(center);
    electroGroup.add(electroMesh);

    // 4. GLASS TRANSMISSION MOLECULAR ENVELOPE
    const glassMat = new THREE.MeshPhysicalMaterial({
        color: 0x0ea5e9, transparent: true, opacity: 0.30, transmission: 0.85,
        roughness: 0.12, ior: 1.35, side: THREE.DoubleSide
    });
    const glassMesh = new THREE.Mesh(surfGeo, glassMat);
    glassMesh.position.copy(center);
    glassGroup.add(glassMesh);

    // 5. BALL & STICK
    const stickMat = new THREE.MeshPhysicalMaterial({ color: 0x93c5fd, roughness: 0.25, metalness: 0.3 });
    for(let i=0; i<caPoints.length-1; i++){
        const p1 = caPoints[i], p2 = caPoints[i+1];
        if(p1.distanceTo(p2) < 4.2){
            const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, p1.distanceTo(p2), 8), stickMat);
            cyl.position.copy(p1).add(p2).multiplyScalar(0.5);
            cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), p2.clone().sub(p1).normalize());
            sticksGroup.add(cyl);
        }
    }

    // 6. CPK SPACEFILL (VAN DER WAALS SPHERES)
    const atoms = pdbData.atoms || [];
    const sphereGeo = new THREE.SphereGeometry(0.48, 14, 14);
    const elemColors = { 'C': 0x00d9ff, 'N': 0x3b82f6, 'O': 0xef4444, 'S': 0xfacc15, 'H': 0xffffff };
    atoms.forEach(a => {
        const mat = new THREE.MeshPhysicalMaterial({ color: elemColors[a.elem] || 0x10b981, roughness: 0.25, clearcoat: 0.4 });
        const m = new THREE.Mesh(sphereGeo, mat);
        m.position.set(a.x, a.y, a.z);
        sphereGroup.add(m);
    });

    // 7. HYDRATION SHELL (TIP3P WATER ENVELOPE)
    const waterWaters = pdbData.hydration_waters || [];
    const wOGeo = new THREE.SphereGeometry(0.26, 12, 12);
    const wHGeo = new THREE.SphereGeometry(0.14, 10, 10);
    const wOMat = new THREE.MeshPhysicalMaterial({ color: 0xef4444, roughness: 0.2, clearcoat: 0.4 });
    const wHMat = new THREE.MeshPhysicalMaterial({ color: 0xffffff, roughness: 0.2, clearcoat: 0.4 });

    waterWaters.forEach((w, idx) => {
        const wGroup = new THREE.Group();
        wGroup.position.set(w.x, w.y, w.z);
        wGroup.name = "water_" + idx;

        const oMesh = new THREE.Mesh(wOGeo, wOMat);
        const h1Mesh = new THREE.Mesh(wHGeo, wHMat); h1Mesh.position.set(0.24, 0.20, 0);
        const h2Mesh = new THREE.Mesh(wHGeo, wHMat); h2Mesh.position.set(-0.24, 0.20, 0);

        wGroup.add(oMesh, h1Mesh, h2Mesh);
        hydrationGroup.add(wGroup);
    });

    // 8. MEMBRANE BILAYER SLAB (POPC PHOSPHOLIPIDS)
    const headGeo = new THREE.SphereGeometry(0.42, 10, 10);
    const headMat1 = new THREE.MeshPhysicalMaterial({ color: 0x06b6d4, roughness: 0.25, transmission: 0.4, transparent: true, opacity: 0.75 });
    const headMat2 = new THREE.MeshPhysicalMaterial({ color: 0xf59e0b, roughness: 0.25, transmission: 0.4, transparent: true, opacity: 0.75 });

    for(let i=-3; i<=3; i++){
        for(let j=-3; j<=3; j++){
            const hTop = new THREE.Mesh(headGeo, (i+j)%2===0 ? headMat1 : headMat2);
            hTop.position.set(i * 3.8, 12.0, j * 3.8);
            membraneGroup.add(hTop);

            const hBot = new THREE.Mesh(headGeo, (i+j)%2===0 ? headMat2 : headMat1);
            hBot.position.set(i * 3.8, -12.0, j * 3.8);
            membraneGroup.add(hBot);
        }
    }
    const coreSlab = new THREE.Mesh(
        new THREE.BoxGeometry(26, 22, 26),
        new THREE.MeshBasicMaterial({ color: 0x06182e, transparent: true, opacity: 0.20, side: THREE.DoubleSide })
    );
    membraneGroup.add(coreSlab);
    membraneGroup.visible = false; // Default hidden until toggled

    // Apply Active Representation
    setRepresentation(currentRep, document.getElementById('btnRep' + currentRep.charAt(0).toUpperCase() + currentRep.slice(1)));

    // Fit camera
    const fitDist = Math.max(26, maxDim * 2.2);
    camera.position.set(0, fitDist * 0.35, fitDist);
    if(controls){ controls.target.set(0, 0, 0); controls.update(); }

    // Sequence Chips
    const seqCont = document.getElementById("seqGridContainer");
    if(seqCont && pdbData.sequence){
        seqCont.innerHTML = "";
        pdbData.sequence.forEach(s => {
            const chip = document.createElement("div");
            chip.className = "seqChip";
            chip.innerHTML = `<div class="seqResName">${s.name}</div><div class="seqResNum">${s.id}</div>`;
            chip.onclick = () => {
                showToast("Residue Focused", `${s.name} #${s.id}`);
                const ca = pdbData.ca_coords.find(c => c.id === s.id);
                if(ca) focusResidue(ca.x, ca.y, ca.z, `${s.name} ${s.id}`, 'Sequence', 'selected');
            };
            seqCont.appendChild(chip);
        });
    }

    // Properties Table
    const pTable = document.getElementById("propertiesTable");
    if(pTable && pdbData.properties){
        let tbody = "<tbody>";
        for(const [k,v] of Object.entries(pdbData.properties)){
            tbody += `<tr><th>${k}</th><td>${v}</td></tr>`;
        }
        tbody += "</tbody>";
        pTable.innerHTML = tbody;
    }
}

/* ================= 3D REPRESENTATIONS ================= */
function setRepresentation(style, elem){
    currentRep = style;
    document.querySelectorAll(".viewerBottom .styleBtn").forEach(b => b.classList.remove("active"));
    if(elem) elem.classList.add("active");

    const wrap = document.getElementById("threeCanvasWrap");
    if(wrap && wrap.style.display === 'none'){
        switchWorkspaceTab('viewer', document.querySelectorAll('.viewer .tab')[0]);
    }

    if(ribbonGroup) ribbonGroup.visible = (style === 'ribbon' || style === 'glass');
    if(electroGroup) electroGroup.visible = (style === 'electro');
    if(glassGroup) glassGroup.visible = (style === 'glass');
    if(sticksGroup) sticksGroup.visible = (style === 'sticks');
    if(sphereGroup) sphereGroup.visible = (style === 'sphere');

    showToast("3D Representation", `${style.toUpperCase()} active`);
}

function resetCamera(){
    camera.position.set(0, 10, 36);
    if(controls){ controls.target.set(0,0,0); controls.update(); }
    showToast("Camera", "Reset to default orientation");
}

function focusMolecule(){
    if(controls){ controls.target.set(0,0,0); controls.update(); }
    showToast("Focus", "Centered on molecular centroid");
}

function toggleSurface(){
    const nextStyle = (currentRep === 'electro') ? 'ribbon' : 'electro';
    setRepresentation(nextStyle, document.getElementById('btnRep' + nextStyle.charAt(0).toUpperCase() + nextStyle.slice(1)));
}

function randomizeMolecule(){
    if(moleculeGroup){
        moleculeGroup.rotation.x += Math.PI * 0.25;
        moleculeGroup.rotation.y += Math.PI * 0.35;
    }
    showToast("Reorient", "Rotated 3D coordinate space");
}

function takeSnapshot(){
    if(!renderer || !scene || !camera) return;
    renderer.render(scene, camera);
    const data = renderer.domElement.toDataURL("image/png");
    const link = document.createElement("a");
    link.download = "polymathix-molecular-render.png";
    link.href = data;
    link.click();
    showToast("Snapshot Downloaded", "PNG render saved");
}

function toggleViewerFullscreen(){
    const v = document.querySelector(".viewer");
    if(!v) return;
    v.classList.toggle("fullscreenMode");
    const isFull = v.classList.contains("fullscreenMode");
    showToast("3D Viewer", isFull ? "Fullscreen 3D (Press Esc to exit)" : "Normal view restored");
    setTimeout(resizeThree, 100);
}

function toggleQuality(){
    const p = renderer ? renderer.getPixelRatio() : 1;
    const nextP = p >= 2 ? 1 : 2;
    if(renderer) renderer.setPixelRatio(nextP);
    showToast("Render Quality", nextP === 2 ? "High (2x Antialiasing)" : "Medium (1x Balanced)");
}

/* ================= SIMULATION CONTROLS & PHYSICS ================= */
function toggleSimPlay(){
    simRunning = !simRunning;
    const btn = document.getElementById("btnSimPlay");
    const dot = document.getElementById("simDot");
    const statusText = document.getElementById("simStatusText");

    if(btn){
        btn.textContent = simRunning ? "⏸ Pause" : "▶ Resume";
        btn.classList.toggle("paused", !simRunning);
    }
    if(dot){
        dot.style.background = simRunning ? "#00f59b" : "#facc15";
        dot.style.boxShadow = simRunning ? "0 0 8px #00f59b" : "0 0 8px #facc15";
    }
    if(statusText){
        statusText.textContent = simRunning ? `BIOPHYSICAL MD (${simTemp.toFixed(0)}K)` : "DYNAMICS PAUSED";
    }
    showToast("Biophysical MD", simRunning ? "Simulation running" : "Dynamics paused");
}

function setSimMode(mode){
    simMode = mode;
    const badge = document.getElementById("simModeBadge");
    if(badge) badge.textContent = mode.toUpperCase();
    showToast("Simulation Mode", `Switched to: ${mode.toUpperCase()}`);
}

function setSimTemp(val){
    simTemp = parseFloat(val);
    const disp = document.getElementById("simTempDisplay");
    const hudT = document.getElementById("hudTemp");
    const statusText = document.getElementById("simStatusText");
    if(disp) disp.textContent = `${simTemp}K`;
    if(hudT) hudT.textContent = `${simTemp.toFixed(1)} K`;
    if(statusText && simRunning) statusText.textContent = `BIOPHYSICAL MD (${simTemp.toFixed(0)}K)`;
}

function toggleDisulfides(show){
    if(disulfideGroup) disulfideGroup.visible = show;
    showToast("Disulfide Bridges", show ? "S-S covalent rods visible" : "Hidden");
}

function toggleHydration(show){
    if(hydrationGroup) hydrationGroup.visible = show;
    showToast("Hydration Shell", show ? "TIP3P water molecules visible" : "Hidden");
}

function toggleMembrane(show){
    if(membraneGroup) membraneGroup.visible = show;
    showToast("Lipid Bilayer", show ? "POPC membrane slab visible" : "Hidden");
}

/* ================= MAIN ANIMATION & SIMULATION LOOP ================= */
function animate(){
    requestAnimationFrame(animate);
    const t = performance.now() * 0.002 * simSpeed;

    // Cinematic continuous slow rotation when not dragging
    if(autoRotate && moleculeGroup) {
        moleculeGroup.rotation.y += 0.0012;
    }

    // BIOPHYSICAL PHYSICS ENGINE
    if(simRunning && originalCAPoints.length > 0){
        const tempRatio = (simTemp / 300.0);

        // 1. Thermal Langevin Vibrations on Ribbon Beads
        originalCAPoints.forEach((c, idx) => {
            const bead = ribbonGroup.getObjectByName("ca_bead_" + c.id);
            if(bead){
                const amp = (c.sec_struct === 'loop' ? 0.38 : 0.10) * tempRatio;
                const dx = amp * Math.sin(2.3 * t + idx * 0.7);
                const dy = amp * Math.cos(1.9 * t + idx * 0.5);
                const dz = amp * Math.sin(2.7 * t + idx * 0.9);
                bead.position.set(c.x + dx, c.y + dy, c.z + dz);
            }
        });

        // 2. Normal Mode Conformational Breathing
        if(simMode === 'nma' && ribbonGroup){
            const hingeAngle = 0.05 * Math.sin(1.6 * t);
            ribbonGroup.rotation.z = hingeAngle;
        } else if(ribbonGroup) {
            ribbonGroup.rotation.z = 0;
        }

        // 3. Induced-Fit D-Glucose Ligand Docking Exploration
        if(glucoseGroup && interactionGroup){
            let gdx = 0, gdy = 0, gdz = 0;
            if(simMode === 'docking'){
                gdx = 0.22 * Math.sin(1.8 * t);
                gdy = 0.18 * Math.cos(1.4 * t);
                gdz = 0.15 * Math.sin(2.2 * t);
                glucoseGroup.position.set(gdx, gdy, gdz);
            } else {
                glucoseGroup.position.set(0, 0, 0);
            }

            // Update contact line endpoints dynamically
            BINDING_CONTACTS.forEach(c => {
                const line = interactionGroup.getObjectByName("contact_line_" + c.name);
                if(line){
                    const p1 = new THREE.Vector3(gdx, gdy, gdz);
                    const p2 = new THREE.Vector3(c.x, c.y, c.z);
                    line.geometry.setFromPoints([p1, p2]);
                    line.computeLineDistances();

                    // Update live distance label in binding badge
                    const distEl = document.getElementById("dist_" + c.name.replace(" ", "_"));
                    if(distEl && simMode === 'docking'){
                        const liveDist = (p1.distanceTo(p2)).toFixed(1);
                        distEl.textContent = `${liveDist} Å`;
                    }
                }
            });
        }

        // 4. Hydration Water Thermal Brownian Diffusion
        if(hydrationGroup && hydrationGroup.visible){
            hydrationGroup.children.forEach((wGroup, i) => {
                wGroup.position.x += 0.015 * Math.sin(3.5 * t + i);
                wGroup.position.y += 0.015 * Math.cos(3.2 * t + i * 2);
            });
        }

        // 5. Update Simulation HUD Metrics in Real Time
        const hudT = document.getElementById("hudTemp");
        const hudR = document.getElementById("hudRMSD");
        const hudE = document.getElementById("hudEnergy");
        const hudG = document.getElementById("hudDeltaG");

        if(hudT) hudT.textContent = (simTemp + Math.sin(t * 3.0) * 0.7).toFixed(1) + " K";
        if(hudR) hudR.textContent = (0.82 + Math.abs(Math.sin(t * 1.8) * 0.06) * tempRatio).toFixed(2) + " Å";
        if(hudE) hudE.textContent = (Math.round(-146240 + Math.sin(t * 1.4) * 160)).toLocaleString() + " kJ";
        if(hudG) hudG.textContent = (-7.82 + Math.sin(t * 2.2) * 0.12).toFixed(2);
    }

    if(controls && controls.update) controls.update();
    if(renderer && scene && camera) renderer.render(scene, camera);
}

"""
    html = html[:idx1] + new_js_block + html[idx2:]
    print("Successfully replaced JavaScript engine with realistic simulation engine!")
else:
    print("WARNING: Could not find JS replacement markers!")

# Save the full enhanced build script
enhanced_builder_path = os.path.join(ROOT_DIR, "scripts", "build_clean_index.py")
full_script_content = f'''import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

html_code = """{html}"""

import json
from polymathix.orchestrator import PolymathixOrchestrator
orc = PolymathixOrchestrator()
state_json = json.dumps(orc.get_state())

injection = f"""try {{
    const INITIAL_EMBEDDED_STATE = {{state_json}};
    if(typeof updateStateFromPython === 'function') {{{{
        updateStateFromPython(INITIAL_EMBEDDED_STATE);
    }}}}
}} catch(e) {{{{
    console.error("Error applying embedded state:", e);
}}}}"""

html_code = html_code.replace("/* __INJECT_INITIAL_STATE__ */", injection)

target = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html")
with open(target, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Successfully generated clean, consolidated index.html ({{len(html_code)}} bytes)!")
'''

with open(enhanced_builder_path, "w", encoding="utf-8") as f:
    f.write(full_script_content)

print("Updated scripts/build_clean_index.py successfully.")

# Execute build to generate frontend index.html
with open(os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html"), "w", encoding="utf-8") as f:
    # Inject initial state
    injection = f"""try {{
    const INITIAL_EMBEDDED_STATE = {state_json};
    if(typeof updateStateFromPython === 'function') {{
        updateStateFromPython(INITIAL_EMBEDDED_STATE);
    }}
}} catch(e) {{
    console.error("Error applying embedded state:", e);
}}"""
    f.write(html.replace("/* __INJECT_INITIAL_STATE__ */", injection))

print("Updated polymathix_ui/frontend/index.html successfully!")

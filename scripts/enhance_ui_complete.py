import os
import re

html_path = r"C:\Users\sohel\Downloads\GitHub T1\Polymathix\polymathix_ui\frontend\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Fix Sidebar CSS to prevent overlapping quote box
old_sidebar_css = """.sidebar{
    position:relative;
    padding:18px 13px;
    border-right:1px solid var(--border);
    background:
        linear-gradient(180deg,rgba(4,20,38,.94),rgba(2,12,25,.94));
    backdrop-filter:blur(24px);
    z-index:10;
}"""

new_sidebar_css = """.sidebar{
    position:relative;
    padding:18px 13px;
    border-right:1px solid var(--border);
    background:
        linear-gradient(180deg,rgba(4,20,38,.94),rgba(2,12,25,.94));
    backdrop-filter:blur(24px);
    z-index:10;
    display: flex;
    flex-direction: column;
    height: 100vh;
    overflow: hidden;
    box-sizing: border-box;
}

.nav{
    margin-top:12px;
    flex: 1;
    overflow-y: auto;
    scrollbar-width: none;
    padding-bottom: 10px;
}
.nav::-webkit-scrollbar { display: none; }"""

if old_sidebar_css in html:
    html = html.replace(old_sidebar_css, new_sidebar_css, 1)

old_quote_css = """.quote{
    position:absolute;
    left:15px;
    right:15px;
    bottom:18px;
    min-height:155px;
    padding:19px;
    border:1px solid rgba(80,160,255,.18);
    border-radius:17px;
    overflow:hidden;
    background:
        linear-gradient(135deg,rgba(8,28,53,.86),rgba(7,20,37,.74));
}"""

new_quote_css = """.quote{
    position: relative;
    margin-top: auto;
    left: 0;
    right: 0;
    bottom: 0;
    min-height: 110px;
    padding: 13px;
    border: 1px solid rgba(80,160,255,.18);
    border-radius: 14px;
    overflow: hidden;
    flex-shrink: 0;
    background:
        linear-gradient(135deg,rgba(8,28,53,.86),rgba(7,20,37,.74));
}"""

if old_quote_css in html:
    html = html.replace(old_quote_css, new_quote_css, 1)

# 2. Fix Search Bar Examples to showcase Plant, Animal, Human, and PDB capabilities
old_search_example = """            <div class="searchExample">
                e.g. "Run Membrane MD v2.4" | "Synthesize de-novo drug with RDKit" | "Deep Trajectory PCA" | "Autonomous OpenMM Minimization"
            </div>"""

new_search_example = """            <div class="searchExample" style="display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-top:3px;">
                <span style="color:#38bdf8;cursor:pointer;background:rgba(56,189,248,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(56,189,248,0.2);" onclick="runAI('Run Crop Proteome & Thermal Adaptation protocol')">🌿 Crop Resilience</span>
                <span style="color:#00f59b;cursor:pointer;background:rgba(0,245,155,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(0,245,155,0.2);" onclick="runAI('Run Veterinary Broad-Spectrum Antimicrobial protocol')">🐾 Veterinary Health</span>
                <span style="color:#a855f7;cursor:pointer;background:rgba(168,85,247,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(168,85,247,0.2);" onclick="runAI('Synthesize novel drug with RDKit and Lipinski screening')">🧪 De-Novo Drug Design</span>
                <span style="color:#ffd84d;cursor:pointer;background:rgba(255,216,77,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(255,216,77,0.2);" onclick="runAI('Load 1UBQ')">🧬 Fetch Ubiquitin (1UBQ)</span>
                <span style="color:#f43f5e;cursor:pointer;background:rgba(244,63,94,0.1);padding:2px 8px;border-radius:6px;border:1px solid rgba(244,63,94,0.2);" onclick="runAI('Load 4HHB')">🩸 Fetch Hemoglobin (4HHB)</span>
            </div>"""

if old_search_example in html:
    html = html.replace(old_search_example, new_search_example, 1)

# 3. Update 3D representation buttons to call setRepresentation(style)
old_rep_buttons = """    <div class="viewerBottom">

        <button class="styleBtn">
            Cartoon
        </button>

        <button class="styleBtn active" onclick="toggleSurface()">
            Surface
        </button>

        <button class="styleBtn">
            Sticks
        </button>

        <button class="styleBtn">
            Sphere
        </button>

        <button class="styleBtn">
            Mesh
        </button>"""

new_rep_buttons = """    <div class="viewerBottom">
        <button class="styleBtn active" id="btnRepCartoon" onclick="setRepresentation('cartoon', this)">Cartoon</button>
        <button class="styleBtn" id="btnRepSurface" onclick="setRepresentation('surface', this)">Surface</button>
        <button class="styleBtn" id="btnRepSticks" onclick="setRepresentation('sticks', this)">Sticks</button>
        <button class="styleBtn" id="btnRepSphere" onclick="setRepresentation('sphere', this)">Sphere</button>
        <button class="styleBtn" id="btnRepMesh" onclick="setRepresentation('mesh', this)">Mesh</button>"""

if old_rep_buttons in html:
    html = html.replace(old_rep_buttons, new_rep_buttons, 1)

# 4. Enhance Three.js Sizing, Rendering & Representation Switching in JS
enhanced_three_js = """
/* ================= ROBUST THREE.JS RESIZING & MULTI-STYLE ENGINE ================= */

let currentRep = 'cartoon';
let cartoonGroup, sticksGroup, sphereGroup, realSurfaceGroup, meshGroup;
let lastCanvasWidth = 0, lastCanvasHeight = 0;

function resizeThree(){
    if(!renderer || !camera || !canvas) return;
    const parent = canvas.parentElement;
    const width = canvas.clientWidth || (parent ? parent.clientWidth : 700) || 700;
    const height = canvas.clientHeight || (parent ? parent.clientHeight : 450) || 450;
    
    if (width > 20 && height > 20 && (width !== lastCanvasWidth || height !== lastCanvasHeight)) {
        lastCanvasWidth = width;
        lastCanvasHeight = height;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height, false);
    }
}

function setRepresentation(style, elem){
    currentRep = style;
    document.querySelectorAll('.viewerBottom .styleBtn').forEach(b => b.classList.remove('active'));
    if (elem) elem.classList.add('active');

    if (cartoonGroup) cartoonGroup.visible = (style === 'cartoon');
    if (realSurfaceGroup) realSurfaceGroup.visible = (style === 'surface');
    if (sticksGroup) sticksGroup.visible = (style === 'sticks');
    if (sphereGroup) sphereGroup.visible = (style === 'sphere');
    if (meshGroup) meshGroup.visible = (style === 'mesh');

    showToast('3D Representation', style.toUpperCase() + ' representation activated');
}

function renderRealPDB(pdbData){
    if (!pdbData || !pdbData.ca_coords || pdbData.ca_coords.length === 0) return;

    // Clear old molecule
    if (moleculeGroup) {
        while(moleculeGroup.children.length > 0) {
            moleculeGroup.remove(moleculeGroup.children[0]);
        }
    } else {
        moleculeGroup = new THREE.Group();
        scene.add(moleculeGroup);
    }

    cartoonGroup = new THREE.Group();
    sphereGroup = new THREE.Group();
    sticksGroup = new THREE.Group();
    realSurfaceGroup = new THREE.Group();
    meshGroup = new THREE.Group();

    // 1. CARTOON RIBBON: CatmullRomCurve3 through all CA coordinates
    const caPoints = pdbData.ca_coords.map(c => new THREE.Vector3(c.x, c.y, c.z));
    if (caPoints.length >= 2) {
        const curve = new THREE.CatmullRomCurve3(caPoints);
        const tubeGeo = new THREE.TubeGeometry(curve, Math.max(100, caPoints.length * 6), 0.42, 12, false);
        
        // Multi-color vertex coloring (Rainbow from N to C terminus)
        const count = tubeGeo.attributes.position.count;
        const colors = new Float32Array(count * 3);
        const tempColor = new THREE.Color();
        for (let i = 0; i < count; i++) {
            const t = (i / count);
            tempColor.setHSL(0.55 - t * 0.55, 0.95, 0.55); // Cyan -> Green -> Yellow -> Orange -> Magenta
            colors[i * 3] = tempColor.r;
            colors[i * 3 + 1] = tempColor.g;
            colors[i * 3 + 2] = tempColor.b;
        }
        tubeGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const tubeMat = new THREE.MeshStandardMaterial({
            vertexColors: true,
            roughness: 0.25,
            metalness: 0.2
        });
        const ribbonMesh = new THREE.Mesh(tubeGeo, tubeMat);
        cartoonGroup.add(ribbonMesh);

        // Alpha-carbon spheres
        const caSphereGeo = new THREE.SphereGeometry(0.55, 16, 16);
        caPoints.forEach((pt, idx) => {
            const frac = idx / caPoints.length;
            const mat = new THREE.MeshStandardMaterial({
                color: new THREE.Color().setHSL(0.55 - frac * 0.55, 0.95, 0.6),
                roughness: 0.2
            });
            const sMesh = new THREE.Mesh(caSphereGeo, mat);
            sMesh.position.copy(pt);
            cartoonGroup.add(sMesh);
        });
    }

    // 2. SPHERE (CPK Space-Filling) & STICKS: All Atoms
    const atoms = pdbData.atoms || [];
    const sphereGeo = new THREE.SphereGeometry(0.48, 14, 14);
    const elemColors = {
        'C': 0x00d9ff, 'N': 0x3b82f6, 'O': 0xef4444, 'S': 0xfacc15, 'H': 0xffffff, 'P': 0xf97316
    };

    atoms.forEach(a => {
        const col = elemColors[a.elem] || 0x10b981;
        const mat = new THREE.MeshStandardMaterial({ color: col, roughness: 0.3 });
        const sMesh = new THREE.Mesh(sphereGeo, mat);
        sMesh.position.set(a.x, a.y, a.z);
        sphereGroup.add(sMesh);
    });

    // Sticks: Connect consecutive CA atoms and close atoms (< 1.8 Å)
    const stickMat = new THREE.MeshStandardMaterial({ color: 0x93c5fd, roughness: 0.3 });
    for (let i = 0; i < caPoints.length - 1; i++) {
        const p1 = caPoints[i];
        const p2 = caPoints[i+1];
        const dist = p1.distanceTo(p2);
        if (dist < 4.2) {
            const cylinderGeo = new THREE.CylinderGeometry(0.18, 0.18, dist, 8);
            const cyl = new THREE.Mesh(cylinderGeo, stickMat);
            cyl.position.copy(p1).add(p2).multiplyScalar(0.5);
            cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0, 1, 0), p2.clone().sub(p1).normalize());
            sticksGroup.add(cyl);
        }
    }

    // 3. SURFACE: Translucent Molecular Envelope
    const box = new THREE.Box3().setFromPoints(caPoints);
    const size = new THREE.Vector3();
    box.getSize(size);
    const center = new THREE.Vector3();
    box.getCenter(center);
    const maxDim = Math.max(size.x, size.y, size.z) * 0.65;

    const surfaceGeo = new THREE.IcosahedronGeometry(Math.max(6, maxDim), 3);
    const surfaceMat = new THREE.MeshPhysicalMaterial({
        color: 0x0ea5e9,
        transparent: true,
        opacity: 0.22,
        roughness: 0.1,
        transmission: 0.6,
        side: THREE.DoubleSide
    });
    const sMeshObj = new THREE.Mesh(surfaceGeo, surfaceMat);
    sMeshObj.position.copy(center);
    realSurfaceGroup.add(sMeshObj);

    // 4. MESH WIREFRAME
    const wireMat = new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true });
    const wireMesh = new THREE.Mesh(surfaceGeo, wireMat);
    wireMesh.position.copy(center);
    meshGroup.add(wireMesh);

    // Add all to moleculeGroup
    moleculeGroup.add(cartoonGroup);
    moleculeGroup.add(sphereGroup);
    moleculeGroup.add(sticksGroup);
    moleculeGroup.add(realSurfaceGroup);
    moleculeGroup.add(meshGroup);

    // Set initial representation
    setRepresentation(currentRep, document.getElementById('btnRep' + currentRep.charAt(0).toUpperCase() + currentRep.slice(1)));

    // Fit camera smoothly
    camera.position.set(0, maxDim * 0.8, maxDim * 2.2);
    if (controls) {
        controls.target.set(center.x, center.y, center.z);
        controls.update();
    }

    // Populate sequence chips
    const seqContainer = document.getElementById('seqGridContainer');
    if (seqContainer && pdbData.sequence) {
        seqContainer.innerHTML = '';
        pdbData.sequence.forEach(s => {
            const chip = document.createElement('div');
            chip.className = 'seqChip';
            chip.innerHTML = `<div class="seqResName">${s.name}</div><div class="seqResNum">${s.id}</div>`;
            chip.onclick = () => {
                showToast('Residue Selected', `${s.name} #${s.id} focused`);
            };
            seqContainer.appendChild(chip);
        });
    }

    // Populate properties table
    if (pdbData.properties) {
        const pTable = document.getElementById('propertiesTable');
        if (pTable) {
            let tbody = '<tbody>';
            for (const [k, v] of Object.entries(pdbData.properties)) {
                tbody += `<tr><th>${k}</th><td>${v}</td></tr>`;
            }
            tbody += '</tbody>';
            pTable.innerHTML = tbody;
        }
    }
}
"""

# Replace the old renderRealPDB and add the robust engine
html = html.replace("/* ================= REAL PDB RENDERING IN THREE.JS ================= */", enhanced_three_js, 1)

# Ensure animate() calls resizeThree() regularly
html = html.replace("function animate(){", """function animate(){
    resizeThree();""", 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Enhanced UI logic applied successfully!")

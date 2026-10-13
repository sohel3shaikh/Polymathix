import os

html_path = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html")

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# Replace the runAI function and bridge JS with comprehensive functions
new_js_logic = """
/* ================= ADVANCED POLYMATHIX INTERACTIVITY ================= */

function runAI(customQuery){
    const inputElem = document.getElementById('aiInput');
    const query = customQuery || (inputElem ? inputElem.value : '') || 'Run scientific protocol';
    
    showToast('AI Research Agent', 'Planning & orchestrating protocol...');
    addLog('AI', 'Natural language instruction received: "' + query + '"');

    Streamlit.setComponentValue({
        action: 'runAI',
        query: query,
        timestamp: Date.now()
    });
    
    if (inputElem) inputElem.value = '';
}

function triggerQuickAction(actionType){
    showToast('Polymathix OS', 'Executing ' + actionType.replace('_', ' ') + '...');
    Streamlit.setComponentValue({
        action: 'quick_action',
        type: actionType,
        timestamp: Date.now()
    });
}

function triggerAgentControl(cmd){
    showToast('Agent Control', 'Command: ' + cmd.toUpperCase());
    Streamlit.setComponentValue({
        action: 'agent_control',
        cmd: cmd,
        timestamp: Date.now()
    });
}

function switchWorkspaceTab(tabName, elem){
    document.querySelectorAll('.viewer .tab').forEach(t => t.classList.remove('active'));
    if (elem) elem.classList.add('active');

    // Hide all panels
    const canvasWrap = document.getElementById('threeCanvasWrap');
    if (canvasWrap) canvasWrap.style.display = (tabName === 'viewer') ? 'block' : 'none';

    document.querySelectorAll('.workspacePanel').forEach(p => p.classList.remove('active'));
    
    if (tabName !== 'viewer') {
        const target = document.getElementById(tabName + 'Panel');
        if (target) target.classList.add('active');
    }

    showToast('Workspace', tabName.toUpperCase() + ' panel active');
}

let trajInterval = null;
function toggleTrajectoryPlay(){
    const slider = document.getElementById('trajSlider');
    const frameLabel = document.getElementById('trajFrame');
    if (trajInterval) {
        clearInterval(trajInterval);
        trajInterval = null;
        showToast('Trajectory', 'Playback paused');
    } else {
        showToast('Trajectory', 'Playback running');
        trajInterval = setInterval(() => {
            let val = parseInt(slider.value) + 15;
            if (val > 1500) val = 0;
            slider.value = val;
            frameLabel.innerText = val;
            if (moleculeGroup) {
                moleculeGroup.rotation.y += 0.03;
            }
        }, 80);
    }
}

/* ================= REAL PDB RENDERING IN THREE.JS ================= */

let realProteinGroup = null;

function renderRealPDB(pdbData){
    if (!pdbData || !pdbData.ca_coords || pdbData.ca_coords.length === 0) return;

    if (realProteinGroup) {
        scene.remove(realProteinGroup);
    }
    realProteinGroup = new THREE.Group();

    // 1. CatmullRomCurve3 Backbone Tube through all CA coordinates
    const points = pdbData.ca_coords.map(c => new THREE.Vector3(c.x, c.y, c.z));
    const curve = new THREE.CatmullRomCurve3(points);
    const tubeGeo = new THREE.TubeGeometry(curve, 200, 0.35, 10, false);
    
    const tubeMat = new THREE.MeshStandardMaterial({
        color: 0x00d9ff,
        metalness: 0.25,
        roughness: 0.25,
        transparent: true,
        opacity: 0.95
    });
    const tubeMesh = new THREE.Mesh(tubeGeo, tubeMat);
    realProteinGroup.add(tubeMesh);

    // 2. Add alpha-carbon spheres with residue color variation
    const sphereGeo = new THREE.SphereGeometry(0.42, 16, 16);
    points.forEach((pt, idx) => {
        const hue = (idx / points.length) * 0.7 + 0.15;
        const color = new THREE.Color().setHSL(hue, 0.9, 0.55);
        const mat = new THREE.MeshStandardMaterial({ color: color, roughness: 0.3 });
        const sphere = new THREE.Mesh(sphereGeo, mat);
        sphere.position.copy(pt);
        realProteinGroup.add(sphere);
    });

    // Replace default surface group with real structure
    if (surfaceGroup) {
        surfaceGroup.visible = false;
    }
    scene.add(realProteinGroup);
    
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
}

/* ================= PYTHON STATE SYNCHRONIZATION ================= */

function updateStateFromPython(state){
    if (!state) return;

    // 1. Session & Protocol
    if (state.session_name) {
        const sElem = document.getElementById('sessionNameDisplay');
        if (sElem) sElem.innerText = state.session_name;
    }
    if (state.protocol_name) {
        const pElem = document.getElementById('protocolNameDisplay');
        if (pElem) pElem.innerText = state.protocol_name;
    }
    if (state.status) {
        const stElem = document.getElementById('sessionStatusDisplay');
        if (stElem) {
            const isAct = state.status === 'Active';
            stElem.innerHTML = `<span class="statusDot" style="background:${isAct ? '#00f59b' : '#ffae3d'}"></span>${state.status}`;
        }
    }

    // 2. Workflow Steps
    if (state.workflow_steps && Array.isArray(state.workflow_steps)) {
        const wfContainer = document.querySelector('.workflow');
        if (wfContainer) {
            let html = '<div class="workflowTitle">Workflow Steps</div>';
            state.workflow_steps.forEach((step, idx) => {
                const num = idx + 1;
                let cls = 'step';
                let icon = '';
                if (step.status === 'done') {
                    cls = 'step done';
                    icon = '<span style="margin-left:auto;color:#00f59b">✓</span>';
                } else if (step.status === 'running') {
                    cls = 'step running';
                    icon = '<span style="margin-left:auto;color:#529fff">●</span>';
                }
                html += `<div class="${cls}"><div class="stepNum">${num}</div><span>${step.name}</span>${icon}</div>`;
            });
            wfContainer.innerHTML = html;
        }
    }

    // 3. Progress & Time Remaining
    if (typeof state.progress_percent === 'number') {
        const pFill = document.getElementById('progressFill');
        const pVal = document.getElementById('progressValue');
        if (pFill) pFill.style.width = state.progress_percent + '%';
        if (pVal) pVal.innerText = state.progress_percent + '%';
    }
    if (state.time_remaining) {
        const tRem = document.getElementById('timeRemainingDisplay');
        if (tRem) tRem.innerText = 'Estimated time remaining: ' + state.time_remaining;
    }

    // 4. Logs
    if (state.logs && Array.isArray(state.logs)) {
        const logBody = document.getElementById('logBody');
        if (logBody) {
            logBody.innerHTML = '';
            state.logs.forEach(l => {
                let cls = 'logInfo';
                if (l.type === 'SUCCESS') cls = 'logSuccess';
                if (l.type === 'WARN') cls = 'logWarn';
                if (l.type === 'ERROR') cls = 'logError';
                if (l.type === 'AI') cls = 'logSuccess';
                
                const div = document.createElement('div');
                div.className = 'logLine';
                div.innerHTML = `[${l.time}] <span class="${cls}">${l.type}</span> ${l.msg}`;
                logBody.appendChild(div);
            });
            logBody.scrollTop = logBody.scrollHeight;
        }
    }

    // 5. Results Grid
    if (state.results && Array.isArray(state.results)) {
        const grid = document.getElementById('resultGrid');
        if (grid) {
            grid.innerHTML = '';
            state.results.forEach(r => {
                const card = document.createElement('div');
                card.className = 'resultCard';
                card.onclick = () => {
                    showToast('Result Item', 'Opening ' + r.name);
                };
                card.innerHTML = `
                    <div class="resultPreview">${r.icon || '🧬'}</div>
                    <div class="resultName">${r.name}</div>
                    <div class="resultMeta">${r.meta || 'Recent'}</div>
                `;
                grid.appendChild(card);
            });
        }
    }

    // 6. Real PDB coordinates
    if (state.pdb_data) {
        renderRealPDB(state.pdb_data);
    }
}
"""

# Replace the old bridge logic with the complete bidirectional engine
old_bridge_pattern = """/* ================= STREAMLIT BRIDGE ================= */
const Streamlit = {
    setComponentReady: function() {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:componentReady', apiVersion: 1}, '*');
    },
    setFrameHeight: function(height) {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: height}, '*');
    },
    setComponentValue: function(value) {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: value}, '*');
    }
};

window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:render') {
        const args = event.data.args;
        if (args && args.command === 'update_logs') {
            addLog(args.log_type, args.log_message);
        } else if (args && args.command === 'update_progress') {
            document.getElementById('progressFill').style.width = args.percent + '%';
            document.getElementById('progressValue').innerText = args.percent + '%';
        }
    }
});

// Signal ready and set height on load
window.addEventListener('load', function() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight);
});

// Update height on resize
window.addEventListener('resize', function() {
    Streamlit.setFrameHeight(window.innerHeight);
});"""

new_bridge_full = new_js_logic + """
/* ================= STREAMLIT BRIDGE ================= */
const Streamlit = {
    setComponentReady: function() {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:componentReady', apiVersion: 1}, '*');
    },
    setFrameHeight: function(height) {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: height}, '*');
    },
    setComponentValue: function(value) {
        window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: value}, '*');
    }
};

window.addEventListener('message', function(event) {
    if (event.data.type === 'streamlit:render') {
        const args = event.data.args;
        const state = (args && args.initial_data) ? args.initial_data : args;
        if (state) {
            updateStateFromPython(state);
        }
    }
});

window.addEventListener('load', function() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight);
});

window.addEventListener('resize', function() {
    Streamlit.setFrameHeight(window.innerHeight);
});
"""

if old_bridge_pattern in html:
    html = html.replace(old_bridge_pattern, new_bridge_full, 1)
else:
    # Append before </script>
    html = html.replace("</script>", new_bridge_full + "\n</script>", 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("UI JavaScript engine updated successfully!")

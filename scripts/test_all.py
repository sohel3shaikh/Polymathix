import os
import sys
import time

# Ensure root directory in sys.path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

print("=" * 60)
print("POLYMATHIX OS — COMPREHENSIVE END-TO-END VERIFICATION")
print("=" * 60)

passed = 0
failed = 0

def test_step(name, func):
    global passed, failed
    print(f"\n[TEST] {name}...")
    try:
        func()
        print(f"  --> PASSED")
        passed += 1
    except Exception as e:
        print(f"  --> FAILED: {e}")
        failed += 1

if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

def t1_orchestrator_init():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    state = orc.get_state()
    assert state["session_name"] == "MembraneONE", "Incorrect default session"
    assert "Glucose" in state["protocol_name"] or "Membrane" in state["protocol_name"], "Incorrect default protocol"
    assert len(state["workflow_steps"]) in [6, 8], f"Unexpected workflow steps: {len(state['workflow_steps'])}"
    assert len(state["connectors"]) == 10, "Expected 10 tool connectors"
    assert "pdb_data" in state, "Missing pdb_data in state"
    assert len(state["pdb_data"]["ca_coords"]) == 46, f"Expected 46 CA coords, got {len(state['pdb_data']['ca_coords'])}"
    assert len(state["pdb_data"]["atoms"]) == 327, f"Expected 327 atoms, got {len(state['pdb_data']['atoms'])}"

def t2_rdkit_drug_design():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.run_ai_task("Synthesize novel anti-inflammatory molecule with RDKit")
    state = orc.get_state()
    assert state["active_protocol_key"] == "drug_design", "Expected drug_design protocol"
    assert any("mol_" in r["name"] for r in state["results"]), "Missing synthesized molecule in results"
    assert os.path.exists(os.path.join(ROOT_DIR, "assets", "generated_mol.png")), "generated_mol.png not found"

def t3_deep_pca():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.run_ai_task("Run Deep Trajectory PCA analysis")
    state = orc.get_state()
    assert state["active_protocol_key"] == "deep_pca", "Expected deep_pca protocol"
    assert any("deep_pca" in r["name"] for r in state["results"]), "Missing deep_pca in results"
    assert os.path.exists(os.path.join(ROOT_DIR, "assets", "deep_pca_comparison.png")), "deep_pca_comparison.png not found"

def t4_minimization():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.run_ai_task("Autonomous energy minimization and 3D OBJ export")
    state = orc.get_state()
    assert state["active_protocol_key"] == "minimization", "Expected minimization protocol"
    assert os.path.exists(os.path.join(ROOT_DIR, "assets", "energy_plot.png")), "energy_plot.png not found"
    assert os.path.exists(os.path.join(ROOT_DIR, "assets", "polymathix_3d_render.obj")), "polymathix_3d_render.obj not found"

def t5_quick_actions():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.handle_quick_action("new_session")
    state = orc.get_state()
    valid_prefixes = ["BioDiscovery-", "PlantResilience-", "EnzymeEngineering-", "VeterinaryTherapeutics-", "GlobalHealth-"]
    assert any(state["session_name"].startswith(p) for p in valid_prefixes), f"Unexpected new session name: {state['session_name']}"
    assert state["progress_percent"] == 10, "Progress should reset to 10 on new session"
    
    orc.handle_quick_action("generate_plot")
    assert any("energy convergence" in l["msg"].lower() for l in orc.logs), "Missing plot generation log"

def t6_agent_controls():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.handle_agent_control("pause")
    assert orc.status == "Paused", "Expected status Paused"
    orc.handle_agent_control("pause")
    assert orc.status == "Active", "Expected status Active"
    orc.handle_agent_control("stop")
    assert orc.status == "Stopped", "Expected status Stopped"

def t7_tool_connectors():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    initial_status = next(c["status"] for c in orc.connectors if c["name"] == "GROMACS")
    orc.toggle_connector("GROMACS")
    new_status = next(c["status"] for c in orc.connectors if c["name"] == "GROMACS")
    assert initial_status != new_status, "Connector status did not toggle"

def t8_frontend_assets():
    frontend_assets = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "assets")
    assert os.path.exists(frontend_assets), "Frontend assets directory missing"
    assert os.path.exists(os.path.join(frontend_assets, "energy_plot.png")), "Frontend energy_plot.png missing"
    assert os.path.exists(os.path.join(frontend_assets, "deep_pca_comparison.png")), "Frontend deep_pca_comparison.png missing"

def t9_frontend_index_integrity():
    index_path = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html")
    assert os.path.exists(index_path), "index.html missing"
    with open(index_path, "r", encoding="utf-8") as f:
        html = f.read()

    # Core UI DOM Elements (Full pack of views & layer toggles)
    required_dom = [
        "aiInput", "sessionNameDisplay", "protocolNameDisplay", "sessionStatusDisplay",
        "progressFill", "progressValue", "timeRemainingDisplay", "logBody", "resultGrid",
        "threeCanvasWrap", "threeCanvas", "sequencePanel", "trajectoryPanel", "surfacesPanel",
        "propertiesPanel", "analysisPanel", "bindingPanel", "bindingResiduesList",
        "sessionModalOverlay", "exportOverlay", "resultsModalOverlay", "settingsModalOverlay",
        "simHUD", "simControlsBar", "btnSimPlay", "simModeSelect", "simTempSlider",
        "chkDisulfides", "chkHydration", "chkMembrane", "chkLigand", "chkCavity",
        "viewModeSelect", "btnRepRibbon", "btnRepCartoon", "btnRepSurface", "btnRepElectro",
        "btnRepHydrophobic", "btnRepGlass", "btnRepMesh", "btnRepSticks", "btnRepLicorice",
        "btnRepSphere", "btnRepBfactor", "btnRepBackbone"
    ]
    for dom_id in required_dom:
        assert f'id="{dom_id}"' in html or f"id='{dom_id}'" in html, f"Missing DOM id='{dom_id}' in index.html"

    # Core JavaScript Functions (all 53 essential functions)
    required_funcs = [
        "initThree", "resizeThree", "animate", "renderRealPDB", "setRepresentation",
        "resetCamera", "focusMolecule", "toggleSurface", "randomizeMolecule", "takeSnapshot",
        "toggleViewerFullscreen", "toggleQuality", "createGlucoseLigand", "createInteractions",
        "focusResidue", "focusBindingPocket", "closeBindingPanel",
        "toggleSimPlay", "setSimMode", "setSimTemp", "toggleDisulfides", "toggleHydration", "toggleMembrane",
        "toggleLigand", "toggleCavity",
        "switchWorkspaceTab", "toggleTrajectoryPlay", "scrubTrajectory",
        "switchLogTab", "clearLogs", "filterLogs", "navSelect",
        "openSessionModal", "closeSessionModal", "openExport", "closeExport",
        "openResultsModal", "closeResultsModal", "openSettingsModal", "closeSettingsModal",
        "openConnectorsModal", "setExportFormat", "performExport",
        "toggleAudio", "toggleTheme", "setupSimpleControls",
        "runAI", "triggerQuickAction", "triggerAgentControl", "toggleConnector",
        "updateStateFromPython", "showToast", "updateClock"
    ]
    import re
    actual_funcs = set(re.findall(r'function\s+([a-zA-Z0-9_]+)\s*\(', html))
    for func in required_funcs:
        assert func in actual_funcs, f"Missing function declaration: function {func}() in index.html"

def t10_streamlit_app_compilation():
    app_path = os.path.join(ROOT_DIR, "app.py")
    import py_compile
    py_compile.compile(app_path, doraise=True)

def t11_glucose_binding_pocket():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    orc.run_ai_task("Show glucose binding site and identify residues within 4 Angstroms")
    state = orc.get_state()
    assert state["active_protocol_key"] == "binding_site", "Expected binding_site protocol"
    assert "pdb_data" in state, "Missing pdb_data"
    pdb = state["pdb_data"]
    assert "binding_residues" in pdb, "Missing binding_residues"
    assert len(pdb["binding_residues"]) == 8, f"Expected 8 interacting residues, got {len(pdb['binding_residues'])}"
    assert "glucose_coords" in pdb, "Missing glucose_coords"
    assert len(pdb["glucose_coords"]) == 12, f"Expected 12 glucose ring/substituent atoms, got {len(pdb['glucose_coords'])}"
    assert os.path.exists(os.path.join(ROOT_DIR, "assets", "glucose_2d.png")), "glucose_2d.png missing"
    assert any("glucose" in r["name"] for r in state["results"]), "Missing glucose in results list"

def t12_universal_small_molecules():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    
    # Test Aspirin
    orc.run_ai_task("Show aspirin in 3D")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert pdb.get("is_small_molecule") == True, "Aspirin should be marked as small molecule"
    assert pdb.get("atom_count") == 21, f"Expected 21 atoms for Aspirin, got {pdb.get('atom_count')}"
    assert len(pdb.get("bonds", [])) >= 20, f"Expected >= 20 bonds for Aspirin, got {len(pdb.get('bonds', []))}"
    assert state["progress_percent"] == 100, f"Expected 100% progress, got {state['progress_percent']}"
    assert state["time_remaining"] == "Completed (Ready)", f"Expected Completed (Ready), got {state['time_remaining']}"

    # Test Caffeine
    orc.run_ai_task("caffeine")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert pdb.get("is_small_molecule") == True, "Caffeine should be marked as small molecule"
    assert pdb.get("atom_count") == 24, f"Expected 24 atoms for Caffeine, got {pdb.get('atom_count')}"
    assert state["progress_percent"] == 100

    # Test Ibuprofen
    orc.run_ai_task("ibuprofen")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert pdb.get("is_small_molecule") == True, "Ibuprofen should be marked as small molecule"
    assert pdb.get("atom_count") == 33, f"Expected 33 atoms for Ibuprofen, got {pdb.get('atom_count')}"
    assert state["progress_percent"] == 100

def t13_100_percent_progress_and_completion():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    queries = [
        "Run Crop Proteome & Thermal Adaptation protocol",
        "Run Veterinary Broad-Spectrum Antimicrobial protocol",
        "Biocatalytic Triad Optimization v3.0",
        "Synthesize novel drug with RDKit and Lipinski screening",
        "Run Deep Trajectory PCA analysis"
    ]
    for q in queries:
        orc.run_ai_task(q)
        state = orc.get_state()
        assert state["progress_percent"] == 100, f"Query '{q}' did not reach 100% progress (got {state['progress_percent']}%)"
        assert state["time_remaining"] == "Completed (Ready)", f"Query '{q}' time_remaining is '{state['time_remaining']}'"
        assert all(step["status"] == "done" for step in state["workflow_steps"]), f"Not all steps are done for '{q}'"

def t14_materials_science_crystals():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    
    # 1. Perovskite (SrTiO3)
    orc.run_ai_task("perovskite")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert "Perovskite" in pdb["pdb_name"], "Expected Perovskite name"
    assert pdb.get("is_material") == True, "Expected is_material flag True"
    assert pdb.get("atom_count") == 15, f"Expected 15 atoms for SrTiO3, got {pdb.get('atom_count')}"
    assert len(pdb.get("bonds", [])) >= 20, f"Expected coordination bonds, got {len(pdb.get('bonds', []))}"
    assert state["active_protocol_key"] == "material_discovery", "Expected material_discovery protocol"
    assert state["progress_percent"] == 100

    # 2. 2D Graphene
    orc.run_ai_task("graphene")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert "Graphene" in pdb["pdb_name"], "Expected Graphene name"
    assert pdb.get("atom_count") == 32, f"Expected 32 carbon atoms for graphene, got {pdb.get('atom_count')}"
    assert len(pdb.get("bonds", [])) >= 30, f"Expected sp2 bonds, got {len(pdb.get('bonds', []))}"

    # 3. SWCNT Carbon Nanotube
    orc.run_ai_task("swcnt")
    state = orc.get_state()
    pdb = state["pdb_data"]
    assert "Carbon Nanotube" in pdb["pdb_name"], "Expected SWCNT name"
    assert pdb.get("atom_count") == 60, f"Expected 60 atoms for (5,5) SWCNT, got {pdb.get('atom_count')}"

def t15_library_catalog_and_copilot():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    state = orc.get_state()
    
    # Verify Library catalog
    assert "library_examples" in state, "Missing library_examples in state"
    examples = state["library_examples"]
    assert len(examples) >= 20, f"Expected at least 20 examples, got {len(examples)}"
    categories = set(e["category"] for e in examples)
    assert "Human Therapeutics" in categories, "Missing Human Therapeutics"
    assert "Materials Science & Crystals" in categories, "Missing Materials Science"
    assert "Agricultural & Crop Resilience" in categories, "Missing Agricultural Resilience"

    # Verify AI Co-Pilot chat response and real-time structure mutation
    reply = orc.handle_chat_message("Fluorinate aspirin at position 4 to enhance metabolic stability")
    assert len(reply) > 50, "Expected detailed scientific co-pilot reply"
    assert len(orc.chat_history) >= 2, "Chat history should contain user and AI messages"
    assert "5-Fluoro-Aspirin" in orc.pdb_data["pdb_name"], "Structure was not updated to 5-Fluoro-Aspirin in real time"

def t16_cross_domain_correctness_invariants():
    from polymathix.orchestrator import PolymathixOrchestrator
    from polymathix.core.invariants import CrossDomainCorrectnessVerifier
    orc = PolymathixOrchestrator()
    verifier = CrossDomainCorrectnessVerifier()

    # 1. Biomolecular domain verification (Crambin fold + Glucose pocket)
    st = orc.get_state()
    assert "correctness_dossier" in st, "Missing correctness_dossier in orchestrator state"
    cd = st["correctness_dossier"]
    assert cd["status"] == "VERIFIED", f"Expected VERIFIED, got {cd['status']}"
    assert cd["confidence_score"] >= 0.85, f"Expected high confidence, got {cd['confidence_score']}"
    assert cd["checks_passed"] >= 3, "Expected at least 3 invariant checks passed"

    # 2. Solid-State Materials domain verification (SrTiO3 Perovskite)
    orc.run_ai_task("perovskite")
    st = orc.get_state()
    cd = st["correctness_dossier"]
    assert cd["domain"] == "Solid-State Chemistry & Materials Crystallography"
    assert cd["status"] == "VERIFIED"
    assert cd["confidence_score"] == 1.0
    invariant_names = [c["invariant"] for c in cd["checks"]]
    assert "Unit Cell Electroneutrality Invariant" in invariant_names
    assert "Crystallographic Space Group Invariance" in invariant_names

    # 3. Cheminformatics & Small Molecule domain verification (Aspirin)
    orc.run_ai_task("aspirin")
    st = orc.get_state()
    cd = st["correctness_dossier"]
    assert cd["domain"] == "Cheminformatics & Molecular Mechanics"
    assert cd["status"] == "VERIFIED"
    assert cd["confidence_score"] == 1.0

def t17_provenance_and_deterministic_replay():
    from polymathix.orchestrator import PolymathixOrchestrator
    from polymathix.core.provenance import ScientificRunManifest, DeterministicReplayEngine
    orc = PolymathixOrchestrator()

    # 1. Verify cryptographic run manifest compilation
    st = orc.get_state()
    assert "run_provenance" in st, "Missing run_provenance in orchestrator state"
    prov = st["run_provenance"]
    assert len(prov["run_id"]) > 10, "Invalid UUID in run manifest"
    assert "canonical_intermediate_representation" in prov
    assert "coordinate_sha256" in prov["canonical_intermediate_representation"]
    assert prov["kernel_environment"]["prng_seed"] == 42
    assert prov["reproducibility_guarantee"] == "BIT_EXACT_REPRODUCIBLE"

    # 2. Test Deterministic Replay Engine
    replay_report = DeterministicReplayEngine.verify_replay(prov, st["pdb_data"])
    assert replay_report["replay_verified"] is True, f"Deterministic replay verification failed: {replay_report}"
    assert replay_report["match_level"] == "BIT_EXACT"

    # 3. Test Replay on Material Science Lattice
    orc.run_ai_task("graphene")
    st_mat = orc.get_state()
    prov_mat = st_mat["run_provenance"]
    mat_replay = DeterministicReplayEngine.verify_replay(prov_mat, st_mat["pdb_data"])
    assert mat_replay["replay_verified"] is True
    assert mat_replay["match_level"] == "BIT_EXACT"

test_step("1. Polymathix Orchestrator Initialization & PDB Parsing", t1_orchestrator_init)
test_step("2. De-Novo Drug Synthesis Engine (RDKit Backend)", t2_rdkit_drug_design)
test_step("3. Deep Trajectory PCA & Manifold Learning Engine", t3_deep_pca)
test_step("4. Self-Healing Energy Minimization & OBJ Exporter", t4_minimization)
test_step("5. Quick Action Handlers & Session Lifecycle", t5_quick_actions)
test_step("6. Agent Controls (Pause, Stop, Run)", t6_agent_controls)
test_step("7. Tool Connector Router & Toggle Logic", t7_tool_connectors)
test_step("8. Frontend Scientific Assets Synchronization", t8_frontend_assets)
test_step("9. Frontend Index HTML & Three.js 3D Engine Integrity", t9_frontend_index_integrity)
test_step("10. Streamlit Master Application Compilation", t10_streamlit_app_compilation)
test_step("11. D-Glucose Active Pocket Docking & 3D Interacting Network", t11_glucose_binding_pocket)
test_step("12. Universal Small Molecule 3D Engine (Aspirin, Caffeine, Ibuprofen)", t12_universal_small_molecules)
test_step("13. 100% Progress Convergence & Protocol Finalization", t13_100_percent_progress_and_completion)
test_step("14. Solid-State Materials Science & Crystallography Engine (SrTiO3, Graphene, SWCNT)", t14_materials_science_crystals)
test_step("15. 3D Discovery Library Catalog (23+ Targets) & Real-Time AI Co-Pilot", t15_library_catalog_and_copilot)
test_step("16. Cross-Domain Physical Invariants & Correctness Verifier", t16_cross_domain_correctness_invariants)
test_step("17. Cryptographic Run Provenance & Deterministic Replay Engine", t17_provenance_and_deterministic_replay)

print("\n" + "=" * 60)
print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED")
print("=" * 60)

if failed > 0:
    sys.exit(1)

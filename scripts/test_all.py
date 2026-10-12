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

def t1_orchestrator_init():
    from polymathix.orchestrator import PolymathixOrchestrator
    orc = PolymathixOrchestrator()
    state = orc.get_state()
    assert state["session_name"] == "MembraneONE", "Incorrect default session"
    assert state["protocol_name"] == "Membrane MD v2.4", "Incorrect default protocol"
    assert len(state["workflow_steps"]) == 8, "Expected 8 workflow steps"
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
    required = [
        "aiInput", "sessionNameDisplay", "protocolNameDisplay", "sessionStatusDisplay",
        "progressFill", "progressValue", "timeRemainingDisplay", "logBody", "resultGrid",
        "threeCanvasWrap", "sequencePanel", "trajectoryPanel", "surfacesPanel",
        "propertiesPanel", "analysisPanel", "renderRealPDB", "updateStateFromPython"
    ]
    for req in required:
        assert req in html, f"Missing {req} in index.html"

def t10_streamlit_app_compilation():
    app_path = os.path.join(ROOT_DIR, "app.py")
    import py_compile
    py_compile.compile(app_path, doraise=True)

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

print("\n" + "=" * 60)
print(f"VERIFICATION SUMMARY: {passed} PASSED, {failed} FAILED")
print("=" * 60)

if failed > 0:
    sys.exit(1)

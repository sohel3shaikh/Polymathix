import os
import sys

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

html_code = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>POLYMATHIX — AI for Scientific Discovery</title>

<!-- Local Fast Bundle + CDN Fallback -->
<script src="js/three.min.js"></script>
<script>
if(typeof THREE === 'undefined'){
    document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/build/three.min.js"><\\/script>');
}
</script>
<script src="js/OrbitControls.js"></script>
<script>
if(typeof THREE !== 'undefined' && typeof THREE.OrbitControls === 'undefined'){
    document.write('<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"><\\/script>');
}
</script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/OBJExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/STLExporter.js"></script>
<script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/exporters/GLTFExporter.js"></script>

<style>
:root{
    --bg:#020914;
    --bg2:#061426;
    --panel:rgba(7,25,46,.78);
    --panel2:rgba(10,31,57,.88);
    --border:rgba(90,178,255,.20);
    --blue:#168cff;
    --cyan:#00eaff;
    --violet:#7657ff;
    --green:#00f59b;
    --yellow:#ffd84d;
    --red:#ff4d67;
    --text:#f2f7ff;
    --muted:#7e94ad;
    --shadow:0 0 35px rgba(0,120,255,.14);
}

*{ box-sizing:border-box; margin:0; padding:0; }

html,body{
    width:100%; height:100%;
    overflow:hidden;
    font-family:Inter,Segoe UI,-apple-system,BlinkMacSystemFont,Roboto,sans-serif;
    color:var(--text);
    background:
        radial-gradient(circle at 75% 5%,rgba(0,110,255,.15),transparent 35%),
        radial-gradient(circle at 20% 80%,rgba(115,55,255,.10),transparent 35%),
        linear-gradient(135deg,#020711,#04101e 55%,#020814);
}

button, input{ font:inherit; color:var(--text); outline:none; }

.app{
    width:100vw; height:100vh;
    display:grid;
    grid-template-columns:240px 1fr;
    overflow:hidden;
}

/* ================= SIDEBAR ================= */
.sidebar{
    position:relative;
    padding:16px 12px;
    border-right:1px solid var(--border);
    background:linear-gradient(180deg,rgba(4,20,38,.96),rgba(2,12,25,.96));
    backdrop-filter:blur(24px);
    z-index:10;
    display:flex;
    flex-direction:column;
    height:100vh;
    overflow:hidden;
}

.logo{
    height:60px;
    display:flex;
    align-items:center;
    gap:12px;
    padding:0 8px 10px;
    border-bottom:1px solid rgba(90,178,255,.12);
}

.logoCube{
    width:40px; height:40px;
    border-radius:12px;
    display:grid;
    place-items:center;
    font-size:22px;
    color:#fff;
    background:linear-gradient(135deg,#08eaff,#416cff 55%,#8758ff);
    box-shadow:0 0 15px rgba(0,220,255,.6),inset 0 0 15px rgba(255,255,255,.22);
}

.logoText{ font-size:18px; letter-spacing:1px; font-weight:700; }
.logoSub{ font-size:9px; color:#67caff; margin-top:2px; letter-spacing:.8px; }

.nav{
    margin-top:12px;
    flex:1;
    overflow-y:auto;
    scrollbar-width:none;
    display:flex;
    flex-direction:column;
    gap:4px;
}
.nav::-webkit-scrollbar{ display:none; }

.navItem{
    height:42px;
    display:flex;
    align-items:center;
    gap:12px;
    padding:0 12px;
    border:1px solid transparent;
    border-radius:11px;
    color:#a7b8cb;
    cursor:pointer;
    transition:.2s;
    font-size:13px;
    user-select:none;
}
.navItem:hover{
    background:rgba(20,100,200,.15);
    color:#fff;
    border-color:rgba(56,189,248,0.2);
}
.navItem.active{
    color:#fff;
    border-color:rgba(40,145,255,.45);
    background:linear-gradient(90deg,rgba(20,102,255,.6),rgba(21,77,157,.25));
    box-shadow:inset 0 0 20px rgba(0,120,255,.18),0 0 15px rgba(0,110,255,.15);
}
.navIcon{ width:20px; text-align:center; font-size:16px; }
.navArrow{ margin-left:auto; color:#55708d; font-size:11px; }

.quote{
    position:relative;
    margin-top:auto;
    padding:14px;
    border:1px solid rgba(80,160,255,.2);
    border-radius:14px;
    overflow:hidden;
    flex-shrink:0;
    background:linear-gradient(135deg,rgba(8,28,53,.86),rgba(7,20,37,.74));
}
.quote:after{
    content:""; position:absolute; width:130px; height:130px;
    right:-45px; bottom:-55px; border-radius:50%;
    background:radial-gradient(circle,rgba(0,180,255,.22),transparent 65%);
}
.quoteText{ position:relative; z-index:1; font-size:13px; line-height:1.5; font-style:italic; color:#eaf4ff; }
.quoteSub{ position:relative; z-index:1; margin-top:8px; font-size:9px; color:#68819c; letter-spacing:0.5px; }

/* ================= MAIN CONTAINER ================= */
.main{
    min-width:0;
    height:100vh;
    padding:12px;
    display:grid;
    grid-template-rows:68px 84px minmax(0,1fr) 230px 48px;
    gap:9px;
    overflow:hidden;
}

/* ================= GLASS PANEL ================= */
.glass{
    border:1px solid var(--border);
    border-radius:14px;
    background:linear-gradient(145deg,rgba(7,27,49,.86),rgba(3,16,31,.78));
    box-shadow:var(--shadow);
    backdrop-filter:blur(18px);
}

/* ================= TOPBAR ================= */
.topbar{ display:flex; align-items:center; gap:12px; }

.search{
    flex:1; height:56px;
    display:flex; align-items:center; gap:12px; padding:0 14px;
    border:1px solid rgba(48,156,255,.38);
    border-radius:14px;
    background:linear-gradient(135deg,rgba(8,31,59,.85),rgba(4,19,38,.72));
    box-shadow:var(--shadow);
}

.aiOrb{
    width:32px; height:32px; flex:0 0 32px;
    border-radius:50%; display:grid; place-items:center;
    background:radial-gradient(circle,#00eaff,#0e71ff 60%,transparent 68%);
    box-shadow:0 0 18px rgba(0,225,255,.5);
    font-size:14px;
}

.searchText{ min-width:0; flex:1; display:flex; flex-direction:column; justify-content:center; }

.searchMainInput{
    width:100%; background:transparent; border:none; color:#f2f7ff;
    font-size:13px; font-weight:600;
}
.searchMainInput::placeholder{ color:#65819e; font-weight:400; }

.promptChips{
    display:flex; gap:6px; overflow-x:auto; scrollbar-width:none;
    margin-top:3px; padding-bottom:1px;
}
.promptChips::-webkit-scrollbar{ display:none; }
.chip{
    padding:2px 8px; border-radius:6px; font-size:10px; cursor:pointer;
    white-space:nowrap; transition:all 0.15s; border:1px solid transparent;
}
.chip:hover{ transform:translateY(-1px); }
.chip-glucose{ background:rgba(0,234,255,0.12); color:#38bdf8; border-color:rgba(56,189,248,0.3); font-weight:700; }
.chip-crop{ background:rgba(0,245,155,0.1); color:#00f59b; border-color:rgba(0,245,155,0.25); }
.chip-animal{ background:rgba(255,216,77,0.1); color:#ffd84d; border-color:rgba(255,216,77,0.25); }
.chip-drug{ background:rgba(168,85,247,0.1); color:#c084fc; border-color:rgba(168,85,247,0.25); }
.chip-pdb{ background:rgba(244,63,94,0.1); color:#fb7185; border-color:rgba(244,63,94,0.25); }

.sendBtn{
    width:36px; height:36px; border:0; border-radius:10px;
    cursor:pointer; background:linear-gradient(135deg,#087dff,#624dff);
    box-shadow:0 0 16px rgba(30,117,255,.45);
    display:grid; place-items:center; font-size:14px;
    transition:0.15s;
}
.sendBtn:hover{ transform:scale(1.05); }

.topButton{
    width:40px; height:40px; border:1px solid var(--border);
    border-radius:11px; background:rgba(9,28,49,.8);
    cursor:pointer; font-size:14px; transition:.15s;
}
.topButton:hover{ background:rgba(20,60,110,.8); border-color:#38bdf8; }

.profile{
    display:flex; align-items:center; gap:10px; padding:0 8px; min-width:170px;
}
.avatar{
    width:38px; height:38px; border-radius:50%; display:grid;
    place-items:center; font-weight:700; font-size:12px;
    background:linear-gradient(135deg,#2169c8,#684dff);
    box-shadow:0 0 16px rgba(65,111,255,.35);
}
.profileName{ font-size:12px; font-weight:600; }
.profileRole{ margin-top:1px; font-size:10px; color:#7188a3; }

/* ================= KPIS ================= */
.kpis{
    display:grid;
    grid-template-columns:repeat(5,1fr) 1.25fr;
    gap:9px;
}
.kpi, .dateCard{
    border:1px solid var(--border); border-radius:12px;
    background:linear-gradient(145deg,rgba(8,30,53,.82),rgba(5,19,35,.7));
    box-shadow:var(--shadow); overflow:hidden; position:relative;
    padding:12px;
}
.kpiIcon{ font-size:18px; color:#00cfff; }
.kpiTitle{ position:absolute; left:44px; top:12px; font-size:9px; color:#7891aa; font-weight:600; letter-spacing:0.5px; }
.kpiValue{ margin-top:4px; font-size:20px; font-weight:700; }
.kpiTrend{ font-size:9px; color:var(--green); margin-top:2px; font-weight:600; }
.kpiGlow{ position:absolute; width:80px; height:80px; right:-35px; bottom:-45px; border-radius:50%; background:radial-gradient(circle,rgba(0,160,255,.22),transparent 70%); }

.dateCard{ padding:10px 14px; }
.dateSmall{ color:#839bb4; font-size:10px; }
.dateTime{ margin-top:4px; font-size:21px; font-weight:700; }
.dateGood{ margin-top:2px; font-size:9px; color:#839bb4; }
.planet{
    position:absolute; right:-20px; top:-20px; width:95px; height:95px; border-radius:50%;
    background:radial-gradient(circle at 35% 30%,#6f8e9f,#1c3545 43%,#061422 68%);
    box-shadow:inset -12px -10px 20px rgba(0,0,0,.65),0 0 25px rgba(0,170,255,.15);
}

/* ================= WORKSPACE MIDDLE ================= */
.workspace{
    min-height:0;
    display:grid;
    grid-template-columns:minmax(480px,1.2fr) 340px 240px;
    gap:9px;
}

/* ================= 3D VIEWER ================= */
.viewer{
    min-width:0;
    display:grid;
    grid-template-rows:44px minmax(0,1fr) 46px;
    overflow:hidden;
    position:relative;
}

.tabs{
    display:flex; align-items:center; gap:4px; padding:6px 10px;
    border-bottom:1px solid rgba(90,170,255,.12);
}
.tab{
    padding:6px 11px; border-radius:8px; color:#8096ad; font-size:11px;
    cursor:pointer; transition:.15s; user-select:none;
}
.tab:hover{ color:#fff; background:rgba(255,255,255,0.05); }
.tab.active{
    color:#fff; font-weight:600;
    background:linear-gradient(135deg,#176dff,#5c4bff);
    box-shadow:0 0 12px rgba(39,107,255,.35);
}

.canvasWrap{
    position:relative;
    min-height:280px;
    height:100%;
    overflow:hidden;
    margin:0 8px;
    border-radius:10px;
    background:radial-gradient(circle at 50% 45%,rgba(14,78,128,.18),transparent 55%),#010811;
}

#threeCanvas{
    width:100%; height:100%; display:block;
}

/* TOOLBAR OVERLAY */
.viewerTools{
    position:absolute; left:12px; top:12px;
    display:flex; flex-direction:column; gap:6px; z-index:5;
}
.viewerTool{
    width:32px; height:32px; border:1px solid rgba(90,178,255,.25);
    border-radius:8px; background:rgba(5,20,38,.85); backdrop-filter:blur(10px);
    cursor:pointer; display:grid; place-items:center; font-size:13px;
    transition:.15s;
}
.viewerTool:hover{
    background:rgba(20,80,160,.85); border-color:#38bdf8;
    box-shadow:0 0 10px rgba(56,189,248,.4);
}

/* BINDING PANEL */
.bindingPanel{
    position:absolute; right:12px; top:12px; width:220px;
    padding:12px; border-radius:12px;
    border:1px solid rgba(56,189,248,.35);
    background:linear-gradient(145deg,rgba(4,22,44,.92),rgba(2,14,28,.88));
    backdrop-filter:blur(14px);
    box-shadow:0 0 25px rgba(0,140,255,.2);
    z-index:5; font-size:11px;
    transition:all 0.2s;
}
.bindingTitle{
    display:flex; justify-content:space-between; align-items:center;
    font-weight:700; color:#38bdf8; margin-bottom:6px; font-size:12px;
}
.bindingClose{ cursor:pointer; color:#94a3b8; font-size:14px; }
.bindingClose:hover{ color:#fff; }
.bindingMeta{ color:#94a3b8; margin-bottom:8px; line-height:1.4; font-size:10px; border-bottom:1px solid rgba(90,178,255,.15); padding-bottom:6px; }

.residuesList{ max-height:140px; overflow-y:auto; scrollbar-width:none; display:flex; flex-direction:column; gap:4px; }
.residuesList::-webkit-scrollbar{ display:none; }
.residue{
    display:flex; justify-content:space-between; align-items:center;
    padding:3px 6px; border-radius:6px; cursor:pointer;
    background:rgba(14,38,64,0.4); border:1px solid transparent;
    transition:.15s;
}
.residue:hover{
    background:rgba(20,75,130,0.8); border-color:#38bdf8; transform:translateX(2px);
}
.resName{ font-weight:600; color:#e2e8f0; }
.resDist{ font-size:10px; color:#38bdf8; font-family:monospace; }

.legend{ margin-top:8px; padding-top:6px; border-top:1px solid rgba(90,178,255,.15); display:grid; grid-template-columns:1fr 1fr; gap:4px; font-size:9px; color:#94a3b8; }
.legendItem{ display:flex; align-items:center; gap:4px; }
.dot{ width:6px; height:6px; border-radius:50%; }
.dot-hbond{ background:#00f59b; box-shadow:0 0 6px #00f59b; }
.dot-hydro{ background:#ffd84d; box-shadow:0 0 6px #ffd84d; }
.dot-electro{ background:#ff4d67; box-shadow:0 0 6px #ff4d67; }
.dot-pi{ background:#a855f7; box-shadow:0 0 6px #a855f7; }

/* WORKSPACE ALTERNATIVE PANELS */
.workspacePanel{
    position:relative; min-height:0; overflow-y:auto;
    margin:0 8px; padding:16px; border-radius:10px;
    background:radial-gradient(circle at 50% 45%,rgba(14,78,128,.15),transparent 45%),#010811;
    display:none; color:#e2e8f0;
}
.workspacePanel.active{ display:block; }

.seqGrid{ display:grid; grid-template-columns:repeat(auto-fill,minmax(48px,1fr)); gap:6px; margin-top:12px; }
.seqChip{
    padding:6px 2px; text-align:center; border-radius:6px;
    background:rgba(14,38,64,.7); border:1px solid rgba(56,189,248,.2);
    font-size:10px; cursor:pointer; transition:.15s;
}
.seqChip:hover{ border-color:#38bdf8; background:rgba(20,75,130,.8); transform:translateY(-2px); }
.seqResName{ font-weight:700; color:#38bdf8; }
.seqResNum{ font-size:8px; color:#94a3b8; margin-top:1px; }

.propTable{ width:100%; border-collapse:collapse; margin-top:10px; font-size:11px; }
.propTable th, .propTable td{ padding:8px 10px; text-align:left; border-bottom:1px solid rgba(90,178,255,.12); }
.propTable th{ color:#7dd3fc; font-weight:600; font-size:10px; text-transform:uppercase; letter-spacing:0.5px; }

.analysisPlotPreview{ max-width:100%; border-radius:8px; border:1px solid rgba(56,189,248,.3); margin-top:8px; cursor:pointer; }

/* VIEWER BOTTOM BAR */
.viewerBottom{
    display:flex; align-items:center; gap:6px; padding:6px 12px;
    border-top:1px solid rgba(90,170,255,.12);
}
.styleBtn{
    padding:5px 10px; border-radius:8px; font-size:10px; cursor:pointer;
    border:1px solid rgba(90,178,255,.2); background:rgba(10,31,57,.6);
    transition:.15s; user-select:none;
}
.styleBtn:hover{ border-color:#38bdf8; color:#fff; }
.styleBtn.active{
    background:linear-gradient(135deg,#168cff,#684dff);
    color:#fff; border-color:transparent; font-weight:600;
}
.viewerSpacer{ flex:1; }

.controlBtn{
    padding:5px 10px; border-radius:8px; font-size:10px; cursor:pointer;
    border:1px solid var(--border); background:rgba(10,31,57,.8);
    transition:.15s; user-select:none;
}
.controlBtn:hover{ background:rgba(20,70,130,.8); border-color:#38bdf8; }

/* FULLSCREEN VIEWER MODE */
.viewer.fullscreenMode{
    position:fixed !important; top:0 !important; left:0 !important;
    width:100vw !important; height:100vh !important; z-index:999999 !important;
    margin:0 !important; border-radius:0 !important; background:#010812 !important;
    border:none !important; display:flex !important; flex-direction:column !important;
}
.viewer.fullscreenMode .canvasWrap{ flex:1 !important; height:auto !important; margin:0 10px !important; }
.exitFullscreenBtn{
    position:absolute; top:12px; right:12px; z-index:1000000;
    background:rgba(220,38,38,.85); color:white; border:1px solid rgba(255,255,255,.3);
    padding:6px 14px; border-radius:8px; font-size:11px; font-weight:600;
    cursor:pointer; display:none; backdrop-filter:blur(8px);
}
.viewer.fullscreenMode .exitFullscreenBtn{ display:block !important; }

/* ================= AGENT CENTER ================= */
.agent{
    min-width:0; padding:14px; display:flex; flex-direction:column;
    gap:10px; overflow:hidden;
}
.panelTitle{
    display:flex; justify-content:space-between; align-items:center;
    font-size:12px; font-weight:700; color:#fff;
}
.statusBadge{
    display:flex; align-items:center; gap:5px; font-size:10px;
    padding:2px 8px; border-radius:12px;
    background:rgba(0,245,155,.1); color:var(--green); border:1px solid rgba(0,245,155,.25);
}
.statusDot{ width:6px; height:6px; border-radius:50%; background:var(--green); box-shadow:0 0 6px var(--green); }

.sessionCard{
    padding:10px 12px; border-radius:10px;
    border:1px solid rgba(90,178,255,.15);
    background:rgba(10,31,57,.5); display:grid;
    grid-template-columns:auto 1fr; gap:8px 10px; font-size:11px;
}
.sessionLabel{ color:#7e94ad; font-size:9px; font-weight:600; letter-spacing:0.5px; }
.sessionVal{ font-weight:700; color:#f1f5f9; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }

.workflow{
    flex:1; overflow-y:auto; scrollbar-width:none;
    display:flex; flex-direction:column; gap:5px; margin-top:2px;
}
.workflow::-webkit-scrollbar{ display:none; }
.workflowTitle{ font-size:10px; font-weight:700; color:#7891aa; text-transform:uppercase; letter-spacing:0.5px; margin-bottom:2px; }

.step{
    display:flex; align-items:center; gap:8px; padding:5px 8px;
    border-radius:6px; font-size:10px; color:#94a3b8;
    background:rgba(10,31,57,.3); border:1px solid transparent;
}
.stepNum{ width:16px; height:16px; border-radius:50%; display:grid; place-items:center; font-size:8px; background:rgba(255,255,255,.08); }
.step.done{ color:#e2e8f0; border-color:rgba(0,245,155,.15); }
.step.done .stepNum{ background:rgba(0,245,155,.2); color:var(--green); font-weight:700; }
.step.running{ color:#fff; border-color:rgba(56,189,248,.35); background:rgba(20,80,160,.2); font-weight:600; }
.step.running .stepNum{ background:#168cff; color:#fff; }

.progressBox{ margin-top:auto; padding-top:4px; }
.progressTrack{ width:100%; height:6px; border-radius:3px; background:rgba(255,255,255,.08); overflow:hidden; }
.progressFill{ height:100%; border-radius:3px; background:linear-gradient(90deg,#168cff,#00f59b); transition:width .3s; }
.progressMeta{ display:flex; justify-content:space-between; font-size:9px; color:#839bb4; margin-top:4px; }

.agentButtons{ display:flex; gap:6px; margin-top:6px; }
.agentBtn{
    flex:1; padding:6px; border-radius:8px; border:1px solid var(--border);
    background:rgba(10,31,57,.7); font-size:11px; cursor:pointer;
    text-align:center; transition:.15s; font-weight:600;
}
.agentBtn:hover{ background:rgba(20,70,130,.8); border-color:#38bdf8; }
.agentBtn-run{ background:linear-gradient(135deg,#087dff,#624dff); border-color:transparent; color:#fff; }

/* ================= TOOL CONNECTORS ================= */
.connectors{
    min-width:0; padding:14px; display:flex; flex-direction:column;
    gap:8px; overflow:hidden;
}
.connectorsList{
    flex:1; overflow-y:auto; scrollbar-width:none; display:flex;
    flex-direction:column; gap:4px;
}
.connectorsList::-webkit-scrollbar{ display:none; }

.connector{
    display:flex; align-items:center; gap:8px; padding:6px 10px;
    border-radius:8px; background:rgba(10,31,57,.45);
    border:1px solid rgba(90,178,255,.1); cursor:pointer; font-size:11px;
    transition:.15s; user-select:none;
}
.connector:hover{
    background:rgba(14,48,88,.6); border-color:#38bdf8; transform:translateX(2px);
}
.connIcon{ font-size:13px; width:18px; text-align:center; }
.connName{ font-weight:600; color:#e2e8f0; }
.connStatus{
    margin-left:auto; font-size:9px; padding:2px 6px; border-radius:8px;
    font-weight:600;
}
.connStatus.ok{ background:rgba(0,245,155,.12); color:#00f59b; border:1px solid rgba(0,245,155,.25); }
.connStatus.run{ background:rgba(56,189,248,.15); color:#38bdf8; border:1px solid rgba(56,189,248,.3); }
.connStatus.ready{ background:rgba(255,255,255,.08); color:#cbd5e1; }
.connStatus.off{ background:rgba(239,68,68,.12); color:#f87171; border:1px solid rgba(239,68,68,.25); }

/* ================= BOTTOM PANELS ================= */
.bottom{
    display:grid; grid-template-columns:1fr 1fr; gap:9px; min-height:0;
}

.logs{
    min-width:0; display:flex; flex-direction:column; padding:12px;
    overflow:hidden;
}
.logsHeader{
    display:flex; align-items:center; gap:8px; margin-bottom:8px;
    border-bottom:1px solid rgba(90,170,255,.12); padding-bottom:6px;
}
.logTab{
    font-size:11px; color:#748da7; cursor:pointer; padding:3px 8px;
    border-radius:6px; transition:.15s; user-select:none;
}
.logTab:hover{ color:#fff; background:rgba(255,255,255,.05); }
.logTab.active{ color:#fff; font-weight:600; background:rgba(22,140,255,.2); color:#38bdf8; }
.clearBtn{ margin-left:auto; color:#00ed9a; font-size:10px; cursor:pointer; user-select:none; }
.clearBtn:hover{ text-decoration:underline; }

.logSearch{
    width:100%; padding:5px 10px; border-radius:6px;
    border:1px solid rgba(90,178,255,.15); background:rgba(5,19,35,.8);
    font-size:10px; margin-bottom:6px; color:#fff;
}
.logBody{
    flex:1; overflow-y:auto; scrollbar-width:thin;
    font-family:"Fira Code",Consolas,monospace; font-size:10px;
    line-height:1.45; display:flex; flex-direction:column; gap:3px;
}
.logLine{ color:#cbd5e1; }
.logTime{ color:#64748b; margin-right:4px; }
.logInfo{ color:#38bdf8; font-weight:600; }
.logSuccess{ color:#00f59b; font-weight:600; }
.logWarn{ color:#facc15; font-weight:600; }
.logError{ color:#f87171; font-weight:600; }
.logAI{ color:#c084fc; font-weight:700; }

.results{
    min-width:0; display:flex; flex-direction:column; padding:12px;
    overflow:hidden;
}
.resultsHeader{
    display:flex; justify-content:space-between; align-items:center;
    margin-bottom:8px; border-bottom:1px solid rgba(90,170,255,.12); padding-bottom:6px;
}
.resultGrid{
    flex:1; overflow-y:auto; scrollbar-width:none;
    display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr));
    gap:8px; align-content:start;
}
.resultCard{
    padding:8px; border-radius:8px; background:rgba(10,31,57,.5);
    border:1px solid rgba(90,178,255,.15); cursor:pointer; text-align:center;
    transition:.15s;
}
.resultCard:hover{
    background:rgba(20,70,130,.7); border-color:#38bdf8; transform:translateY(-2px);
}
.resultPreview{ font-size:22px; margin-bottom:4px; }
.resultName{ font-size:10px; font-weight:600; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; color:#e2e8f0; }
.resultMeta{ font-size:8px; color:#7891aa; margin-top:2px; }

/* ================= QUICK ACTIONS FOOTER ================= */
.quick{
    display:flex; align-items:center; gap:8px; padding:0 12px;
}
.quickTitle{ font-size:11px; font-weight:700; color:#7891aa; margin-right:4px; }
.quickBtn{
    padding:5px 11px; border-radius:7px; border:1px solid rgba(90,178,255,.2);
    background:rgba(10,31,57,.65); font-size:10px; cursor:pointer;
    transition:.15s; font-weight:600;
}
.quickBtn:hover{
    background:rgba(20,80,160,.8); border-color:#38bdf8; color:#fff;
}

/* ================= MODALS & OVERLAYS ================= */
.modalOverlay{
    position:fixed; top:0; left:0; width:100vw; height:100vh;
    background:rgba(1,8,18,.88); backdrop-filter:blur(20px);
    z-index:9999999; display:none; align-items:center; justify-content:center;
    padding:20px;
}
.modalOverlay.show{ display:flex; }

.modalBox{
    width:860px; max-width:95vw; max-height:88vh;
    background:linear-gradient(145deg,rgba(8,30,55,.96),rgba(4,18,34,.94));
    border:1px solid rgba(56,189,248,.35); border-radius:18px;
    box-shadow:0 0 50px rgba(0,150,255,.25); display:flex; flex-direction:column;
    overflow:hidden;
}
.modalHeader{
    padding:16px 20px; border-bottom:1px solid rgba(90,178,255,.15);
    display:flex; align-items:center; justify-content:space-between;
}
.modalTitle{ font-size:15px; font-weight:700; color:#f8fafc; }
.modalClose{ font-size:18px; cursor:pointer; background:none; border:none; color:#94a3b8; }
.modalClose:hover{ color:#fff; }
.modalBody{ padding:20px; overflow-y:auto; flex:1; font-size:12px; }

/* TOAST NOTIFICATION */
.toast{
    position:fixed; bottom:24px; right:24px; z-index:10000000;
    padding:10px 16px; border-radius:10px;
    background:linear-gradient(135deg,rgba(10,38,70,.95),rgba(4,20,38,.95));
    border:1px solid #38bdf8; box-shadow:0 0 25px rgba(56,189,248,.35);
    color:#fff; font-size:12px; pointer-events:none;
    opacity:0; transform:translateY(10px); transition:.2s;
}
.toast.show{ opacity:1; transform:translateY(0); }
.toastTitle{ font-weight:700; color:#38bdf8; margin-bottom:2px; font-size:11px; }
</style>
</head>
<body>

<div class="app">

<!-- ================= SIDEBAR ================= -->
<aside class="sidebar">
    <div class="logo">
        <div class="logoCube">⚛</div>
        <div>
            <div class="logoText">POLYMATHIX</div>
            <div class="logoSub">AI FOR SCIENTIFIC DISCOVERY</div>
        </div>
    </div>

    <div class="nav">
        <div class="navItem active" onclick="navSelect('Home', this)"><div class="navIcon">⌂</div><div>Home</div></div>
        <div class="navItem" onclick="navSelect('AI Chat', this)"><div class="navIcon">✦</div><div>AI Chat</div></div>
        <div class="navItem" onclick="navSelect('Research Sessions', this)"><div class="navIcon">⚗</div><div>Research Sessions</div></div>
        <div class="navItem" onclick="navSelect('Protocols', this)"><div class="navIcon">◈</div><div>Protocols</div></div>
        <div class="navItem" onclick="navSelect('Molecular Tools', this)"><div class="navIcon">⌘</div><div>Molecular Tools</div><div class="navArrow">⌄</div></div>
        <div class="navItem" onclick="navSelect('Simulations', this)"><div class="navIcon">△</div><div>Simulations</div><div class="navArrow">⌄</div></div>
        <div class="navItem" onclick="navSelect('Data Analysis', this)"><div class="navIcon">▥</div><div>Data Analysis</div><div class="navArrow">⌄</div></div>
        <div class="navItem" onclick="navSelect('Visualization', this)"><div class="navIcon">◇</div><div>Visualization</div><div class="navArrow">⌄</div></div>
        <div class="navItem" onclick="navSelect('3D Library', this)"><div class="navIcon">▦</div><div>3D Library</div></div>
        <div class="navItem" onclick="navSelect('Notebooks', this)"><div class="navIcon">▤</div><div>Notebooks</div></div>
        <div class="navItem" onclick="navSelect('Files & Data', this)"><div class="navIcon">□</div><div>Files & Data</div></div>
        <div class="navItem" onclick="navSelect('Settings', this)"><div class="navIcon">⚙</div><div>Settings</div></div>
    </div>

    <div class="quote">
        <div class="quoteText">“Science Today, Better Tomorrow.”</div>
        <div class="quoteSub">POLYMATHIX RESEARCH ENGINE</div>
    </div>
</aside>

<!-- ================= MAIN VIEW ================= -->
<main class="main">

<!-- TOPBAR -->
<header class="topbar">
    <div class="search">
        <div class="aiOrb">✦</div>
        <div class="searchText">
            <input type="text" class="searchMainInput" id="aiInput" placeholder="Ask Polymathix anything... (e.g. 'Show glucose binding pocket' or 'Run Crop Resilience')" onkeydown="if(event.key==='Enter') runAI()" />
            <div class="promptChips">
                <span class="chip chip-glucose" onclick="runAI('Show glucose binding site and identify residues within 4 Å')">🍬 Glucose Pocket (4.0 Å)</span>
                <span class="chip chip-crop" onclick="runAI('Run Crop Proteome & Thermal Adaptation protocol')">🌿 Crop Resilience</span>
                <span class="chip chip-animal" onclick="runAI('Run Veterinary Broad-Spectrum Antimicrobial protocol')">🐾 Veterinary Health</span>
                <span class="chip chip-drug" onclick="runAI('Synthesize novel drug with RDKit and Lipinski screening')">🧪 De-Novo Drug Design</span>
                <span class="chip chip-pdb" onclick="runAI('Load 1UBQ')">🧬 Fetch Ubiquitin (1UBQ)</span>
                <span class="chip chip-pdb" onclick="runAI('Load 4HHB')">🩸 Fetch Hemoglobin (4HHB)</span>
            </div>
        </div>
        <button class="sendBtn" onclick="runAI()">➤</button>
    </div>

    <button class="topButton" onclick="toggleAudio()" title="Sound / Audio Alerts">♩</button>
    <button class="topButton" onclick="toggleTheme()" title="Visual FX Glow">♧</button>

    <div class="profile">
        <div class="avatar">SS</div>
        <div>
            <div class="profileName">Lead Scientist</div>
            <div class="profileRole">Researcher</div>
        </div>
        <div style="cursor:pointer;color:#7891aa;font-size:12px;" onclick="openSettingsModal()">⌄</div>
    </div>
</header>

<!-- KPIS -->
<section class="kpis">
    <div class="kpi">
        <div class="kpiIcon">⚗</div>
        <div class="kpiTitle">ACTIVE SESSIONS</div>
        <div class="kpiValue">8</div>
        <div class="kpiTrend">↑ 2 active</div>
        <div class="kpiGlow"></div>
    </div>
    <div class="kpi">
        <div class="kpiIcon">▱</div>
        <div class="kpiTitle">CONNECTED TOOLS</div>
        <div class="kpiValue">12</div>
        <div class="kpiTrend">↑ 3 synced</div>
        <div class="kpiGlow"></div>
    </div>
    <div class="kpi">
        <div class="kpiIcon">▣</div>
        <div class="kpiTitle">RUNNING JOBS</div>
        <div class="kpiValue">28</div>
        <div class="kpiTrend">↑ 5 queued</div>
        <div class="kpiGlow"></div>
    </div>
    <div class="kpi">
        <div class="kpiIcon">◉</div>
        <div class="kpiTitle">TOTAL DATA</div>
        <div class="kpiValue">1.4 TB</div>
        <div class="kpiTrend">↑ 12% storage</div>
        <div class="kpiGlow"></div>
    </div>
    <div class="kpi">
        <div class="kpiIcon">ϟ</div>
        <div class="kpiTitle">SYSTEM UPTIME</div>
        <div class="kpiValue">99.8%</div>
        <div class="kpiTrend">Live Cluster</div>
        <div class="kpiGlow"></div>
    </div>
    <div class="dateCard">
        <div class="dateSmall">Tue, 13 Oct 2026</div>
        <div class="dateTime" id="clock">14:40</div>
        <div class="dateGood">Good Afternoon, Researcher!</div>
        <div class="planet"></div>
    </div>
</section>

<!-- WORKSPACE -->
<section class="workspace">

    <!-- 3D VIEWER -->
    <div class="viewer glass">
        <div class="tabs">
            <div class="tab active" onclick="switchWorkspaceTab('viewer', this)">3D Viewer</div>
            <div class="tab" onclick="switchWorkspaceTab('sequence', this)">Sequence</div>
            <div class="tab" onclick="switchWorkspaceTab('trajectory', this)">Trajectory</div>
            <div class="tab" onclick="switchWorkspaceTab('surfaces', this)">Surfaces</div>
            <div class="tab" onclick="switchWorkspaceTab('properties', this)">Properties</div>
            <div class="tab" onclick="switchWorkspaceTab('analysis', this)">Analysis</div>
        </div>

        <div class="canvasWrap" id="threeCanvasWrap">
            <canvas id="threeCanvas"></canvas>

            <div class="viewerTools">
                <button class="viewerTool" onclick="resetCamera()" title="Reset Camera View">↖</button>
                <button class="viewerTool" onclick="focusMolecule()" title="Focus Center">◎</button>
                <button class="viewerTool" onclick="toggleSurface()" title="Toggle Molecular Surface">◉</button>
                <button class="viewerTool" onclick="randomizeMolecule()" title="Reorient Model">✣</button>
                <button class="viewerTool" onclick="focusBindingPocket()" title="Focus Glucose Binding Pocket">⌖</button>
                <button class="viewerTool" onclick="takeSnapshot()" title="Save PNG Snapshot">📷</button>
                <button class="viewerTool" onclick="toggleViewerFullscreen()" title="Fullscreen 3D Mode">⛶</button>
                <button class="viewerTool" onclick="openExport()" title="Export 3D Geometry">↓</button>
            </div>

            <button class="exitFullscreenBtn" onclick="toggleViewerFullscreen()">✕ Exit Fullscreen (Esc)</button>

            <!-- BINDING PANEL -->
            <div class="bindingPanel" id="bindingPanel">
                <div class="bindingTitle">
                    <span>Binding Site Analysis</span>
                    <span class="bindingClose" onclick="closeBindingPanel()">×</span>
                </div>
                <div class="bindingMeta">
                    Ligand: <b style="color:#38bdf8">D-Glucose</b><br>
                    Distance cutoff: 4.0 Å<br>
                    Interacting residues (8)
                </div>
                <div class="residuesList" id="bindingResiduesList">
                    <!-- Populated dynamically -->
                </div>
                <div class="legend">
                    <div class="legendItem"><span class="dot dot-hbond"></span>H-Bond</div>
                    <div class="legendItem"><span class="dot dot-hydro"></span>Hydrophobic</div>
                    <div class="legendItem"><span class="dot dot-electro"></span>Electrostatic</div>
                    <div class="legendItem"><span class="dot dot-pi"></span>π-Stacking</div>
                </div>
            </div>
        </div>

        <!-- SIBLING WORKSPACE PANELS -->
        <div class="workspacePanel" id="sequencePanel">
            <div style="font-size:13px;font-weight:700;color:#38bdf8;display:flex;justify-content:space-between;">
                <span>Primary Amino Acid Sequence (1CRN - Chain A)</span>
                <span style="font-size:10px;color:#94a3b8;">46 Residues | High Resolution</span>
            </div>
            <div class="seqGrid" id="seqGridContainer"></div>
        </div>

        <div class="workspacePanel" id="trajectoryPanel">
            <div style="font-size:13px;font-weight:700;color:#38bdf8;">Molecular Dynamics Production Trajectory</div>
            <div style="margin-top:6px;font-size:11px;color:#94a3b8;">Frames: 1500 / 1500 | Ensemble: NPT (300K, 1 bar) | Integrator: Langevin (2 fs)</div>
            <div style="margin-top:14px;display:flex;align-items:center;gap:10px;">
                <button class="controlBtn" id="btnPlayTraj" onclick="toggleTrajectoryPlay()">▶ Play Trajectory</button>
                <input type="range" min="0" max="1500" value="750" style="flex:1" id="trajSlider" oninput="scrubTrajectory(this.value)" />
                <span id="trajFrame" style="font-size:11px;font-family:monospace;min-width:60px;">Frame 750</span>
            </div>
            <div style="margin-top:16px;padding:12px;background:rgba(10,31,57,0.6);border-radius:8px;border:1px solid rgba(56,189,248,0.2);">
                <div style="font-size:11px;color:#7dd3fc;font-weight:600;">RMSD & Energy Stability Profile</div>
                <div style="font-size:10px;color:#cbd5e1;margin-top:4px;">Average Backbone RMSD: 0.84 ± 0.04 Å. System maintains crystallographic stability without conformational drift.</div>
            </div>
        </div>

        <div class="workspacePanel" id="surfacesPanel">
            <div style="font-size:13px;font-weight:700;color:#38bdf8;">Molecular Potential & Surfaces</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:10px;margin-top:12px;">
                <div style="padding:12px;background:rgba(10,31,57,0.6);border-radius:8px;border:1px solid rgba(56,189,248,0.2);cursor:pointer;" onclick="toggleSurface()">
                    <div style="font-weight:600;color:#38bdf8;font-size:11px;">Solvent Accessible Surface (SASA)</div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Rolling probe radius: 1.4 Å | Analytical Conolly algorithm</div>
                </div>
                <div style="padding:12px;background:rgba(10,31,57,0.6);border-radius:8px;border:1px solid rgba(56,189,248,0.2);cursor:pointer;" onclick="showToast('Surface','Electrostatic Coulombic potential mapped')">
                    <div style="font-weight:600;color:#ff4d67;font-size:11px;">Poisson-Boltzmann Electrostatics</div>
                    <div style="font-size:10px;color:#94a3b8;margin-top:4px;">Coulombic continuum charge distribution (-10 to +10 kT/e)</div>
                </div>
            </div>
        </div>

        <div class="workspacePanel" id="propertiesPanel">
            <div style="font-size:13px;font-weight:700;color:#38bdf8;">Physicochemical Properties Dossier</div>
            <table class="propTable" id="propertiesTable"><tbody></tbody></table>
        </div>

        <div class="workspacePanel" id="analysisPanel">
            <div style="font-size:13px;font-weight:700;color:#38bdf8;">Active Scientific Analysis Visualizations</div>
            <div style="margin-top:6px;font-size:11px;color:#94a3b8;">Deep Non-Linear Manifold Projection & Autonomous Minimization Curves</div>
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-top:12px;">
                <div style="background:rgba(10,31,57,0.6);padding:10px;border-radius:8px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:10px;color:#7dd3fc;font-weight:600;">Deep Latent Space (RBF Kernel PCA)</div>
                    <img src="assets/deep_pca_comparison.png" class="analysisPlotPreview" onclick="window.open(this.src)" onerror="this.style.display='none'" />
                </div>
                <div style="background:rgba(10,31,57,0.6);padding:10px;border-radius:8px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:10px;color:#7dd3fc;font-weight:600;">Energy Minimization Convergence</div>
                    <img src="assets/energy_plot.png" class="analysisPlotPreview" onclick="window.open(this.src)" onerror="this.style.display='none'" />
                </div>
            </div>
        </div>

        <!-- VIEWER BOTTOM -->
        <div class="viewerBottom">
            <button class="styleBtn active" id="btnRepCartoon" onclick="setRepresentation('cartoon', this)">Cartoon</button>
            <button class="styleBtn" id="btnRepSurface" onclick="setRepresentation('surface', this)">Surface</button>
            <button class="styleBtn" id="btnRepSticks" onclick="setRepresentation('sticks', this)">Sticks</button>
            <button class="styleBtn" id="btnRepSphere" onclick="setRepresentation('sphere', this)">Sphere</button>
            <button class="styleBtn" id="btnRepMesh" onclick="setRepresentation('mesh', this)">Mesh</button>

            <div class="viewerSpacer"></div>

            <button class="controlBtn" onclick="toggleQuality()">Quality ▾</button>
            <button class="controlBtn" onclick="takeSnapshot()">📷</button>
            <button class="controlBtn" onclick="toggleViewerFullscreen()">⛶ Fullscreen 3D</button>
            <button class="controlBtn" onclick="openExport()">↓ Export 3D</button>
        </div>
    </div>

    <!-- AI AGENT CONTROL CENTER -->
    <div class="agent glass">
        <div class="panelTitle">
            <span>🧠 AI Agent Control Center</span>
            <button class="controlBtn" onclick="openSessionModal()" style="font-size:9px;padding:3px 7px;">⛶ Fullscreen</button>
            <div class="statusBadge" id="sessionStatusDisplay"><span class="statusDot"></span>Active</div>
        </div>

        <div class="sessionCard">
            <div class="sessionLabel">SESSION</div>
            <div class="sessionVal" id="sessionNameDisplay">MembraneONE</div>
            <div class="sessionLabel">MODEL</div>
            <div class="sessionVal">AI Research Agent</div>
            <div class="sessionLabel">PROTOCOL</div>
            <div class="sessionVal" id="protocolNameDisplay" style="color:#38bdf8;">Glucose Binding Pocket (4.0 Å)</div>
        </div>

        <div class="workflow">
            <div class="workflowTitle">Workflow Steps</div>
            <div id="workflowStepsContainer"></div>
        </div>

        <div class="progressBox">
            <div class="progressTrack"><div class="progressFill" id="progressFill" style="width:65%;"></div></div>
            <div class="progressMeta">
                <span id="progressValue">65%</span>
                <span id="timeRemainingDisplay">Estimated time: 42m remaining</span>
            </div>
        </div>

        <div class="agentButtons">
            <button class="agentBtn" onclick="triggerAgentControl('pause')">⏸ Pause</button>
            <button class="agentBtn" onclick="triggerAgentControl('stop')">■ Stop</button>
            <button class="agentBtn agentBtn-run" onclick="triggerAgentControl('run')">▶ Run</button>
        </div>
    </div>

    <!-- TOOL CONNECTORS -->
    <div class="connectors glass">
        <div class="panelTitle">
            <span>🔌 Tool Connectors</span>
            <button class="controlBtn" onclick="openConnectorsModal()">Manage</button>
        </div>

        <div class="connectorsList" id="connectorsList">
            <!-- Populated dynamically -->
        </div>
    </div>

</section>

<!-- BOTTOM -->
<section class="bottom">

    <!-- TERMINAL / LOGS -->
    <div class="logs glass">
        <div class="logsHeader">
            <div class="logTab active" onclick="switchLogTab('all', this)">▣ Terminal / Logs</div>
            <div class="logTab" onclick="switchLogTab('analysis', this)">Analysis Output</div>
            <div class="logTab" onclick="switchLogTab('plots', this)">Plots</div>
            <div class="logTab" onclick="switchLogTab('system', this)">System Messages</div>
            <div class="clearBtn" onclick="clearLogs()">● Clear</div>
        </div>

        <input type="text" class="logSearch" id="logSearch" placeholder="Search terminal logs..." oninput="filterLogs()" />

        <div class="logBody" id="logBody"></div>
    </div>

    <!-- RESULTS -->
    <div class="results glass">
        <div class="resultsHeader">
            <div style="font-size:11px;font-weight:700;">📊 Results & Visualizations</div>
            <button class="controlBtn" onclick="openResultsModal()">View All</button>
        </div>

        <div class="resultGrid" id="resultGrid"></div>
    </div>

</section>

<!-- QUICK ACTIONS FOOTER -->
<footer class="quick glass">
    <div class="quickTitle">Quick Actions</div>
    <button class="quickBtn" onclick="triggerQuickAction('new_session')">＋ New Session</button>
    <button class="quickBtn" onclick="triggerQuickAction('run_protocol')">◈ Run Protocol</button>
    <button class="quickBtn" onclick="triggerQuickAction('analyze_data')">∫ Analyze Data</button>
    <button class="quickBtn" onclick="triggerQuickAction('generate_plot')">▥ Generate Plot</button>
    <button class="quickBtn" onclick="triggerQuickAction('create_report')">▤ Create Report</button>
    <button class="quickBtn" onclick="openExport()">↓ Export All</button>
</footer>

</main>

</div>

<!-- ================= MODALS ================= -->

<!-- SESSION MODAL -->
<div class="modalOverlay" id="sessionModalOverlay">
    <div class="modalBox">
        <div class="modalHeader">
            <div style="display:flex;align-items:center;gap:10px;">
                <span style="font-size:20px;">🧠</span>
                <div>
                    <div class="modalTitle" id="modalSessionTitle">Research Session: MembraneONE</div>
                    <div style="font-size:10px;color:#38bdf8;" id="modalSessionSubtitle">Protocol: Glucose Binding Pocket | Model: AI Research Agent</div>
                </div>
            </div>
            <button class="modalClose" onclick="closeSessionModal()">✕</button>
        </div>
        <div class="modalBody">
            <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:16px;">
                <div style="background:rgba(10,31,57,0.6);padding:12px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:10px;color:#7dd3fc;font-weight:600;text-transform:uppercase;">Active Protocol</div>
                    <div style="font-size:16px;font-weight:700;margin-top:4px;color:#fff;" id="modalProtocolName">Glucose Binding Pocket (4.0 Å)</div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Target: D-Glucose / Crambin Hydrophobic Cavity</div>
                </div>
                <div style="background:rgba(10,31,57,0.6);padding:12px;border-radius:10px;border:1px solid rgba(56,189,248,0.2);">
                    <div style="font-size:10px;color:#7dd3fc;font-weight:600;text-transform:uppercase;">Computational Engine</div>
                    <div style="font-size:16px;font-weight:700;margin-top:4px;color:#00f59b;">● Active Converged</div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:2px;" id="modalTimeRemaining">Estimated time: 42m remaining</div>
                </div>
            </div>

            <div style="font-size:12px;font-weight:700;color:#e2e8f0;margin-bottom:8px;">Protocol Execution Pipeline</div>
            <div id="modalWorkflowSteps" style="display:flex;flex-direction:column;gap:6px;"></div>

            <div style="display:flex;gap:8px;margin-top:20px;border-top:1px solid rgba(90,178,255,0.15);padding-top:14px;">
                <button class="quickBtn" onclick="triggerAgentControl('pause')">⏸ Pause Session</button>
                <button class="quickBtn" onclick="triggerAgentControl('stop')">■ Stop Session</button>
                <button class="quickBtn" onclick="triggerAgentControl('run')">▶ Resume Execution</button>
                <button class="quickBtn" style="margin-left:auto;" onclick="triggerQuickAction('create_report')">▤ Export Dossier</button>
            </div>
        </div>
    </div>
</div>

<!-- EXPORT MODAL -->
<div class="modalOverlay" id="exportOverlay">
    <div class="modalBox" style="width:650px;">
        <div class="modalHeader">
            <div class="modalTitle">↓ Export 3D Model & Scientific Data</div>
            <button class="modalClose" onclick="closeExport()">✕</button>
        </div>
        <div class="modalBody">
            <div style="font-size:12px;font-weight:600;color:#7dd3fc;margin-bottom:10px;">Select Export Format</div>
            <div style="display:grid;grid-template-columns:repeat(5,1fr);gap:8px;margin-bottom:20px;">
                <button class="styleBtn active" onclick="setExportFormat('glb', this)">◈ GLB</button>
                <button class="styleBtn" onclick="setExportFormat('obj', this)">◇ OBJ</button>
                <button class="styleBtn" onclick="setExportFormat('stl', this)">△ STL</button>
                <button class="styleBtn" onclick="setExportFormat('gltf', this)">□ GLTF</button>
                <button class="styleBtn" onclick="setExportFormat('ply', this)">▦ PLY</button>
            </div>
            <div style="font-size:11px;color:#94a3b8;line-height:1.6;margin-bottom:20px;">
                Includes: 3D Protein Backbone, CPK Atoms, D-Glucose Ligand coordinates, and 8 active site hydrogen bond interactions.
            </div>
            <div style="display:flex;justify-content:flex-end;gap:8px;">
                <button class="quickBtn" onclick="closeExport()">Cancel</button>
                <button class="agentBtn agentBtn-run" id="btnDoExport" style="flex:0;padding:6px 18px;" onclick="performExport()">Download Model</button>
            </div>
        </div>
    </div>
</div>

<!-- RESULTS VIEW ALL MODAL -->
<div class="modalOverlay" id="resultsModalOverlay">
    <div class="modalBox">
        <div class="modalHeader">
            <div class="modalTitle">📊 All Generated Scientific Results & Artifacts</div>
            <button class="modalClose" onclick="closeResultsModal()">✕</button>
        </div>
        <div class="modalBody">
            <div class="resultGrid" id="modalResultGrid" style="grid-template-columns:repeat(auto-fill,minmax(140px,1fr));"></div>
        </div>
    </div>
</div>

<!-- SETTINGS MODAL -->
<div class="modalOverlay" id="settingsModalOverlay">
    <div class="modalBox" style="width:550px;">
        <div class="modalHeader">
            <div class="modalTitle">⚙ Scientific Workspace Settings</div>
            <button class="modalClose" onclick="closeSettingsModal()">✕</button>
        </div>
        <div class="modalBody">
            <div style="display:flex;flex-direction:column;gap:14px;">
                <div>
                    <div style="font-weight:600;color:#7dd3fc;">3D Render Quality</div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Antialiasing & Pixel Ratio</div>
                    <select id="settingQuality" style="margin-top:6px;padding:6px;border-radius:6px;background:#061426;border:1px solid #38bdf8;color:#fff;" onchange="applyQuality(this.value)">
                        <option value="2">High (Antialiased 2x - Recommended)</option>
                        <option value="1">Medium (Balanced)</option>
                        <option value="0.75">Fast (Low Power)</option>
                    </select>
                </div>
                <div>
                    <div style="font-weight:600;color:#7dd3fc;">Distance Units</div>
                    <div style="font-size:11px;color:#94a3b8;margin-top:2px;">Angstroms (Å) or Nanometers (nm)</div>
                    <select style="margin-top:6px;padding:6px;border-radius:6px;background:#061426;border:1px solid #38bdf8;color:#fff;">
                        <option>Angstroms (Å)</option>
                        <option>Nanometers (nm)</option>
                    </select>
                </div>
                <div>
                    <div style="font-weight:600;color:#7dd3fc;">Continuous Orbit Rotation</div>
                    <label style="display:flex;align-items:center;gap:8px;margin-top:6px;cursor:pointer;">
                        <input type="checkbox" id="chkAutoRotate" checked onchange="autoRotate = this.checked;" />
                        <span>Enable slow cinematic molecular rotation</span>
                    </label>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- TOAST -->
<div class="toast" id="toast">
    <div class="toastTitle" id="toastTitle">Notification</div>
    <div id="toastText">Action completed</div>
</div>

<!-- ================= JAVASCRIPT ================= -->
<script>
/* ================= STREAMLIT INSTANT HANDSHAKE ================= */
const Streamlit = {
    setComponentReady: function() {
        try { window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:componentReady', apiVersion: 1}, '*'); } catch(e){}
    },
    setFrameHeight: function(height) {
        try {
            const h = height || document.body.scrollHeight || window.innerHeight || 1200;
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: h}, '*');
        } catch(e){}
    },
    setComponentValue: function(value) {
        try { window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: value}, '*'); } catch(e){}
    }
};

Streamlit.setComponentReady();
Streamlit.setFrameHeight(window.innerHeight || 1200);

document.addEventListener('DOMContentLoaded', function(){
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight || 1200);
});

window.addEventListener('load', function(){
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight || 1200);
});

/* ================= TOAST NOTIFICATION ================= */
function showToast(title, text){
    const toast = document.getElementById("toast");
    if(!toast) return;
    document.getElementById("toastTitle").textContent = title;
    document.getElementById("toastText").textContent = text;
    toast.classList.add("show");
    setTimeout(() => { toast.classList.remove("show"); }, 3000);
}

/* ================= CLOCK ================= */
function updateClock(){
    const now = new Date();
    const h = String(now.getHours()).padStart(2, "0");
    const m = String(now.getMinutes()).padStart(2, "0");
    const clockEl = document.getElementById("clock");
    if(clockEl) clockEl.textContent = `${h}:${m}`;
}
setInterval(updateClock, 1000);
updateClock();

/* ================= THREE.JS 3D SCENE ================= */
let scene, camera, renderer, controls;
let moleculeGroup, cartoonGroup, sphereGroup, sticksGroup, surfaceGroup, meshGroup, glucoseGroup, interactionGroup;
let currentRep = 'cartoon';
let autoRotate = true;
let surfaceVisible = false;
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

        const wrap = document.getElementById("threeCanvasWrap");
        const width = (wrap && wrap.clientWidth > 50) ? wrap.clientWidth : (canvas.clientWidth || 700);
        const height = (wrap && wrap.clientHeight > 50) ? wrap.clientHeight : (canvas.clientHeight || 450);

        camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 2000);
        camera.position.set(0, 8, 28);

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
            controls.maxDistance = 120;
        } else {
            setupSimpleControls(camera, renderer.domElement);
        }

        // Lighting
        const ambient = new THREE.AmbientLight(0xffffff, 1.4);
        scene.add(ambient);

        const key = new THREE.DirectionalLight(0xffffff, 2.0);
        key.position.set(15, 20, 15);
        scene.add(key);

        const fill = new THREE.DirectionalLight(0x7da4ff, 1.2);
        fill.position.set(-15, -10, -15);
        scene.add(fill);

        // Molecular Groups
        moleculeGroup = new THREE.Group();
        cartoonGroup = new THREE.Group();
        sphereGroup = new THREE.Group();
        sticksGroup = new THREE.Group();
        surfaceGroup = new THREE.Group();
        meshGroup = new THREE.Group();
        glucoseGroup = new THREE.Group();
        interactionGroup = new THREE.Group();

        moleculeGroup.add(cartoonGroup, sphereGroup, sticksGroup, surfaceGroup, meshGroup, glucoseGroup, interactionGroup);
        scene.add(moleculeGroup);

        // Initial Standalone Glucose + Interactions in Pocket
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

function animate(){
    requestAnimationFrame(animate);
    if(autoRotate && moleculeGroup) {
        moleculeGroup.rotation.y += 0.0018;
    }
    if(controls && controls.update) controls.update();
    if(renderer && scene && camera) renderer.render(scene, camera);
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
    [0,1], [1,2], [2,3], [3,4], [4,5], [5,0], // Ring
    [0,6], [1,7], [2,8], [3,9], [4,10], [10,11] // Hydroxyls
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

    const cMat = new THREE.MeshStandardMaterial({ color: 0x00f59b, roughness: 0.25, metalness: 0.2 });
    const oMat = new THREE.MeshStandardMaterial({ color: 0xff4d67, roughness: 0.2, metalness: 0.3 });
    const bondMat = new THREE.MeshStandardMaterial({ color: 0x8be9fd, roughness: 0.3, metalness: 0.4 });

    const sphereGeo = new THREE.SphereGeometry(0.35, 16, 16);

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

    BINDING_CONTACTS.forEach((c, idx) => {
        const start = new THREE.Vector3(0, 0, 0);
        const end = new THREE.Vector3(c.x, c.y, c.z);
        
        const lineGeo = new THREE.BufferGeometry().setFromPoints([start, end]);
        const lineMat = new THREE.LineDashedMaterial({ color: c.color, dashSize: 0.3, gapSize: 0.15 });
        const line = new THREE.Line(lineGeo, lineMat);
        line.computeLineDistances();
        interactionGroup.add(line);

        // Marker for residue
        const marker = new THREE.Mesh(new THREE.SphereGeometry(0.25, 12, 12), new THREE.MeshStandardMaterial({ color: c.color }));
        marker.position.copy(end);
        interactionGroup.add(marker);

        // Populate Binding Panel
        if(resListEl) {
            const div = document.createElement("div");
            div.className = "residue";
            div.onclick = () => focusResidue(c.x, c.y, c.z, c.name, c.dist, c.type);
            div.innerHTML = `<span class="resName">${c.name}</span><span class="resDist">${c.dist}</span>`;
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
    if(!scene || !cartoonGroup){
        window._pendingPDBData = pdbData;
        return;
    }

    // Clear previous
    [cartoonGroup, sphereGroup, sticksGroup, surfaceGroup, meshGroup].forEach(g => {
        if(g) while(g.children.length > 0) g.remove(g.children[0]);
    });

    // 1. CARTOON RAINBOW BACKBONE
    const caPoints = pdbData.ca_coords.map(c => new THREE.Vector3(c.x, c.y, c.z));
    if(caPoints.length >= 2){
        const curve = new THREE.CatmullRomCurve3(caPoints);
        const tubeGeo = new THREE.TubeGeometry(curve, caPoints.length * 6, 0.42, 10, false);
        
        const count = tubeGeo.attributes.position.count;
        const colors = new Float32Array(count * 3);
        const color = new THREE.Color();
        for(let i=0; i<count; i++){
            const t = i / count;
            color.setHSL(0.55 - t * 0.55, 0.95, 0.55); // Cyan -> Green -> Yellow -> Orange -> Magenta
            colors[i*3] = color.r; colors[i*3+1] = color.g; colors[i*3+2] = color.b;
        }
        tubeGeo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

        const tubeMat = new THREE.MeshStandardMaterial({ vertexColors: true, roughness: 0.25, metalness: 0.2 });
        cartoonGroup.add(new THREE.Mesh(tubeGeo, tubeMat));

        // CA spheres
        const caGeo = new THREE.SphereGeometry(0.5, 14, 14);
        caPoints.forEach((p, idx) => {
            const frac = idx / caPoints.length;
            const mat = new THREE.MeshStandardMaterial({ color: new THREE.Color().setHSL(0.55 - frac * 0.55, 0.95, 0.6), roughness: 0.25 });
            const s = new THREE.Mesh(caGeo, mat);
            s.position.copy(p);
            cartoonGroup.add(s);
        });
    }

    // 2. CPK SPHERES
    const atoms = pdbData.atoms || [];
    const sphereGeo = new THREE.SphereGeometry(0.45, 12, 12);
    const elemColors = { 'C': 0x00d9ff, 'N': 0x3b82f6, 'O': 0xef4444, 'S': 0xfacc15, 'H': 0xffffff };
    atoms.forEach(a => {
        const mat = new THREE.MeshStandardMaterial({ color: elemColors[a.elem] || 0x10b981, roughness: 0.3 });
        const m = new THREE.Mesh(sphereGeo, mat);
        m.position.set(a.x, a.y, a.z);
        sphereGroup.add(m);
    });

    // 3. STICKS
    const stickMat = new THREE.MeshStandardMaterial({ color: 0x93c5fd, roughness: 0.3 });
    for(let i=0; i<caPoints.length-1; i++){
        const p1 = caPoints[i], p2 = caPoints[i+1];
        if(p1.distanceTo(p2) < 4.2){
            const cyl = new THREE.Mesh(new THREE.CylinderGeometry(0.18, 0.18, p1.distanceTo(p2), 8), stickMat);
            cyl.position.copy(p1).add(p2).multiplyScalar(0.5);
            cyl.quaternion.setFromUnitVectors(new THREE.Vector3(0,1,0), p2.clone().sub(p1).normalize());
            sticksGroup.add(cyl);
        }
    }

    // 4. SURFACE ENVELOPE
    const box = new THREE.Box3().setFromPoints(caPoints);
    const size = new THREE.Vector3(); box.getSize(size);
    const center = new THREE.Vector3(); box.getCenter(center);
    const maxDim = Math.max(size.x, size.y, size.z) * 0.65;

    const surfGeo = new THREE.IcosahedronGeometry(Math.max(6, maxDim), 3);
    const surfMat = new THREE.MeshPhysicalMaterial({ color: 0x0ea5e9, transparent: true, opacity: 0.22, transmission: 0.6, side: THREE.DoubleSide });
    const sMesh = new THREE.Mesh(surfGeo, surfMat);
    sMesh.position.copy(center);
    surfaceGroup.add(sMesh);

    // 5. MESH WIREFRAME
    const wireMesh = new THREE.Mesh(surfGeo, new THREE.MeshBasicMaterial({ color: 0x38bdf8, wireframe: true }));
    wireMesh.position.copy(center);
    meshGroup.add(wireMesh);

    // Apply active representation
    setRepresentation(currentRep, document.getElementById('btnRep' + currentRep.charAt(0).toUpperCase() + currentRep.slice(1)));

    // Fit camera
    const fitDist = Math.max(26, maxDim * 2.2);
    camera.position.set(0, fitDist * 0.35, fitDist);
    if(controls){ controls.target.set(center.x, center.y, center.z); controls.update(); }

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

/* ================= 3D CONTROLS & CAMERA ================= */
function setRepresentation(style, elem){
    currentRep = style;
    document.querySelectorAll(".viewerBottom .styleBtn").forEach(b => b.classList.remove("active"));
    if(elem) elem.classList.add("active");

    if(cartoonGroup) cartoonGroup.visible = (style === 'cartoon');
    if(surfaceGroup) surfaceGroup.visible = (style === 'surface');
    if(sticksGroup) sticksGroup.visible = (style === 'sticks');
    if(sphereGroup) sphereGroup.visible = (style === 'sphere');
    if(meshGroup) meshGroup.visible = (style === 'mesh');

    showToast("3D Representation", `${style.toUpperCase()} active`);
}

function resetCamera(){
    camera.position.set(0, 8, 28);
    if(controls){ controls.target.set(0,0,0); controls.update(); }
    showToast("Camera", "Reset to default orientation");
}

function focusMolecule(){
    if(controls){ controls.target.set(0,0,0); controls.update(); }
    showToast("Focus", "Centered on molecular centroid");
}

function toggleSurface(){
    surfaceVisible = !surfaceVisible;
    if(surfaceGroup) surfaceGroup.visible = surfaceVisible;
    showToast("Molecular Surface", surfaceVisible ? "Surface envelope visible" : "Surface hidden");
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

/* ================= WORKSPACE TABS ================= */
function switchWorkspaceTab(tabName, elem){
    document.querySelectorAll(".viewer .tab").forEach(t => t.classList.remove("active"));
    if(elem) elem.classList.add("active");

    const wrap = document.getElementById("threeCanvasWrap");
    if(wrap) wrap.style.display = (tabName === 'viewer') ? 'block' : 'none';

    document.querySelectorAll(".workspacePanel").forEach(p => p.classList.remove("active"));
    if(tabName !== 'viewer'){
        const p = document.getElementById(tabName + "Panel");
        if(p) p.classList.add("active");
    }
    showToast("Workspace", `${tabName.toUpperCase()} tab active`);
    if(tabName === 'viewer') setTimeout(resizeThree, 50);
}

/* ================= TRAJECTORY PLAY/PAUSE ================= */
let trajTimer = null;
function toggleTrajectoryPlay(){
    const btn = document.getElementById("btnPlayTraj");
    const slider = document.getElementById("trajSlider");
    const label = document.getElementById("trajFrame");

    if(trajTimer){
        clearInterval(trajTimer);
        trajTimer = null;
        if(btn) btn.textContent = "▶ Play Trajectory";
        showToast("Trajectory", "Simulation playback paused");
    } else {
        if(btn) btn.textContent = "⏸ Pause Playback";
        showToast("Trajectory", "Playing production dynamics");
        trajTimer = setInterval(() => {
            let val = parseInt(slider.value) + 10;
            if(val > 1500) val = 0;
            slider.value = val;
            if(label) label.textContent = `Frame ${val}`;
            if(moleculeGroup) moleculeGroup.rotation.y += 0.04;
        }, 80);
    }
}
function scrubTrajectory(val){
    const label = document.getElementById("trajFrame");
    if(label) label.textContent = `Frame ${val}`;
    if(moleculeGroup) moleculeGroup.rotation.y = (val / 1500) * Math.PI * 4;
}

/* ================= LOG TABS & FILTERING ================= */
let currentLogTab = 'all';
function switchLogTab(tab, elem){
    currentLogTab = tab;
    document.querySelectorAll(".logsHeader .logTab").forEach(t => t.classList.remove("active"));
    if(elem) elem.classList.add("active");
    filterLogs();
}

function clearLogs(){
    const body = document.getElementById("logBody");
    if(body) body.innerHTML = `<div class="logLine" style="color:#64748b;">[Logs cleared by researcher]</div>`;
    showToast("Terminal", "Logs cleared");
}

function filterLogs(){
    const q = (document.getElementById("logSearch")?.value || "").toLowerCase();
    document.querySelectorAll("#logBody .logLine").forEach(line => {
        const text = line.textContent.toLowerCase();
        let matchTab = true;
        if(currentLogTab === 'analysis') matchTab = text.includes('success') || text.includes('ai') || text.includes('plan');
        if(currentLogTab === 'system') matchTab = text.includes('info') || text.includes('connector') || text.includes('cluster');
        if(currentLogTab === 'plots') matchTab = text.includes('plot') || text.includes('graph') || text.includes('pca');

        const matchQ = !q || text.includes(q);
        line.style.display = (matchTab && matchQ) ? "" : "none";
    });
}

/* ================= SIDEBAR NAV ROUTING ================= */
function navSelect(name, elem){
    document.querySelectorAll(".sidebar .navItem").forEach(n => n.classList.remove("active"));
    if(elem) elem.classList.add("active");

    if(name === 'Home') switchWorkspaceTab('viewer', document.querySelectorAll('.viewer .tab')[0]);
    else if(name === 'AI Chat') {
        const inp = document.getElementById('aiInput');
        if(inp){ inp.focus(); showToast("AI Chat", "Type scientific query and press Enter"); }
    }
    else if(name === 'Research Sessions') openSessionModal();
    else if(name === 'Protocols') runAI('Run Crop Proteome & Thermal Adaptation protocol');
    else if(name === 'Simulations') switchWorkspaceTab('trajectory', document.querySelectorAll('.viewer .tab')[2]);
    else if(name === 'Data Analysis') switchWorkspaceTab('analysis', document.querySelectorAll('.viewer .tab')[5]);
    else if(name === 'Visualization') switchWorkspaceTab('viewer', document.querySelectorAll('.viewer .tab')[0]);
    else if(name === '3D Library' || name === 'Files & Data') openResultsModal();
    else if(name === 'Settings') openSettingsModal();
    else showToast("Polymathix OS", `${name} selected`);
}

/* ================= MODAL CONTROLS ================= */
function openSessionModal(){
    const o = document.getElementById("sessionModalOverlay");
    if(o) o.classList.add("show");
}
function closeSessionModal(){
    const o = document.getElementById("sessionModalOverlay");
    if(o) o.classList.remove("show");
}
function openExport(){
    const o = document.getElementById("exportOverlay");
    if(o) o.classList.add("show");
}
function closeExport(){
    const o = document.getElementById("exportOverlay");
    if(o) o.classList.remove("show");
}
function openResultsModal(){
    const o = document.getElementById("resultsModalOverlay");
    if(o) o.classList.add("show");
}
function closeResultsModal(){
    const o = document.getElementById("resultsModalOverlay");
    if(o) o.classList.remove("show");
}
function openSettingsModal(){
    const o = document.getElementById("settingsModalOverlay");
    if(o) o.classList.add("show");
}
function closeSettingsModal(){
    const o = document.getElementById("settingsModalOverlay");
    if(o) o.classList.remove("show");
}
function openConnectorsModal(){
    showToast("Tool Connectors", "Click any connector card to toggle status");
}

let exportFormat = 'glb';
function setExportFormat(fmt, elem){
    exportFormat = fmt;
    document.querySelectorAll("#exportOverlay .styleBtn").forEach(b => b.classList.remove("active"));
    if(elem) elem.classList.add("active");
    const btn = document.getElementById("btnDoExport");
    if(btn) btn.textContent = `Download ${fmt.toUpperCase()}`;
}
function performExport(){
    showToast("Exporting Model", `Preparing ${exportFormat.toUpperCase()} package...`);
    closeExport();
    // Download link
    const link = document.createElement("a");
    link.download = `polymathix-model.${exportFormat}`;
    link.href = (exportFormat === 'png') ? '#' : 'assets/polymathix_3d_render.obj';
    link.click();
}

function toggleAudio(){ showToast("Audio System", "Scientific sound effects enabled"); }
function toggleTheme(){ showToast("Display FX", "Visual neon glow intensity adjusted"); }

// ESC Key closes everything
document.addEventListener('keydown', function(e){
    if(e.key === 'Escape'){
        const v = document.querySelector(".viewer");
        if(v && v.classList.contains("fullscreenMode")) {
            v.classList.remove("fullscreenMode");
            resizeThree();
        }
        closeSessionModal(); closeExport(); closeResultsModal(); closeSettingsModal();
    }
});

/* ================= SIMPLE MOUSE ORBIT CONTROLS FALLBACK ================= */
function setupSimpleControls(cam, domElem){
    let isDragging = false, prevMouse = { x: 0, y: 0 };
    domElem.addEventListener('mousedown', (e) => { isDragging = true; prevMouse = { x: e.clientX, y: e.clientY }; });
    window.addEventListener('mouseup', () => { isDragging = false; });
    window.addEventListener('mousemove', (e) => {
        if(!isDragging || !moleculeGroup) return;
        moleculeGroup.rotation.y += (e.clientX - prevMouse.x) * 0.008;
        moleculeGroup.rotation.x += (e.clientY - prevMouse.y) * 0.008;
        prevMouse = { x: e.clientX, y: e.clientY };
    });
    domElem.addEventListener('wheel', (e) => {
        if(!cam) return;
        cam.position.z += e.deltaY * 0.02;
        cam.position.z = Math.max(5, Math.min(120, cam.position.z));
    }, { passive: true });
}

/* ================= STREAMLIT TRIGGER FUNCTIONS ================= */
function runAI(customQuery){
    const inp = document.getElementById('aiInput');
    const q = customQuery || (inp ? inp.value : '') || 'Show glucose binding pocket';
    showToast("AI Orchestrator", `Executing: "${q}"`);
    Streamlit.setComponentValue({ action: 'runAI', query: q, timestamp: Date.now() });
    if(inp && !customQuery) inp.value = '';
}

function triggerQuickAction(type){
    showToast("Quick Action", `Invoking ${type}...`);
    Streamlit.setComponentValue({ action: 'quick_action', type: type, timestamp: Date.now() });
}

function triggerAgentControl(cmd){
    showToast("Agent Command", cmd.toUpperCase());
    Streamlit.setComponentValue({ action: 'agent_control', cmd: cmd, timestamp: Date.now() });
}

function toggleConnector(name){
    showToast("Connector", `Toggling ${name}...`);
    Streamlit.setComponentValue({ action: 'toggle_connector', name: name, timestamp: Date.now() });
}

/* ================= STATE UPDATE FROM PYTHON ================= */
function updateStateFromPython(state){
    if(!state) return;

    if(state.session_name) {
        const el = document.getElementById("sessionNameDisplay"); if(el) el.textContent = state.session_name;
        const mel = document.getElementById("modalSessionTitle"); if(mel) mel.textContent = `Research Session: ${state.session_name}`;
    }
    if(state.protocol_name) {
        const el = document.getElementById("protocolNameDisplay"); if(el) el.textContent = state.protocol_name;
        const mel = document.getElementById("modalProtocolName"); if(mel) mel.textContent = state.protocol_name;
    }
    if(state.status) {
        const st = document.getElementById("sessionStatusDisplay");
        if(st) {
            const isAct = state.status === 'Active';
            st.innerHTML = `<span class="statusDot" style="background:${isAct ? '#00f59b' : '#facc15'}"></span>${state.status}`;
        }
    }

    // Workflow Steps
    if(state.workflow_steps && Array.isArray(state.workflow_steps)){
        const c = document.getElementById("workflowStepsContainer");
        const mc = document.getElementById("modalWorkflowSteps");
        let html = "";
        state.workflow_steps.forEach((s, idx) => {
            const num = idx + 1;
            let cls = "step";
            let icon = "";
            if(s.status === 'done'){ cls = "step done"; icon = `<span style="margin-left:auto;color:#00f59b">✓</span>`; }
            else if(s.status === 'running'){ cls = "step running"; icon = `<span style="margin-left:auto;color:#38bdf8">●</span>`; }
            html += `<div class="${cls}"><div class="stepNum">${num}</div><span>${s.name}</span>${icon}</div>`;
        });
        if(c) c.innerHTML = html;
        if(mc) mc.innerHTML = html;
    }

    // Progress
    if(typeof state.progress_percent === 'number'){
        const pf = document.getElementById("progressFill"); if(pf) pf.style.width = state.progress_percent + "%";
        const pv = document.getElementById("progressValue"); if(pv) pv.textContent = state.progress_percent + "%";
    }
    if(state.time_remaining){
        const tr = document.getElementById("timeRemainingDisplay"); if(tr) tr.textContent = `Estimated time: ${state.time_remaining}`;
        const mtr = document.getElementById("modalTimeRemaining"); if(mtr) mtr.textContent = `Estimated time: ${state.time_remaining}`;
    }

    // Tool Connectors
    if(state.connectors && Array.isArray(state.connectors)){
        const cl = document.getElementById("connectorsList");
        if(cl){
            cl.innerHTML = "";
            state.connectors.forEach(c => {
                const div = document.createElement("div");
                div.className = "connector";
                div.onclick = () => toggleConnector(c.name);
                div.innerHTML = `
                    <div class="connIcon">${c.icon}</div>
                    <div class="connName">${c.name}</div>
                    <div class="connStatus ${c.status}">${c.text}</div>
                `;
                cl.appendChild(div);
            });
        }
    }

    // Terminal Logs
    if(state.logs && Array.isArray(state.logs)){
        const lb = document.getElementById("logBody");
        if(lb){
            lb.innerHTML = "";
            state.logs.forEach(l => {
                let cls = "logInfo";
                if(l.type === "SUCCESS") cls = "logSuccess";
                else if(l.type === "WARN") cls = "logWarn";
                else if(l.type === "ERROR") cls = "logError";
                else if(l.type === "AI") cls = "logAI";

                const d = document.createElement("div");
                d.className = "logLine";
                d.innerHTML = `<span class="logTime">[${l.time}]</span><span class="${cls}">${l.type}</span> ${l.msg}`;
                lb.appendChild(d);
            });
            lb.scrollTop = lb.scrollHeight;
        }
    }

    // Results Grid
    if(state.results && Array.isArray(state.results)){
        const rg = document.getElementById("resultGrid");
        const mrg = document.getElementById("modalResultGrid");
        let html = "";
        state.results.forEach(r => {
            html += `
                <div class="resultCard" onclick="showToast('Result Artifact', 'Opening ${r.name}')">
                    <div class="resultPreview">${r.icon || '🧬'}</div>
                    <div class="resultName">${r.name}</div>
                    <div class="resultMeta">${r.meta || 'Recent'}</div>
                </div>
            `;
        });
        if(rg) rg.innerHTML = html;
        if(mrg) mrg.innerHTML = html;
    }

    // Render PDB
    if(state.pdb_data){
        renderRealPDB(state.pdb_data);
    }
}

/* ================= STREAMLIT LISTENER ================= */
window.addEventListener('message', function(event) {
    if(event.data.type === 'streamlit:render'){
        const args = event.data.args;
        const state = (args && args.initial_data) ? args.initial_data : args;
        if(state) updateStateFromPython(state);
    }
});

/* ================= INITIALIZE ON LOAD ================= */
try {
    initThree();
} catch(e) {
    console.error("Error in initThree:", e);
}

/* __INJECT_INITIAL_STATE__ */

</script>
</body>
</html>
"""

import json
from polymathix.orchestrator import PolymathixOrchestrator
orc = PolymathixOrchestrator()
state_json = json.dumps(orc.get_state())

injection = f"""try {{
    const INITIAL_EMBEDDED_STATE = {state_json};
    if(typeof updateStateFromPython === 'function') {{
        updateStateFromPython(INITIAL_EMBEDDED_STATE);
    }}
}} catch(e) {{
    console.error("Error applying embedded state:", e);
}}"""

html_code = html_code.replace("/* __INJECT_INITIAL_STATE__ */", injection)

target = os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html")
with open(target, "w", encoding="utf-8") as f:
    f.write(html_code)

print(f"Successfully generated clean, consolidated index.html ({len(html_code)} bytes)!")

import os

html_path = r"C:\Users\sohel\Downloads\GitHub T1\Polymathix\polymathix_ui\frontend\index.html"

with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

# 1. Prepare immediate Streamlit handshake code
top_bridge_js = """<script>
/* ================= STREAMLIT INSTANT HANDSHAKE ================= */
const Streamlit = {
    setComponentReady: function() {
        try {
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:componentReady', apiVersion: 1}, '*');
        } catch(e) { console.warn('Streamlit handshake error:', e); }
    },
    setFrameHeight: function(height) {
        try {
            const h = height || document.body.scrollHeight || window.innerHeight || 1200;
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setFrameHeight', height: h}, '*');
        } catch(e) {}
    },
    setComponentValue: function(value) {
        try {
            window.parent.postMessage({isStreamlitMessage: true, type: 'streamlit:setComponentValue', value: value}, '*');
        } catch(e) {}
    }
};

// Handshake immediately to prevent Streamlit component loading timeout!
Streamlit.setComponentReady();
Streamlit.setFrameHeight(window.innerHeight || 1200);

document.addEventListener('DOMContentLoaded', function() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight || 1200);
});

window.addEventListener('load', function() {
    Streamlit.setComponentReady();
    Streamlit.setFrameHeight(window.innerHeight || 1200);
});
"""

# Replace `<script>` with the immediate handshake at the very top
html = html.replace("<script>", top_bridge_js, 1)

# 2. Make initThree resilient to async Three.js loading
old_init_call = "initThree();"
new_init_call = """
function safeInitThree() {
    if (typeof THREE === 'undefined') {
        setTimeout(safeInitThree, 150);
        return;
    }
    try {
        initThree();
    } catch(err) {
        console.warn("Three.js init error:", err);
    }
}
safeInitThree();
"""

html = html.replace(old_init_call, new_init_call, 1)

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Streamlit handshake fixed at top of script!")

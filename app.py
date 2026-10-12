import streamlit as st
import os
import sys

# Ensure root directory is in sys.path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from polymathix.orchestrator import PolymathixOrchestrator
from polymathix_ui import render_polymathix_ui

st.set_page_config(
    page_title="POLYMATHIX OS — Scientific Discovery Intelligence",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Fully hide Streamlit default chrome to give 100% immersive scientific workspace
st.markdown("""
<style>
    header {visibility: hidden; display: none !important;}
    footer {visibility: hidden; display: none !important;}
    [data-testid="stSidebar"] {display: none !important;}
    .block-container {padding: 0 !important; max-width: 100% !important; margin: 0 !important;}
    .stApp {background-color: #020914;}
    iframe {border: none; width: 100vw; height: 100vh; overflow: hidden; background-color: #020914;}
</style>
""", unsafe_allow_html=True)

# Initialize the Polymathix AI Orchestrator singleton
if "orchestrator" not in st.session_state:
    st.session_state.orchestrator = PolymathixOrchestrator()

orchestrator = st.session_state.orchestrator

# Keep track of last processed action timestamp to prevent duplicate reruns
if "last_action_ts" not in st.session_state:
    st.session_state.last_action_ts = 0

# Get current state from orchestrator
current_state = orchestrator.get_state()

# Render the bi-directional Polymathix UI component
action_data = render_polymathix_ui(
    initial_data=current_state,
    key="polymathix_dashboard"
)

# Process bi-directional actions from frontend
if action_data and isinstance(action_data, dict):
    action_ts = action_data.get("timestamp", 0)
    action = action_data.get("action")
    
    # Process only new actions
    if action_ts > st.session_state.last_action_ts:
        st.session_state.last_action_ts = action_ts
        
        if action == "runAI":
            query = action_data.get("query", "")
            orchestrator.run_ai_task(query)
            st.rerun()
            
        elif action == "quick_action":
            action_type = action_data.get("type", "")
            orchestrator.handle_quick_action(action_type)
            st.rerun()
            
        elif action == "agent_control":
            cmd = action_data.get("cmd", "")
            orchestrator.handle_agent_control(cmd)
            st.rerun()
            
        elif action == "toggle_connector":
            name = action_data.get("name", "")
            orchestrator.toggle_connector(name)
            st.rerun()

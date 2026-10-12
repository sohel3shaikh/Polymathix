import os
import streamlit.components.v1 as components

# Create the absolute path to the directory containing this script
_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "polymathix_ui",
        url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend")
    _component_func = components.declare_component("polymathix_ui", path=build_dir)

def render_polymathix_ui(initial_data=None, key=None):
    component_value = _component_func(initial_data=initial_data, key=key, default=None)
    return component_value

with open(os.path.join(ROOT_DIR, "polymathix_ui", "frontend", "index.html"), "r", encoding="utf-8") as f:
    html = f.read()

ids_to_check = [
    "aiInput", "sessionNameDisplay", "protocolNameDisplay", "sessionStatusDisplay",
    "timeRemainingDisplay", "resultGrid", "logBody", "progressFill", "progressValue",
    "threeCanvasWrap", "sequencePanel", "trajectoryPanel", "surfacesPanel", "propertiesPanel", "analysisPanel"
]

missing = [i for i in ids_to_check if f'id="{i}"' not in html and f"id='{i}'" not in html]
print("Missing IDs:", missing)
print("Total HTML length:", len(html))
print("Script tag count (<script / </script>):", html.count("<script"), html.count("</script>"))

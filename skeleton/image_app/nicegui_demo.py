from nicegui import ui
from pathlib import Path

# ui.add_head_html("<style>" + open(Path(__file__).parent / "styles.css").read() + "</style>")

with ui.column().classes("w-full items-center"):
    with ui.row():
        ui.markdown("## something here").style("color: red;")
    ui.radio(["A", "B", "Chicken Nugg"], value="A")
    ui.markdown("# Header 1?")
    
ui.run()
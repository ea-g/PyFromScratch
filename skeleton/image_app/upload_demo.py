from nicegui import events, ui
from starlette.formparsers import MultiPartParser
from pathlib import Path

# change css style
ui.add_head_html(
    "<style>" + open(Path(__file__).parent / "styles.css").read() + "</style>"
)

# allow files up to 5 mb to sit in RAM, smoothing larger file upload
MultiPartParser.max_file_size = 1024 * 1024 * 5

# display uploaded markdown files in a popup
with ui.dialog().props('full-width') as dialog:
    with ui.card():
        content = ui.markdown()

# what to do when receiving an upload
def handle_upload(e: events.UploadEventArguments):
    if e.name.endswith(".md"):
        ui.notify("it's a markdown file!")
    text = e.content.read().decode('utf-8')
    content.set_content(text)
    dialog.open()

# instance of the upload class
ui.upload(on_upload=handle_upload, on_rejected=lambda: ui.notify("Rejected!"), max_file_size=10).props('accept=.md,.jpg').classes('max-w-full')

ui.run()

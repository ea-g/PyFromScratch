from nicegui import events, ui
from pathlib import Path

# change css style
ui.add_head_html(
    "<style>" + open(Path(__file__).parent / "styles.css").read() + "</style>"
)

# address of an image
src = "https://picsum.photos/id/565/640/360"


# mouse event handler--note that it's used for our interactive image
def mouse_handler(e: events.MouseEventArguments):
    color = "SkyBlue" if e.type == "mousedown" else "SteelBlue"
    ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
    ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")

down_coord = tuple()
def calc_rectangle(point_a: tuple[float, float], point_b: tuple[float, float]) -> str:
    """Calculates the width, height, x, y from 2 points for a rectangle. x, y is the top left corner of the rectangle.

    Args:
        point_a (tuple[float, float]): one of two corners in the rectangle
        point_b (tuple[float, float]): one of two corners in the rectangle

    Returns:
        str: html string for a rectangle
    """
    pass

def draw_rect(e: events.MouseEventArguments):
    global down_coord
    if e.type == 'mousedown':
        down_coord = (e.image_x, e.image_y)
    else: 
        ii.content += calc_rectangle(down_coord, (e.image_x, e.image_y))
    ui.notify(f'{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})')

with ui.column().classes("w-full items-center"):
    ui.markdown("# Try clicking on this image:")
    ii = ui.interactive_image(
        src, on_mouse=mouse_handler, events=["mousedown", "mouseup"], cross=True
    )

ui.run()

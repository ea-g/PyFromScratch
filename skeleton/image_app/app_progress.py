from nicegui import events, ui
from pathlib import Path
import random

# change css style
ui.add_head_html(
    "<style>" + open(Path(__file__).parent / "styles.css").read() + "</style>"
)

# address of an image
src = "https://picsum.photos/id/565/640/360"


# mouse event handler--note that it's used for our interactive image
def mouse_handler(e: events.MouseEventArguments):
    # color = "SkyBlue" if e.type == "mousedown" else "SteelBlue"
    color = tuple([random.randint(0, 255) for i in range(3)]) # make a random RGB color
    # ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
    ii.content += f'<rect width="300" height="100" x="{e.image_x}" y="{e.image_y}" fill="none" stroke="rgb{color}" stroke-wdith="2" />'
    ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")


def calc_rectangle(point_a: tuple[float, float], point_b: tuple[float, float]) -> str:
    """Calculates the width, height, x, y from 2 points for a rectangle. x, y is the top left corner of the rectangle.

    Args:
        point_a (tuple[float, float]): one of two corners in the rectangle
        point_b (tuple[float, float]): one of two corners in the rectangle

    Returns:
        str: html string for a rectangle
    """
    color = tuple([random.randint(0, 255) for i in range(3)]) # make a random RGB color
    corner = (min([point_a[0], point_b[0]]), min([point_a[1], point_b[1]]))
    h = max([point_a[1], point_b[1]]) - min([point_a[1], point_b[1]])
    w = max([point_a[0], point_b[0]]) - min([point_a[0], point_b[0]])
    return f'<rect width="{w}" height="{h}" x="{corner[0]}" y="{corner[1]}" fill="none" stroke="rgb{color}" stroke-width="4" />'


def draw_rect(e: events.MouseEventArguments):
    global down_coord
    global content_len
    if e.type == "mousedown":
        down_coord = (e.image_x, e.image_y)
        content_len = len(ii.content)
    elif "content_len" not in globals():
        pass
    elif e.type == "mousemove":
        ii.content = ii.content[:content_len]
        ii.content += calc_rectangle(down_coord, (e.image_x, e.image_y))
    else: # this is mousedown!
        ii.content = ii.content[:content_len]
        ii.content += calc_rectangle(down_coord, (e.image_x, e.image_y))
        del down_coord
        del content_len
    # ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")


with ui.column().classes("w-full items-center"):
    ui.markdown("# Try clicking on this image:")
    ii = ui.interactive_image(
        src, on_mouse=draw_rect, events=["mousedown", "mouseup", "mousemove"], cross=True
    )

ui.run()

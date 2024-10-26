from nicegui import events, ui
from pathlib import Path
from starlette.formparsers import MultiPartParser
import random
import base64
from PIL import Image
import numpy as np
import skimage as ski
import io
from typing import Literal
from functools import partial

MultiPartParser.max_file_size = 1024 * 1024 * 5
# change css style
ui.add_head_html(
    "<style>" + open(Path(__file__).parent / "styles.css").read() + "</style>"
)

# # add a bit of code to get the size of the screen
# ui.add_head_html("""
#     <script>
#     function emitSize() {
#         emitEvent('resize', {
#             width: document.body.offsetWidth,
#             height: document.body.offsetHeight,
#         });
#     }
#     window.onload = emitSize;
#     window.onresize = emitSize;
#     </script>
# """)


# def store_size(e):
#     global screen_size
#     screen_size = e.args
#     ui.notify(f"{screen_size}")


# # whenever app is connected or size is changed, get the new size
# ui.on("resize", store_size)


def handle_upload(e: events.UploadEventArguments) -> None:
    # we need to reset all our variables on an upload event
    for i in [
        "rects",
        "og_image",
        "og_image_bytes",
        "image_type",
        "rects",
        "down_coord",
        "content_len",
        "cur_image",
    ]:
        if i in globals():
            globals().pop(i)
        ii.content = ""
    global og_image
    global og_image_bytes
    global image_type
    global rects
    rects = list()
    # compressed form!
    og_image_bytes = base64.b64encode(e.content.read())
    # uncompressed raw image
    og_image = Image.open(e.content)
    # TODO: handle large images
    # compressed type
    image_type = e.type
    ii.set_source(
        f"data:{e.type};base64,{og_image_bytes.decode()}"
    )  # display using b64 bytes


# mouse event handler--note that it's used for our interactive image
def mouse_handler(e: events.MouseEventArguments):
    # color = "SkyBlue" if e.type == "mousedown" else "SteelBlue"
    color = tuple([random.randint(0, 255) for i in range(3)])  # make a random RGB color
    # ii.content += f'<circle cx="{e.image_x}" cy="{e.image_y}" r="15" fill="none" stroke="{color}" stroke-width="4" />'
    ii.content += f'<rect width="300" height="100" x="{e.image_x}" y="{e.image_y}" fill="none" stroke="rgb{color}" stroke-wdith="2" />'
    ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")


def calc_rectangle(point_a: tuple[float, float], point_b: tuple[float, float]) -> tuple:
    """Calculates the width, height, x, y from 2 points for a rectangle. x, y is the top left corner of the rectangle.

    Args:
        point_a (tuple[float, float]): one of two corners in the rectangle
        point_b (tuple[float, float]): one of two corners in the rectangle

    Returns:
        str: html string for a rectangle
    """
    color = tuple([random.randint(0, 255) for i in range(3)])  # make a random RGB color
    corner = (min([point_a[0], point_b[0]]), min([point_a[1], point_b[1]]))
    h = max([point_a[1], point_b[1]]) - min([point_a[1], point_b[1]])
    w = max([point_a[0], point_b[0]]) - min([point_a[0], point_b[0]])
    return (
        f'<rect width="{w}" height="{h}" x="{corner[0]}" y="{corner[1]}" fill="none" stroke="rgb{color}" stroke-width="4" />',
        dict(tc=corner, hw=(h, w)),
    )


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
        res = calc_rectangle(down_coord, (e.image_x, e.image_y))
        ii.content += res[0]
    else:  # this is mousedown!
        ii.content = ii.content[:content_len]
        res = calc_rectangle(down_coord, (e.image_x, e.image_y))
        rects.append(res[1])
        ii.content += res[0]
        del down_coord
        del content_len
    # ui.notify(f"{e.type} at ({e.image_x:.1f}, {e.image_y:.1f})")


def clear_image():
    # reset the image content to original
    # clear out the rectangle list
    global rects
    rects = list()
    ii.content = ii.content[:1]


def revert_image():
    global cur_image
    ii.set_source(f"data:{image_type};base64,{og_image_bytes.decode()}")
    if "cur_image" in globals():
        globals().pop("cur_image")


def draw_circle(e: events.MouseEventArguments):
    global down_coord
    if e.type == "mousedown":
        down_coord = (e.image_x, e.image_y)
        ii.content += f'<circle cx="{down_coord[0]}" cy="{down_coord[1]}" r="{circle_size}" fill="none" stroke-width="4" stroke="black" />'


def switch_circle():
    ii.on_mouse(draw_circle)
    if len(ii._event_listeners) > 1:
        key_1 = list(ii._event_listeners.keys())[0]
        del ii._event_listeners[key_1]


def switch_rect():
    ii.on_mouse(draw_rect)
    if len(ii._event_listeners) > 1:
        key_1 = list(ii._event_listeners.keys())[0]
        del ii._event_listeners[key_1]


def switch_oranges():
    ii.on_mouse(add_oranges)
    if len(ii._event_listeners) > 1:
        key_1 = list(ii._event_listeners.keys())[0]
        del ii._event_listeners[key_1]


def add_oranges(e: events.MouseEventArguments):
    global down_coord
    if e.type == "mousedown":
        h = 203
        w = 200
        down_coord = (e.image_x, e.image_y)
        ii.content += f'<image href="https://i.postimg.cc/PqzhYSB3/orange.webp" x="{down_coord[0]-round(w*0.5)}" y="{down_coord[1]-round(h*0.5)}" height="{h}" width="{w}" />'


global circle_size
circle_size = 50


def circle_smaller():
    global circle_size
    circle_size -= 2
    # ui.notify(f"circle size is now {circle_size}")
    zz.set_text(f"{circle_size}")


def circle_larger():
    global circle_size
    circle_size += 2
    # ui.notify(f"circle size is now {circle_size}")
    zz.set_text(f"{circle_size}")


def change_image():
    global cur_image
    if "cur_image" not in globals():
        new_img = np.array(og_image)
    else:
        new_img = cur_image
    for r in rects:
        y = int(np.floor(r["tc"][1]))
        x = int(np.floor(r["tc"][0]))
        h = int(np.floor(r["hw"][0]))
        w = int(np.floor(r["hw"][1]))
        # TODO: make option to switch between filters here
        # perform a transformation on a rectangle
        blur_rect = np.floor(
            ski.filters.gaussian(new_img[y : y + h, x : x + w, :], 10, channel_axis=2)
            * 255
        ).astype(np.uint8)  # blur, scale, round, convert
        # change the pixels to the transformed version
        new_img[y : y + h, x : x + w, :] = blur_rect
    # get rid of tracking of the rectangles we just transformed
    rects.clear()
    # track the current image
    cur_image = new_img
    # set the transformed image to the source for the front end gui using compressed form
    new_img_byte = io.BytesIO()
    Image.fromarray(new_img).save(new_img_byte, format="JPEG")
    new_img_byte = base64.b64encode(new_img_byte.getvalue())
    ii.set_source(f"data:image/jpeg;base64,{new_img_byte.decode()}")


with ui.column().classes("w-full items-center"):
    ui.upload(on_upload=handle_upload).props("accept=.jpg,.jpeg,.png,.webp").classes(
        "max-w-full"
    )
    ui.markdown("# Try clicking on this image:")
    with ui.row():
        ui.button("Draw Rectangle", on_click=switch_rect)
        ui.button("Draw Circle", on_click=switch_circle)
        ui.button("-", on_click=circle_smaller)
        zz = ui.label(f"{circle_size}")
        ui.button("+", on_click=circle_larger)
        ui.button("Add Oranges", on_click=switch_oranges)
        ui.button("Clear", on_click=clear_image)
        ui.button("Revert Image", on_click=revert_image)
        ui.button("Test", on_click=change_image)
        # TODO: implement menu item for applying filters, use button and menu, hint: use functools partial
    ii = ui.interactive_image(
        on_mouse=draw_rect, events=["mousedown", "mouseup", "mousemove"], cross=True
    )


ui.run()

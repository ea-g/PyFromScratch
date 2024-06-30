from nicegui import ui
from nicegui.events import KeyEventArguments
import asyncio
import time


def handle_key(e: KeyEventArguments):
    if e.key == "f" and not e.action.repeat:
        if e.action.keyup:
            ui.notify("f was just released")
        elif e.action.keydown:
            ui.notify("f was just pressed")
    if e.modifiers.shift and e.action.keydown:
        if e.key.arrow_left:
            ui.notify("going left")
        elif e.key.arrow_right:
            ui.notify("going right")
        elif e.key.arrow_up:
            ui.notify("going up")
        elif e.key.arrow_down:
            ui.notify("going down")


# keyboard element
keyboard = ui.keyboard(on_key=handle_key)


# async event handling
async def async_task():
    ui.notify("Asynchronous task started")
    await asyncio.sleep(5)
    ui.notify("Asynchronous task finished")


# synchronous event handing
def sync_task():
    ui.notify("SYNCHRONOUS task started")
    time.sleep(5)
    ui.notify("SYNCHRONOUS task finished")


with ui.column().classes("w-full items-center"):
    # keyboard stuff
    ui.markdown("### Key events can be caught globally by using the keyboard element.")
    ui.checkbox("Track key events").bind_value_to(keyboard, "active")

    # buttons/ mouse stuff
    with ui.row():
        ui.button("A", on_click=lambda: ui.notify("You clicked the button A."))
        ui.button("B").on("click", lambda: ui.notify("You clicked the button B."))
    with ui.row():
        ui.button("C").on("mousemove", lambda: ui.notify("You moved on button C."))
        ui.button("D").on(
            "mousemove", lambda: ui.notify("You moved on button D."), throttle=0.5
        )
    with ui.row():
        ui.button("E").on("mousedown", lambda e: ui.notify(e))
        ui.button("F").on("mousedown", lambda e: ui.notify(e), ["ctrlKey", "shiftKey"])

    # sync vs. async
    ui.button("start async task", on_click=async_task)
    ui.button("start sync task", on_click=sync_task)
    
ui.run()

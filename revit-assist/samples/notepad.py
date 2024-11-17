import flet as ft
from pywinauto import Application
import time

def main(page: ft.Page):
    def on_button_click(e):
        # Launch Notepad using pywinauto
        app = Application().start("notepad.exe")

        # Wait for Notepad to open
        time.sleep(1)  # Giving it a moment to open

        # Connect to the Notepad window
        notepad_window = app.window(title="Untitled - Notepad")
        notepad_window.set_focus()

        # Type 'Hello World' in Notepad
        notepad_window.type_keys("Hello{SPACE}World")

    # Create a button that triggers the Notepad opening and typing
    button = ft.ElevatedButton("Launch Notepad and Type Hello World", on_click=on_button_click)

    # Add the button to the page
    page.add(button)

# Run the app
ft.app(target=main)

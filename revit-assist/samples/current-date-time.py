import flet as ft
from datetime import datetime

def main(page: ft.Page):
    page.title = "Timestamp Logger"
    page.padding = 0
    page.window_width = 800
    page.window_height = 600
    
    # Create a multiline textbox
    txt_log = ft.TextField(
        multiline=True,
        min_lines=100,
        border_color=ft.colors.GREY_400,
        expand=True,
        text_size=12
    )
    
    def add_timestamp(e):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txt_log.value = (txt_log.value or "") + current_time + "\n"
        page.update()
    
    # Create button
    btn_log = ft.ElevatedButton(
        text="Log Timestamp",
        on_click=add_timestamp,
        width=200
    )
    
    # Create layout
    main_row = ft.Row(
        controls=[
            # Left column with button
            ft.Container(
                content=ft.Column(
                    controls=[btn_log],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                padding=10,
                expand=1
            ),
            # Vertical divider
            ft.VerticalDivider(),
            # Right column with textbox
            ft.Container(
                content=txt_log,
                expand=2,
                padding=10,
                bgcolor=ft.colors.GREY_50,
            )
        ],
        spacing=0,
        expand=True
    )
    
    # Wrap the row in a container that takes full height
    page.add(
        ft.Container(
            content=main_row,
            expand=True
        )
    )
    
    # Update dimensions when window resizes
    def page_resize(e):
        txt_log.height = page.window_height - 40  # Subtract padding
        page.update()
    
    page.on_resize = page_resize
    # Initial size setup
    txt_log.height = page.window_height - 40

ft.app(target=main)
import flet as ft
from datetime import datetime
import pytesseract
from PIL import Image, ImageDraw
import os
import io
import base64

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'

def main(page: ft.Page):
    page.title = "Image Text Extractor"
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    
    # Create a multiline textbox
    txt_log = ft.TextField(
        multiline=True,
        min_lines=100,
        border_color=ft.colors.GREY_400,
        expand=True,
        text_size=12
    )
    
    # Create an image display
    img_display = ft.Image(
        width=600,
        height=300,
        fit=ft.ImageFit.CONTAIN,
    )
    
    def add_timestamp(e):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        txt_log.value = (txt_log.value or "") + current_time + "\n"
        page.update()
    
    # File picker for image selection
    file_picker = ft.FilePicker(
        on_result=lambda e: process_image(e.files[0].path) if e.files else None
    )
    page.overlay.append(file_picker)
    
    def process_image(file_path):
        try:
            # Open and process image
            image = Image.open(file_path)

            # Create a copy for drawing
            draw_image = image.copy()
            draw = ImageDraw.Draw(draw_image)

            # OCR using pytesseract to get data grouped by line
            custom_config = r'--psm 6'  # PSM 6: Assume a single uniform block of text
            data = pytesseract.image_to_data(image, config=custom_config, output_type=pytesseract.Output.DICT)

            # Format the output
            result = f"\n--- OCR Results for {os.path.basename(file_path)} ---\n\n"

            # Group bounding boxes by block and line
            line_boxes = {}
            for i in range(len(data['text'])):
                if data['text'][i].strip():  # Only process non-empty text
                    block_num = data['block_num'][i]
                    line_num = data['line_num'][i]
                    key = (block_num, line_num)

                    # Initialize bounding box for this line if not exists
                    if key not in line_boxes:
                        line_boxes[key] = {
                            "x1": data['left'][i],
                            "y1": data['top'][i],
                            "x2": data['left'][i] + data['width'][i],
                            "y2": data['top'][i] + data['height'][i],
                            "text": data['text'][i]
                        }
                    else:
                        # Expand bounding box to include the current word
                        line_boxes[key]["x1"] = min(line_boxes[key]["x1"], data['left'][i])
                        line_boxes[key]["y1"] = min(line_boxes[key]["y1"], data['top'][i])
                        line_boxes[key]["x2"] = max(line_boxes[key]["x2"], data['left'][i] + data['width'][i])
                        line_boxes[key]["y2"] = max(line_boxes[key]["y2"], data['top'][i] + data['height'][i])
                        line_boxes[key]["text"] += f" {data['text'][i]}"

            # Draw rectangles and log line information
            for key, box in line_boxes.items():
                draw.rectangle(
                    [(box["x1"], box["y1"]), (box["x2"], box["y2"])],
                    outline="blue",
                    width=2
                )
                result += (
                    f"Line Text: {box['text']}\n"
                    f"Position: (x:{box['x1']}, y:{box['y1']})\n"
                    f"Size: {box['x2'] - box['x1']}x{box['y2'] - box['y1']}\n\n"
                )

            # Convert PIL image to base64 for display
            buffered = io.BytesIO()
            draw_image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()

            # Update image display
            img_display.src_base64 = img_str

            # Update text log
            txt_log.value = (txt_log.value or "") + result
            page.update()

        except Exception as e:
            txt_log.value = (txt_log.value or "") + f"\nError processing image: {str(e)}\n"
            page.update()


    
    # Create buttons
    btn_log = ft.ElevatedButton(
        text="Log Timestamp",
        on_click=add_timestamp,
        width=200
    )
    
    pick_files_button = ft.ElevatedButton(
        "Pick Image",
        icon=ft.icons.UPLOAD_FILE,
        on_click=lambda _: file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg"]
        ),
        width=200
    )
    
    btn_process = ft.ElevatedButton(
        text="Process",
        on_click=lambda _: file_picker.pick_files(
            allowed_extensions=["png", "jpg", "jpeg"]
        ),
        width=200,
        icon=ft.icons.DOCUMENT_SCANNER
    )
    
    # Create layout
    main_row = ft.Row(
        controls=[
            # Left column with buttons
            ft.Container(
                content=ft.Column(
                    controls=[
                        btn_log,
                        ft.Divider(height=20, color="transparent"),
                        pick_files_button,
                        ft.Divider(height=10, color="transparent"),
                        btn_process,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.START,
                    spacing=0
                ),
                padding=10,
                expand=1
            ),
            # Vertical divider
            ft.VerticalDivider(),
            # Right column with image and textbox
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Container(
                            content=img_display,
                            alignment=ft.alignment.center,
                            padding=10
                        ),
                        ft.Divider(height=10),
                        txt_log
                    ],
                ),
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
        txt_log.height = page.window_height - 400  # Reduced to make room for image
        img_display.width = page.window_width * 0.6  # 60% of window width
        img_display.height = 300
        page.update()
    
    page.on_resize = page_resize
    # Initial size setup
    txt_log.height = page.window_height - 400
    img_display.width = page.window_width * 0.6

ft.app(target=main)
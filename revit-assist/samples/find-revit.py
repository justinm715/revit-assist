from pywinauto import Application, Desktop, findwindows, mouse
from PIL import Image
import pytesseract
import time

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'


# List all currently open windows
windows = Desktop(backend="uia").windows()

def ocr_data_as_dict(_ocr_data, i):
    output = {
        'text':  _ocr_data['text'][i].strip(),
        'left': _ocr_data['left'][i],
        'top': _ocr_data['top'][i],
        'width': _ocr_data['width'][i],
        'height': _ocr_data['height'][i],
    }
    return output

# Iterate through windows and focus the Revit one
for win in windows:
    title = win.window_text()
    if "SE_2319.2_Marcella Townhomes Cluster 03 R23.rvt" in title:  # Look for "Autodesk Revit" in the title
        print(f"Focusing on: {title}")
        win.set_focus()
        app = Application(backend="uia").connect(handle=win.handle)
        try:
            dialog = findwindows.find_element(title_re=".*Visibility/Graphic Overrides.*", parent=win.handle)
            dialog_window = app.window(handle=dialog.handle)
            dialog_window.set_focus()  # Focus on the dialog
            print(f"Focusing on dialog: {dialog.name}")
            # Take a screenshot of the dialog
            screenshot = dialog_window.capture_as_image()
            file_path = "screenshot.png"
            screenshot.save(file_path)  # Save the screenshot to a file
            print(f"Screenshot saved as 'screenshot.png'")
            image = Image.open(file_path)

            # Use pytesseract for OCR on the screenshot
            ocr_config = '--psm 3'  # Set the page segmentation mode
            # Use pytesseract to get detailed OCR data (with position)
            # ocr_data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT, config=ocr_config)
            ocr_data = pytesseract.image_to_data(screenshot, output_type=pytesseract.Output.DICT, config=ocr_config)
            
            # Loop through OCR data and print text with positions
            print("\nOCR Results (Text and Position):")
            num_boxes = len(ocr_data['text'])
            for i in range(num_boxes):
                text = ocr_data['text'][i]
                if text.strip():  # Skip empty text
                    x, y, w, h = ocr_data['left'][i], ocr_data['top'][i], ocr_data['width'][i], ocr_data['height'][i]
                    print(f"Text: '{text}'")
                    print(f"Position: (x={x}, y={y}, w={w}, h={h})")
                    print("-" * 50)

            
            revit_links_element_positions = {}

            prev = None
            # Find "Revit Links" tab and click on it
            for i in range(num_boxes):
                text = ocr_data['text'][i]
                if text.strip() == 'Revit':
                    prev = 'Revit'
                    continue
                if text.strip() == 'Links':
                    if prev == 'Revit':
                        # found both "Revit" and "Links" text, so we found the tab. record position of the 'Links' text. 
                        print("Found Revit Links")
                        d = ocr_data_as_dict(ocr_data, i)
                        revit_links_element_positions["Links"] = d
                        # Click on it
                        mouse.click(coords=(dialog_window.rectangle().left + int(d["left"] + d["width"]/2), dialog_window.rectangle().top + int(d["top"] + d["height"]/2)))
                        break

            time.sleep(1)
            
            # Find position of "Visibility"
            for i in range(num_boxes):
                text = ocr_data['text'][i]
                if text.strip() == 'Visibility':
                    print("Found Visibility")
                    d = ocr_data_as_dict(ocr_data, i)
                    revit_links_element_positions["Visibility"] = d
                    # Click on it
                    mouse.click(coords=(dialog_window.rectangle().left + int(d["left"] + d["width"]/2), dialog_window.rectangle().top + int(d["top"] + d["height"]/2)))
                    break

            time.sleep(1)

            # Find position of "Display"
            for i in range(num_boxes):
                text = ocr_data['text'][i]
                if text.strip() == 'Display':
                    print("Found Display")
                    d = ocr_data_as_dict(ocr_data, i)
                    revit_links_element_positions["Display"] = d
                    # Click on it
                    mouse.click(coords=(dialog_window.rectangle().left + int(d["left"] + d["width"]/2), dialog_window.rectangle().top + int(d["top"] + d["height"]/2)))
                    break

            time.sleep(1)

            # Gather units
            prev = None
            # Find "Unit" text first. Then next element should be the unit number. Continue.
            for i in range(num_boxes):
                text = ocr_data['text'][i]
                if prev == 'Unit':
                    d = ocr_data_as_dict(ocr_data, i)
                    revit_links_element_positions["Unit " + text.strip()] = d
                    mouse.click(coords=(dialog_window.rectangle().left + int(d["left"] + d["width"]/2), dialog_window.rectangle().top + int(d["top"] + d["height"]/2)))
                    time.sleep(1)
                prev = text.strip()

            print("Found elements:")
            print(revit_links_element_positions)

            # For each unit, click Custom button, then click Worksets tab, then OK

        except findwindows.ElementNotFoundError:
            print("Visibility/Graphic Overrides dialog not found.")

        break
else:
    print("Revit window not found.")



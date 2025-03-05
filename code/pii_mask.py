import pytesseract as pyt
from PIL import Image, ImageDraw, ImageFont
import cv2
import re
import sys
import os
from datetime import datetime
from pyzbar.pyzbar import decode
from PIL import Image, ImageDraw

def import_doc_path():
    global doc_path
    if len(sys.argv) > 1:
        doc_path = sys.argv[1]

if __name__ == "__main__":
    import_doc_path()

# Generate a unique filename with a timestamp
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
masked_doc_path = f"temp/masked_doc_{timestamp}.jpg"

pyt.pytesseract.tesseract_cmd = r'Tesseract-OCR\tesseract.exe'


def qr_blackout(image_path):
    image = Image.open(image_path)
    
    # Decode the QR codes in the image
    decoded_objects = decode(image)
    
    # Create a drawing context
    draw = ImageDraw.Draw(image)
    
    # Iterate through detected QR codes and blackout each one
    for obj in decoded_objects:
        
        # Get the bounding box coordinates
        rect = obj.rect
        left = rect.left
        top = rect.top
        right = rect.left + rect.width
        bottom = rect.top + rect.height
        
        # Draw a black rectangle over the QR code
        draw.rectangle([(left, top), (right, bottom)], fill="black")
    
    # Save or display the modified image
    qr_blackout_image_path = "temp/qrblackout.jpg"
    image.save(qr_blackout_image_path)
    print(f"QR code(s) blacked out and saved as {qr_blackout_image_path}")

    edit_text_in_image(qr_blackout_image_path, masked_doc_path, patterns_and_replacements, 10)



def edit_text_in_image(image_path, output_path, patterns_and_replacements, confidence_threshold):
    image = cv2.imread(image_path)
    img_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    data = pyt.image_to_data(img_rgb, output_type=pyt.Output.DICT)

    img_pil = Image.fromarray(img_rgb)
    draw = ImageDraw.Draw(img_pil)

    text_boxes = []
    accumulated_text = ""

    for i, text in enumerate(data['text']):
        if text.strip() != "":
            confidence = int(data['conf'][i])
            if confidence >= confidence_threshold:
                x, y, w, h = data['left'][i], data['top'][i], data['width'][i], data['height'][i]
                text_boxes.append((text, x, y, w, h))
                accumulated_text += text + " "

    for pattern, replacement in patterns_and_replacements:
        compiled_pattern = re.compile(pattern, re.IGNORECASE)
        if compiled_pattern.search(accumulated_text):
            for text, x, y, w, h in text_boxes:
                if compiled_pattern.search(text):
                    draw.rectangle([x, y, x+w, y+h], fill='white')
                    if replacement:
                        font = ImageFont.load_default()
                        draw.text((x, y), replacement, font=font, fill='red')
                    
    img_pil.save(output_path)

patterns_and_replacements = [
    ("[A-Z]{5}[0-9]{4}[A-Z]{1}", ''),
    (r'\b(?:\d{2}[\/\-\.\s]\d{2}[\/\-\.\s]\d{4}|\d{4}[\/\-\.\s]\d{2}[\/\-\.\s]\d{2})\b', ''),
    (r'\b\d{4} \d{4} \d{4}\b', ''),
    ("[0-9]{11}", ''),
    ("[A-Z]{2}[0-9]{2}", ''),
    ("[0-9]{4}", '')
]

qr_blackout(doc_path)

print("file saved to", masked_doc_path) 

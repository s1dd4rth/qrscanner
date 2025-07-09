#!/usr/bin/env python3
"""
Generate a test image with multiple QR codes for testing the scanner
"""

import qrcode
import json
from PIL import Image, ImageDraw
import numpy as np

def create_test_qr_image():
    """Create a test image with multiple QR codes"""
    
    # Create a large canvas
    canvas_width, canvas_height = 800, 600
    canvas = Image.new('RGB', (canvas_width, canvas_height), 'white')
    
    # QR code data for different modules
    qr_data = [
        "MODULE_001",
        json.dumps({
            "device_id": "SENSOR_001", 
            "type": "temperature_sensor",
            "model": "TempSens3000",
            "firmware": "1.2.3"
        }),
        "ACTUATOR_001",
        json.dumps({
            "device_id": "DISPLAY_001",
            "type": "lcd_display",
            "resolution": "128x64"
        })
    ]
    
    # Positions for QR codes
    positions = [
        (100, 100),   # Top-left
        (400, 100),   # Top-right
        (100, 350),   # Bottom-left
        (400, 350)    # Bottom-right
    ]
    
    # Generate QR codes and place them on canvas
    for i, (data, pos) in enumerate(zip(qr_data, positions)):
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=3,
            border=2,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create QR code image
        qr_img = qr.make_image(fill_color="black", back_color="white")
        
        # Paste QR code onto canvas
        canvas.paste(qr_img, pos)
        
        # Add label below QR code
        draw = ImageDraw.Draw(canvas)
        label = f"Module {i+1}"
        draw.text((pos[0], pos[1] + qr_img.size[1] + 5), label, fill="black")
    
    # Add title
    draw = ImageDraw.Draw(canvas)
    draw.text((canvas_width//2 - 100, 20), "QR Frame Scanner Test Image", fill="black")
    
    # Save the image
    output_path = "/Users/siddarth/test_qr_frame.png"
    canvas.save(output_path)
    print(f"✅ Test image created: {output_path}")
    
    return output_path

if __name__ == "__main__":
    create_test_qr_image()

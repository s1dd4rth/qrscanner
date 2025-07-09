#!/usr/bin/env python3
"""
Create simple QR codes for testing
"""

import qrcode
import json

def create_simple_qr_codes():
    """Create individual QR code images for testing"""
    
    # QR code data
    qr_data = [
        "MODULE_001",
        json.dumps({
            "device_id": "SENSOR_001", 
            "type": "temperature_sensor",
            "model": "TempSens3000"
        }),
        "ACTUATOR_001"
    ]
    
    for i, data in enumerate(qr_data):
        # Create QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        # Create image
        img = qr.make_image(fill_color="black", back_color="white")
        
        # Save individual QR code
        filename = f"/Users/siddarth/qr_test_{i+1}.png"
        img.save(filename)
        print(f"✅ Created: {filename}")
        print(f"   Data: {data}")

if __name__ == "__main__":
    create_simple_qr_codes()

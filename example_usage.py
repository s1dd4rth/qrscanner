#!/usr/bin/env python3
"""
Example usage of the QR Frame Scanner
"""

import json
from qr_frame_scanner import QRFrameScanner


def example_programmatic_usage():
    """Example of using the QR scanner programmatically"""
    
    # Initialize the scanner
    scanner = QRFrameScanner()
    
    print("QR Frame Scanner - Example Usage")
    print("=" * 40)
    
    # Example 1: Scan from image file
    print("\n1. Scanning from image file:")
    print("   (Requires an image file with QR codes)")
    
    # Uncomment and modify the path below to test with an actual image
    # image_path = "path/to/your/frame_image.jpg"
    # result = scanner.scan_frame(image_path=image_path)
    # print(json.dumps(result, indent=2))
    
    # Example 2: Scan from camera (commented out for demo)
    print("\n2. Scanning from camera:")
    print("   (Uncomment the code below to test with camera)")
    
    # result = scanner.scan_frame(live_mode=True)
    # print(json.dumps(result, indent=2))
    
    # Example 3: Expected output format
    print("\n3. Expected output format:")
    sample_output = {
        "timestamp": "2024-01-01T12:00:00.000000",
        "source": "example_frame.jpg",
        "frame_dimensions": {
            "width": 1920,
            "height": 1080
        },
        "modules_detected": 3,
        "modules": [
            {
                "module_id": 1,
                "position": {
                    "center": {"x": 300, "y": 200},
                    "bounding_box": {
                        "min_x": 250, "min_y": 150,
                        "max_x": 350, "max_y": 250,
                        "width": 100, "height": 100
                    },
                    "corners": [
                        {"x": 250, "y": 150}, {"x": 350, "y": 150},
                        {"x": 350, "y": 250}, {"x": 250, "y": 250}
                    ]
                },
                "qr_code_data": "MODULE_001",
                "device_info": {"device_id": "MODULE_001"}
            },
            {
                "module_id": 2,
                "position": {
                    "center": {"x": 600, "y": 400},
                    "bounding_box": {
                        "min_x": 550, "min_y": 350,
                        "max_x": 650, "max_y": 450,
                        "width": 100, "height": 100
                    },
                    "corners": [
                        {"x": 550, "y": 350}, {"x": 650, "y": 350},
                        {"x": 650, "y": 450}, {"x": 550, "y": 450}
                    ]
                },
                "qr_code_data": '{"device_id": "SENSOR_001", "type": "temperature", "model": "TempSens3000"}',
                "device_info": {
                    "device_id": "SENSOR_001",
                    "type": "temperature",
                    "model": "TempSens3000"
                }
            },
            {
                "module_id": 3,
                "position": {
                    "center": {"x": 900, "y": 600},
                    "bounding_box": {
                        "min_x": 850, "min_y": 550,
                        "max_x": 950, "max_y": 650,
                        "width": 100, "height": 100
                    },
                    "corners": [
                        {"x": 850, "y": 550}, {"x": 950, "y": 550},
                        {"x": 950, "y": 650}, {"x": 850, "y": 650}
                    ]
                },
                "qr_code_data": "ACTUATOR_001",
                "device_info": {"device_id": "ACTUATOR_001"}
            }
        ]
    }
    
    print(json.dumps(sample_output, indent=2))
    
    print("\n" + "=" * 40)
    print("To test with real data:")
    print("1. Install dependencies: pip install -r requirements.txt")
    print("2. For image scanning: python qr_frame_scanner.py -i your_image.jpg --pretty")
    print("3. For live camera: python qr_frame_scanner.py -l --pretty")


if __name__ == "__main__":
    example_programmatic_usage()

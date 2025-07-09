#!/usr/bin/env python3
"""
Enhanced QR Scanner with better detection and debugging
"""

import cv2
import json
import numpy as np
from datetime import datetime
import argparse

def enhanced_qr_scan(image_path):
    """Enhanced QR scanning with multiple detection methods"""
    
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        return {"error": f"Could not load image from {image_path}"}
    
    print(f"📸 Image loaded: {img.shape[1]}x{img.shape[0]} pixels")
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Try multiple QR detectors
    detectors = [
        ("OpenCV QRCodeDetector", cv2.QRCodeDetector()),
        ("OpenCV WeChatQRCode", None)  # We'll handle this separately
    ]
    
    results = {
        "timestamp": datetime.now().isoformat(),
        "source": image_path,
        "frame_dimensions": {
            "width": img.shape[1],
            "height": img.shape[0]
        },
        "detection_attempts": [],
        "modules_detected": 0,
        "modules": []
    }
    
    # Method 1: Standard OpenCV QR Detector
    print("🔍 Trying OpenCV QRCodeDetector...")
    qr_detector = cv2.QRCodeDetector()
    
    # Try different preprocessing
    preprocessed_images = [
        ("original", gray),
        ("blur_reduced", cv2.medianBlur(gray, 3)),
        ("contrast_enhanced", cv2.convertScaleAbs(gray, alpha=1.5, beta=0)),
        ("adaptive_threshold", cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2))
    ]
    
    for method_name, processed_img in preprocessed_images:
        print(f"  📋 Testing with {method_name}...")
        
        # Detect QR codes
        retval, decoded_info, points, straight_qrcode = qr_detector.detectAndDecodeMulti(processed_img)
        
        detection_result = {
            "method": f"OpenCV_{method_name}",
            "detected": retval,
            "count": len(decoded_info) if retval else 0
        }
        
        if retval and len(decoded_info) > 0:
            print(f"    ✅ Found {len(decoded_info)} QR codes!")
            detection_result["codes_found"] = len(decoded_info)
            
            for i, (data, bbox) in enumerate(zip(decoded_info, points)):
                if data:  # Only process non-empty data
                    print(f"      📱 QR {i+1}: {data[:50]}...")
                    
                    # Calculate position info
                    center_x = int(np.mean(bbox[:, 0]))
                    center_y = int(np.mean(bbox[:, 1]))
                    min_x, min_y = int(np.min(bbox[:, 0])), int(np.min(bbox[:, 1]))
                    max_x, max_y = int(np.max(bbox[:, 0])), int(np.max(bbox[:, 1]))
                    
                    # Try to parse as JSON
                    device_info = {}
                    try:
                        device_info = json.loads(data)
                    except json.JSONDecodeError:
                        device_info = {"device_id": data}
                    
                    module_info = {
                        "module_id": len(results["modules"]) + 1,
                        "detection_method": method_name,
                        "position": {
                            "center": {"x": center_x, "y": center_y},
                            "bounding_box": {
                                "min_x": min_x, "min_y": min_y,
                                "max_x": max_x, "max_y": max_y,
                                "width": max_x - min_x,
                                "height": max_y - min_y
                            },
                            "corners": [{"x": int(p[0]), "y": int(p[1])} for p in bbox]
                        },
                        "qr_code_data": data,
                        "device_info": device_info
                    }
                    
                    results["modules"].append(module_info)
            
            results["modules_detected"] = len(results["modules"])
            if results["modules_detected"] > 0:
                break  # Found QR codes, stop trying other methods
        else:
            print(f"    ❌ No QR codes found with {method_name}")
        
        results["detection_attempts"].append(detection_result)
    
    # Method 2: Try to detect any rectangular patterns that might be QR codes
    print("🔍 Looking for rectangular patterns...")
    contours, _ = cv2.findContours(cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2), 
                                   cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    rectangles = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > 1000:  # Filter small contours
            x, y, w, h = cv2.boundingRect(contour)
            aspect_ratio = float(w) / h
            if 0.8 <= aspect_ratio <= 1.2:  # Roughly square
                rectangles.append((x, y, w, h, area))
    
    rectangles.sort(key=lambda x: x[4], reverse=True)  # Sort by area
    print(f"  📋 Found {len(rectangles)} potential QR code regions")
    
    results["potential_qr_regions"] = len(rectangles)
    
    return results

def main():
    parser = argparse.ArgumentParser(description="Enhanced QR Scanner with debugging")
    parser.add_argument("-i", "--image", required=True, help="Path to image file")
    parser.add_argument("--pretty", action="store_true", help="Pretty print output")
    
    args = parser.parse_args()
    
    result = enhanced_qr_scan(args.image)
    
    if args.pretty:
        print("\n" + "="*50)
        print("📊 SCAN RESULTS:")
        print("="*50)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

if __name__ == "__main__":
    main()

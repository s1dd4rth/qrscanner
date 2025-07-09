#!/usr/bin/env python3
"""
QR Frame Scanner Application

This application scans a frame containing multiple modules with QR codes,
detects their positions, and returns device information as JSON.
"""

import cv2
import json
import numpy as np
from datetime import datetime
import argparse
import sys
from typing import List, Dict, Any


class QRFrameScanner:
    def __init__(self):
        """Initialize the QR scanner with OpenCV QR detector"""
        self.qr_detector = cv2.QRCodeDetector()
        
    def scan_frame(self, image_path: str = None, camera_index: int = 0, live_mode: bool = False) -> Dict[str, Any]:
        """
        Scan frame for QR codes and return JSON with positions and device info
        
        Args:
            image_path: Path to image file (if not using camera)
            camera_index: Camera index for live scanning
            live_mode: Whether to use live camera feed
            
        Returns:
            Dictionary containing scan results
        """
        if live_mode or image_path is None:
            return self._scan_from_camera(camera_index)
        else:
            return self._scan_from_image(image_path)
    
    def _scan_from_image(self, image_path: str) -> Dict[str, Any]:
        """Scan QR codes from a static image"""
        try:
            # Load image
            frame = cv2.imread(image_path)
            if frame is None:
                return {"error": f"Could not load image from {image_path}"}
            
            return self._process_frame(frame, image_path)
            
        except Exception as e:
            return {"error": f"Error processing image: {str(e)}"}
    
    def _scan_from_camera(self, camera_index: int) -> Dict[str, Any]:
        """Scan QR codes from camera feed"""
        try:
            cap = cv2.VideoCapture(camera_index)
            if not cap.isOpened():
                return {"error": f"Could not open camera {camera_index}"}
            
            print("Camera opened. Press 's' to scan current frame, 'q' to quit")
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Display frame
                cv2.imshow('QR Frame Scanner - Press "s" to scan, "q" to quit', frame)
                
                key = cv2.waitKey(1) & 0xFF
                if key == ord('s'):
                    # Scan current frame
                    result = self._process_frame(frame, "camera_capture")
                    cap.release()
                    cv2.destroyAllWindows()
                    return result
                elif key == ord('q'):
                    break
            
            cap.release()
            cv2.destroyAllWindows()
            return {"message": "Scanning cancelled by user"}
            
        except Exception as e:
            return {"error": f"Camera error: {str(e)}"}
    
    def _process_frame(self, frame: np.ndarray, source: str) -> Dict[str, Any]:
        """Process a frame to detect and decode QR codes"""
        height, width = frame.shape[:2]
        
        # Detect and decode QR codes
        data, bbox, _ = self.qr_detector.detectAndDecode(frame)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "source": source,
            "frame_dimensions": {
                "width": width,
                "height": height
            },
            "modules_detected": 0,
            "modules": []
        }
        
        if bbox is not None and len(bbox) > 0:
            # Handle multiple QR codes
            if isinstance(data, str):
                # Single QR code
                data = [data]
                bbox = [bbox]
            
            for i, (qr_data, qr_bbox) in enumerate(zip(data, bbox)):
                if qr_data:  # Only process if QR code contains data
                    module_info = self._extract_module_info(qr_data, qr_bbox, i + 1)
                    results["modules"].append(module_info)
            
            results["modules_detected"] = len(results["modules"])
        
        return results
    
    def _extract_module_info(self, qr_data: str, bbox: np.ndarray, module_id: int) -> Dict[str, Any]:
        """Extract module information from QR code data and position"""
        # Calculate center position and bounding box
        points = bbox[0]  # Get the four corner points
        
        # Calculate center
        center_x = int(np.mean(points[:, 0]))
        center_y = int(np.mean(points[:, 1]))
        
        # Calculate bounding box
        min_x = int(np.min(points[:, 0]))
        max_x = int(np.max(points[:, 0]))
        min_y = int(np.min(points[:, 1]))
        max_y = int(np.max(points[:, 1]))
        
        # Try to parse QR data as JSON (for structured device info)
        device_info = {}
        try:
            device_info = json.loads(qr_data)
        except json.JSONDecodeError:
            # If not JSON, treat as simple device identifier
            device_info = {"device_id": qr_data}
        
        return {
            "module_id": module_id,
            "position": {
                "center": {
                    "x": center_x,
                    "y": center_y
                },
                "bounding_box": {
                    "min_x": min_x,
                    "min_y": min_y,
                    "max_x": max_x,
                    "max_y": max_y,
                    "width": max_x - min_x,
                    "height": max_y - min_y
                },
                "corners": [
                    {"x": int(point[0]), "y": int(point[1])} 
                    for point in points
                ]
            },
            "qr_code_data": qr_data,
            "device_info": device_info
        }


def main():
    """Main function to run the QR scanner"""
    parser = argparse.ArgumentParser(description="QR Frame Scanner - Scan frames with multiple QR code modules")
    parser.add_argument("-i", "--image", help="Path to image file to scan")
    parser.add_argument("-c", "--camera", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("-l", "--live", action="store_true", help="Use live camera feed")
    parser.add_argument("-o", "--output", help="Output JSON file path")
    parser.add_argument("--pretty", action="store_true", help="Pretty print JSON output")
    
    args = parser.parse_args()
    
    # Initialize scanner
    scanner = QRFrameScanner()
    
    # Perform scan
    if args.image:
        result = scanner.scan_frame(image_path=args.image)
    else:
        result = scanner.scan_frame(camera_index=args.camera, live_mode=True)
    
    # Format output
    if args.pretty:
        json_output = json.dumps(result, indent=2)
    else:
        json_output = json.dumps(result)
    
    # Output results
    if args.output:
        try:
            with open(args.output, 'w') as f:
                f.write(json_output)
            print(f"Results saved to {args.output}")
        except Exception as e:
            print(f"Error saving to file: {e}")
            print("Results:")
            print(json_output)
    else:
        print(json_output)


if __name__ == "__main__":
    main()

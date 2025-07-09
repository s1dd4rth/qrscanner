#!/usr/bin/env python3
"""
Low Resolution QR Scanner with Advanced Enhancement Techniques
"""

import cv2
import json
import numpy as np
from datetime import datetime
import argparse

class LowResQRScanner:
    def __init__(self):
        """Initialize enhanced QR scanner for low resolution images"""
        self.qr_detector = cv2.QRCodeDetector()
    
    def enhance_image_for_qr(self, img):
        """Apply various enhancement techniques for low resolution QR detection"""
        enhanced_images = {}
        
        # Convert to grayscale
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img.copy()
        
        # 1. Original
        enhanced_images['original'] = gray
        
        # 2. Upscale using different interpolation methods
        scale_factor = 2
        height, width = gray.shape
        new_size = (width * scale_factor, height * scale_factor)
        
        enhanced_images['upscale_linear'] = cv2.resize(gray, new_size, interpolation=cv2.INTER_LINEAR)
        enhanced_images['upscale_cubic'] = cv2.resize(gray, new_size, interpolation=cv2.INTER_CUBIC)
        enhanced_images['upscale_lanczos'] = cv2.resize(gray, new_size, interpolation=cv2.INTER_LANCZOS4)
        
        # 3. Denoising
        enhanced_images['denoised'] = cv2.fastNlMeansDenoising(gray)
        
        # 4. Histogram equalization
        enhanced_images['hist_eq'] = cv2.equalizeHist(gray)
        enhanced_images['clahe'] = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8)).apply(gray)
        
        # 5. Sharpening
        kernel_sharpen = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
        enhanced_images['sharpened'] = cv2.filter2D(gray, -1, kernel_sharpen)
        
        # 6. Morphological operations
        kernel = np.ones((2,2), np.uint8)
        enhanced_images['morph_close'] = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, kernel)
        enhanced_images['morph_open'] = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel)
        
        # 7. Edge enhancement
        enhanced_images['edge_enhanced'] = cv2.addWeighted(gray, 1.5, cv2.GaussianBlur(gray, (0,0), 1), -0.5, 0)
        
        # 8. Bilateral filter
        enhanced_images['bilateral'] = cv2.bilateralFilter(gray, 9, 75, 75)
        
        # 9. Adaptive thresholding variations
        enhanced_images['adaptive_thresh_mean'] = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)
        enhanced_images['adaptive_thresh_gaussian'] = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
        
        # 10. Combination approaches
        # Denoise + upscale + sharpen
        denoised = cv2.fastNlMeansDenoising(gray)
        upscaled = cv2.resize(denoised, new_size, interpolation=cv2.INTER_CUBIC)
        enhanced_images['combo_denoise_upscale_sharpen'] = cv2.filter2D(upscaled, -1, kernel_sharpen)
        
        # CLAHE + upscale
        clahe_img = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8,8)).apply(gray)
        enhanced_images['combo_clahe_upscale'] = cv2.resize(clahe_img, new_size, interpolation=cv2.INTER_CUBIC)
        
        return enhanced_images
    
    def scan_low_res_image(self, image_path):
        """Scan low resolution image with multiple enhancement techniques"""
        # Load image
        img = cv2.imread(image_path)
        if img is None:
            return {"error": f"Could not load image from {image_path}"}
        
        print(f"📸 Low-res image loaded: {img.shape[1]}x{img.shape[0]} pixels")
        
        # Get all enhanced versions
        enhanced_images = self.enhance_image_for_qr(img)
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "source": image_path,
            "original_dimensions": {"width": img.shape[1], "height": img.shape[0]},
            "enhancement_attempts": [],
            "modules_detected": 0,
            "modules": []
        }
        
        # Try each enhancement method
        for method_name, enhanced_img in enhanced_images.items():
            print(f"🔍 Trying {method_name}...")
            
            # Try both single and multi detection
            detection_methods = [
                ("single", lambda img: self.qr_detector.detectAndDecode(img)),
                ("multi", lambda img: self.qr_detector.detectAndDecodeMulti(img))
            ]
            
            for det_type, detect_func in detection_methods:
                try:
                    if det_type == "single":
                        data, bbox, _ = detect_func(enhanced_img)
                        if data and bbox is not None:
                            decoded_info = [data]
                            points = [bbox]
                            retval = True
                        else:
                            retval = False
                            decoded_info = []
                            points = []
                    else:
                        retval, decoded_info, points, _ = detect_func(enhanced_img)
                    
                    attempt_result = {
                        "enhancement": method_name,
                        "detection_type": det_type,
                        "detected": retval,
                        "count": len(decoded_info) if retval else 0,
                        "image_size": f"{enhanced_img.shape[1]}x{enhanced_img.shape[0]}"
                    }
                    
                    if retval and len(decoded_info) > 0:
                        print(f"    ✅ Found {len(decoded_info)} QR code(s) with {method_name} ({det_type})!")
                        
                        for i, (data, bbox) in enumerate(zip(decoded_info, points)):
                            if data:  # Only process non-empty data
                                print(f"      📱 QR {i+1}: {data[:50]}...")
                                
                                # Calculate position info (adjust for any scaling)
                                scale_factor = enhanced_img.shape[1] / img.shape[1]
                                
                                if len(bbox.shape) == 3:  # Multi-detection format
                                    bbox = bbox[0]
                                
                                center_x = int(np.mean(bbox[:, 0]) / scale_factor)
                                center_y = int(np.mean(bbox[:, 1]) / scale_factor)
                                min_x, min_y = int(np.min(bbox[:, 0]) / scale_factor), int(np.min(bbox[:, 1]) / scale_factor)
                                max_x, max_y = int(np.max(bbox[:, 0]) / scale_factor), int(np.max(bbox[:, 1]) / scale_factor)
                                
                                # Try to parse as JSON
                                device_info = {}
                                try:
                                    device_info = json.loads(data)
                                except json.JSONDecodeError:
                                    device_info = {"device_id": data}
                                
                                module_info = {
                                    "module_id": len(results["modules"]) + 1,
                                    "enhancement_method": method_name,
                                    "detection_type": det_type,
                                    "position": {
                                        "center": {"x": center_x, "y": center_y},
                                        "bounding_box": {
                                            "min_x": min_x, "min_y": min_y,
                                            "max_x": max_x, "max_y": max_y,
                                            "width": max_x - min_x,
                                            "height": max_y - min_y
                                        },
                                        "corners": [{"x": int(p[0] / scale_factor), "y": int(p[1] / scale_factor)} for p in bbox]
                                    },
                                    "qr_code_data": data,
                                    "device_info": device_info
                                }
                                
                                results["modules"].append(module_info)
                        
                        attempt_result["success"] = True
                        results["enhancement_attempts"].append(attempt_result)
                        
                        # If we found QR codes, we can stop trying other methods
                        if len(results["modules"]) > 0:
                            results["modules_detected"] = len(results["modules"])
                            return results
                    else:
                        print(f"    ❌ No QR codes found with {method_name} ({det_type})")
                        attempt_result["success"] = False
                    
                    results["enhancement_attempts"].append(attempt_result)
                    
                except Exception as e:
                    print(f"    ⚠️ Error with {method_name} ({det_type}): {str(e)}")
                    results["enhancement_attempts"].append({
                        "enhancement": method_name,
                        "detection_type": det_type,
                        "error": str(e)
                    })
        
        results["modules_detected"] = len(results["modules"])
        return results

def main():
    parser = argparse.ArgumentParser(description="Low Resolution QR Scanner")
    parser.add_argument("-i", "--image", required=True, help="Path to low resolution image")
    parser.add_argument("--pretty", action="store_true", help="Pretty print output")
    
    args = parser.parse_args()
    
    scanner = LowResQRScanner()
    result = scanner.scan_low_res_image(args.image)
    
    if args.pretty:
        print("\n" + "="*60)
        print("📊 LOW RESOLUTION QR SCAN RESULTS:")
        print("="*60)
        print(json.dumps(result, indent=2))
    else:
        print(json.dumps(result))

if __name__ == "__main__":
    main()

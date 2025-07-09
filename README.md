# QR Frame Scanner

A Python application that scans frames containing multiple modules with QR codes, detects their positions, and returns device information as JSON.

## Features

- Scan QR codes from static images or live camera feed
- Detect multiple QR codes in a single frame
- Extract position information (center, bounding box, corners)
- Parse device information from QR code data
- Output results as JSON with customizable formatting

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Options

```bash
python qr_frame_scanner.py [options]
```

**Options:**
- `-i, --image PATH`: Path to image file to scan
- `-c, --camera INDEX`: Camera index for live scanning (default: 0)
- `-l, --live`: Use live camera feed
- `-o, --output PATH`: Output JSON file path
- `--pretty`: Pretty print JSON output

### Examples

#### Scan from Image File
```bash
# Basic image scanning
python qr_frame_scanner.py -i frame_image.jpg

# Scan image with pretty JSON output
python qr_frame_scanner.py -i frame_image.jpg --pretty

# Scan image and save to file
python qr_frame_scanner.py -i frame_image.jpg -o results.json --pretty
```

#### Scan from Camera
```bash
# Use default camera (camera 0)
python qr_frame_scanner.py -l

# Use specific camera
python qr_frame_scanner.py -c 1 -l

# Live scan with output to file
python qr_frame_scanner.py -l -o scan_results.json --pretty
```

### Live Camera Controls
When using live camera mode:
- Press **'s'** to scan the current frame
- Press **'q'** to quit without scanning

## Output Format

The application returns JSON with the following structure:

```json
{
  "timestamp": "2024-01-01T12:00:00.000000",
  "source": "image_path_or_camera_capture",
  "frame_dimensions": {
    "width": 1920,
    "height": 1080
  },
  "modules_detected": 2,
  "modules": [
    {
      "module_id": 1,
      "position": {
        "center": {
          "x": 400,
          "y": 300
        },
        "bounding_box": {
          "min_x": 350,
          "min_y": 250,
          "max_x": 450,
          "max_y": 350,
          "width": 100,
          "height": 100
        },
        "corners": [
          {"x": 350, "y": 250},
          {"x": 450, "y": 250},
          {"x": 450, "y": 350},
          {"x": 350, "y": 350}
        ]
      },
      "qr_code_data": "DEVICE_001",
      "device_info": {
        "device_id": "DEVICE_001"
      }
    }
  ]
}
```

## QR Code Data Format

The application supports two formats for QR code data:

### Simple Device ID
```
DEVICE_001
```

### Structured JSON Data
```json
{
  "device_id": "SENSOR_001",
  "type": "temperature_sensor",
  "model": "TempSens3000",
  "firmware": "1.2.3",
  "last_calibration": "2024-01-01"
}
```

## Error Handling

The application includes comprehensive error handling for:
- Invalid image files
- Camera access issues
- Malformed QR codes
- File I/O errors

Errors are returned in the JSON output with an "error" field containing the error message.

## Requirements

- Python 3.7+
- OpenCV 4.5.0+
- NumPy 1.20.0+

## Use Cases

This application is ideal for:
- Industrial equipment monitoring
- Asset tracking systems
- Quality control in manufacturing
- Inventory management
- Modular system configuration verification

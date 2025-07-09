# 🔍 QR Frame Scanner - Streamlit Web App

A powerful web application for scanning frames with multiple QR-coded modules and extracting device information with interactive visualizations.

![QR Frame Scanner](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![OpenCV](https://img.shields.io/badge/OpenCV-27338e?style=for-the-badge&logo=opencv&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

## 🚀 Quick Start

### Local Development

1. **Install Dependencies**:
```bash
source qr_scanner_env/bin/activate
pip install -r streamlit_requirements.txt
```

2. **Launch the App**:
```bash
./run_streamlit_app.sh
```

3. **Open in Browser**: 
   - The app will automatically open at `http://localhost:8501`
   - Upload an image with QR codes to start scanning!

## 🌟 Features

### 📤 **Image Upload**
- Support for multiple formats: PNG, JPG, JPEG, BMP, TIFF
- Drag & drop interface
- Real-time image preview

### 🔍 **Advanced QR Detection**
- **Multiple QR codes** in a single frame
- **High accuracy** detection using OpenCV
- **Position mapping** with precise coordinates
- **Device information** extraction from QR data

### 📊 **Interactive Visualization**
- **Interactive map** showing QR code positions
- **Bounding boxes** and center points
- **Hover information** with QR data preview
- **Zoomable** and pannable interface

### 📋 **Data Analysis**
- **Structured data table** with all module information
- **Expandable details** for each detected module
- **Position coordinates** and dimensions
- **Device information** parsing (JSON support)

### 📥 **Export Options**
- **JSON download** for system integration
- **CSV export** for spreadsheet analysis
- **Timestamped filenames** for organization

## 🎯 Use Cases

### 🏭 **Industrial Applications**
- Equipment monitoring and inventory
- Quality control verification
- Asset tracking systems
- Manufacturing line inspection

### 🔬 **Research & Development**
- Prototype testing and validation
- Modular system configuration
- Laboratory equipment tracking
- Data collection automation

### 📱 **IoT & Smart Systems**
- Device identification and mapping
- Sensor network configuration
- Smart home setup verification
- Remote monitoring systems

## 📊 **Supported QR Code Formats**

### Simple Device IDs
```
MODULE_001
SENSOR_ABC123
DEVICE_XYZ789
```

### Structured JSON Data
```json
{
  "device_id": "SENSOR_001",
  "type": "temperature_sensor",
  "model": "TempSens3000",
  "firmware": "1.2.3",
  "location": "Zone_A",
  "last_calibration": "2024-01-15"
}
```

### Custom Protocols
```
MT:Y.ABCDEF012345678901
PROTOCOL:DEVICE:12345:DATA
```

## 🖥️ **User Interface**

### 📋 **Sidebar**
- **Instructions** and quick help
- **Feature overview** 
- **Sample data** formats
- **Tips** for best results

### 📤 **Main Upload Area**
- **Drag & drop** image upload
- **Image preview** with dimensions
- **Real-time scanning** progress
- **Results summary** with metrics

### 📊 **Results Tabs**

#### 🗺️ **Visualization Tab**
- Interactive map overlay
- QR code position markers
- Bounding box visualization
- Hover details and tooltips

#### 📋 **Data Table Tab**
- Sortable module information
- Expandable detail views
- Position coordinates
- Device specifications

#### 📝 **Raw JSON Tab**
- Complete scan results
- Formatted JSON output
- Copy-friendly format
- API integration ready

#### 📥 **Download Tab**
- JSON file export
- CSV table export
- Timestamped filenames
- Multiple format options

## 🔧 **Technical Specifications**

### **Detection Engine**
- **OpenCV 4.11+** for QR detection
- **Multi-QR support** using `detectAndDecodeMulti()`
- **High precision** coordinate mapping
- **Robust error handling**

### **Visualization**
- **Plotly** interactive charts
- **Responsive design** for all screen sizes
- **Real-time updates** during scanning
- **Export-ready** visualizations

### **Data Processing**
- **Pandas** for data manipulation
- **JSON/CSV** export capabilities
- **Real-time parsing** of QR content
- **Flexible device info** extraction

## 🚀 **Deployment Options**

### **Local Development**
```bash
streamlit run streamlit_qr_app.py
```

### **Streamlit Cloud**
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Deploy with automatic updates

### **Docker Deployment**
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r streamlit_requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_qr_app.py"]
```

### **Custom Server**
```bash
streamlit run streamlit_qr_app.py --server.port 8080 --server.address 0.0.0.0
```

## 📈 **Performance**

- **Real-time processing** for images up to 4K resolution
- **Multiple QR detection** in under 2 seconds
- **Memory efficient** processing
- **Responsive UI** with progress indicators

## 🛠️ **Development**

### **Project Structure**
```
qr-frame-scanner/
├── streamlit_qr_app.py          # Main Streamlit application
├── streamlit_requirements.txt    # Dependencies
├── run_streamlit_app.sh         # Launch script
├── qr_scanner_env/              # Virtual environment
└── test_frame.png               # Sample test image
```

### **Key Components**
- `QRFrameScanner` class for detection logic
- `create_visualization()` for interactive plots
- `create_data_table()` for data formatting
- Streamlit UI with tabbed interface

## 🎯 **Next Steps**

Try the application with your own QR-coded frames:

1. **Launch**: `./run_streamlit_app.sh`
2. **Upload**: Your frame image
3. **Analyze**: Interactive results
4. **Export**: JSON/CSV data
5. **Integrate**: Into your systems

## 📞 **Support**

For questions, issues, or feature requests:
- Check the interactive help in the app sidebar
- Review sample QR code formats
- Test with the provided sample images

---

**Built with ❤️ using Streamlit, OpenCV, and Python** 🐍

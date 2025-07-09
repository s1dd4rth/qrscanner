#!/usr/bin/env python3
"""
QR Frame Scanner - Streamlit Web Application
"""

import streamlit as st
import cv2
import json
import numpy as np
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import io
import base64

# Page configuration
st.set_page_config(
    page_title="QR Frame Scanner",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/your-repo/qr-scanner',
        'Report a bug': 'https://github.com/your-repo/qr-scanner/issues',
        'About': "QR Frame Scanner - Detect multiple QR codes with live camera!"
    }
)

# Mobile-optimized CSS
st.markdown("""
<style>
/* Mobile responsiveness */
@media (max-width: 768px) {
    .stCamera > div {
        max-width: 100% !important;
    }
    
    .stFileUploader > div {
        max-width: 100% !important;
    }
    
    /* Improve camera button visibility */
    [data-testid="camera-input-button"] {
        background-color: #ff4b4b !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 12px 24px !important;
        font-size: 16px !important;
    }
}

/* Camera permission styling */
.camera-permission-banner {
    background: linear-gradient(90deg, #ff4b4b, #ff6b6b);
    color: white;
    padding: 12px;
    border-radius: 8px;
    margin-bottom: 16px;
    text-align: center;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

class QRFrameScanner:
    def __init__(self):
        """Initialize the QR scanner"""
        self.qr_detector = cv2.QRCodeDetector()
    
    def enhance_for_low_res(self, image_cv):
        """Apply enhancement techniques for low resolution images"""
        # Convert to grayscale
        if len(image_cv.shape) == 3:
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
        else:
            gray = image_cv.copy()
        
        # Try upscaling with cubic interpolation
        height, width = gray.shape
        scale_factor = 2
        new_size = (width * scale_factor, height * scale_factor)
        upscaled = cv2.resize(gray, new_size, interpolation=cv2.INTER_CUBIC)
        
        return upscaled, scale_factor
    
    def scan_image(self, image_array):
        """Scan QR codes from image array"""
        try:
            # Convert PIL image to OpenCV format
            if len(image_array.shape) == 3:
                # Convert RGB to BGR for OpenCV
                image_cv = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
            else:
                image_cv = image_array
            
            height, width = image_cv.shape[:2]
            
            # Convert to grayscale for better detection
            gray = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)
            
            # Try multiple detection methods
            results = {
                "timestamp": datetime.now().isoformat(),
                "frame_dimensions": {"width": width, "height": height},
                "modules_detected": 0,
                "modules": []
            }
            
            # Method 1: Standard detection
            retval, decoded_info, points, straight_qrcode = self.qr_detector.detectAndDecodeMulti(gray)
            detection_method = "standard"
            scale_factor = 1
            
            # If no QR codes found, try low resolution enhancement
            if not retval or len(decoded_info) == 0:
                st.info("🔍 No QR codes found with standard detection, trying low-resolution enhancement...")
                enhanced_img, scale_factor = self.enhance_for_low_res(image_cv)
                retval, decoded_info, points, straight_qrcode = self.qr_detector.detectAndDecodeMulti(enhanced_img)
                detection_method = "low_res_enhanced"
                
                if retval and len(decoded_info) > 0:
                    st.success(f"✅ Low-resolution enhancement successful! Found {len(decoded_info)} QR codes.")
                else:
                    st.warning("⚠️ No QR codes detected even with enhancement.")
            
            if retval and len(decoded_info) > 0:
                for i, (data, bbox) in enumerate(zip(decoded_info, points)):
                    if data:  # Only process non-empty data
                        # Calculate position info (adjust for scaling if enhanced)
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
                            "module_id": i + 1,
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
                
                results["modules_detected"] = len(results["modules"])
            
            return results
            
        except Exception as e:
            return {"error": f"Error processing image: {str(e)}"}

def create_visualization(results, image_array):
    """Create interactive visualization of detected QR codes"""
    if "modules" not in results or len(results["modules"]) == 0:
        return None
    
    height, width = image_array.shape[:2]
    
    # Create plotly figure
    fig = go.Figure()
    
    # Add background image
    fig.add_layout_image(
        dict(
            source=Image.fromarray(image_array),
            xref="x", yref="y",
            x=0, y=height,
            sizex=width, sizey=height,
            sizing="stretch",
            opacity=0.8,
            layer="below"
        )
    )
    
    # Add QR code markers and bounding boxes
    for i, module in enumerate(results["modules"]):
        pos = module["position"]
        center = pos["center"]
        bbox = pos["bounding_box"]
        
        # Add bounding box
        fig.add_shape(
            type="rect",
            x0=bbox["min_x"], y0=height - bbox["max_y"],
            x1=bbox["max_x"], y1=height - bbox["min_y"],
            line=dict(color="red", width=2),
            fillcolor="rgba(255,0,0,0.1)"
        )
        
        # Add center point
        fig.add_trace(go.Scatter(
            x=[center["x"]], 
            y=[height - center["y"]],
            mode="markers+text",
            marker=dict(size=10, color="red"),
            text=f"Module {module['module_id']}",
            textposition="top center",
            name=f"Module {module['module_id']}",
            hovertemplate=f"<b>Module {module['module_id']}</b><br>" +
                         f"QR Data: {module['qr_code_data'][:30]}...<br>" +
                         f"Position: ({center['x']}, {center['y']})<br>" +
                         f"Size: {bbox['width']}×{bbox['height']}<extra></extra>"
        ))
    
    # Update layout
    fig.update_layout(
        title="QR Code Detection Results",
        xaxis=dict(range=[0, width], showgrid=False, zeroline=False),
        yaxis=dict(range=[0, height], showgrid=False, zeroline=False, scaleanchor="x"),
        width=800,
        height=400,
        showlegend=True
    )
    
    return fig

def create_data_table(results):
    """Create a data table from scan results"""
    if "modules" not in results or len(results["modules"]) == 0:
        return None
    
    data = []
    for module in results["modules"]:
        pos = module["position"]
        device_info = module["device_info"]
        
        row = {
            "Module ID": module["module_id"],
            "QR Code Data": module["qr_code_data"],
            "Center X": pos["center"]["x"],
            "Center Y": pos["center"]["y"],
            "Width": pos["bounding_box"]["width"],
            "Height": pos["bounding_box"]["height"],
            "Device ID": device_info.get("device_id", "N/A")
        }
        
        # Add additional device info fields
        for key, value in device_info.items():
            if key != "device_id":
                row[f"Device {key.title()}"] = value
        
        data.append(row)
    
    return pd.DataFrame(data)

def download_json(data, filename="qr_scan_results.json"):
    """Create download link for JSON data"""
    json_str = json.dumps(data, indent=2)
    b64 = base64.b64encode(json_str.encode()).decode()
    href = f'<a href="data:application/json;base64,{b64}" download="{filename}">📥 Download JSON Results</a>'
    return href

def main():
    # Header
    st.title("🔍 QR Frame Scanner")
    st.markdown("**Scan frames with multiple QR-coded modules and extract device information**")
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Instructions")
        st.markdown("""
        1. **Choose input method**: Upload file or capture with camera
        2. **Scan QR codes** in your frame
        3. **View detected modules** in the results
        4. **Download JSON/CSV data** for integration
        
        ### 📊 Features:
        - 📁 File upload support (PNG, JPG, etc.)
        - 📷 **Live camera capture**
        - 🔍 Multiple QR code detection
        - 🗺️ Position mapping & visualization
        - 📱 Device information extraction
        - 📥 JSON/CSV export
        - 🔧 Low-resolution enhancement
        """)
        
        st.header("📷 Camera Tips")
        st.markdown("""
        For best camera results:
        - 📱 Ensure good lighting
        - 🎯 Position QR codes clearly in frame
        - 📏 Keep steady for sharp focus
        - 🔍 Get close enough for QR details
        - 🔄 Use enhancement if codes are small
        
        ### 📱 Mobile Instructions:
        - **Allow camera access** when prompted by browser
        - Use **landscape mode** for wide frames
        - **Hold device steady** for clear capture
        - **Tap capture** when QR codes are in view
        """)
        
        st.header("📁 Sample Data")
        st.markdown("""
        QR codes can contain:
        - Simple device IDs: `MODULE_001`
        - JSON data: `{"device_id": "SENSOR_001", "type": "temperature"}`
        """)
    
    # Main content
    scanner = QRFrameScanner()
    
    # Input method selection
    st.header("📤 Input Method")
    input_method = st.radio(
        "Choose input method:",
        ["📁 Upload Image File", "📷 Live Camera Capture"],
        horizontal=True
    )
    
    uploaded_file = None
    camera_image = None
    
    if input_method == "📁 Upload Image File":
        uploaded_file = st.file_uploader(
            "Choose an image file with QR codes",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload an image containing one or more QR codes"
        )
    else:
        st.subheader("📷 Camera Capture")
        
        # Mobile permission banner
        st.markdown("""
        <div class="camera-permission-banner">
            📱 Mobile Users: Your browser will request camera permission. Please allow access to use live scanning!
        </div>
        """, unsafe_allow_html=True)
        
        # Camera instructions
        st.info("""
        📷 **Camera Instructions:**
        - Allow camera access when prompted
        - Position QR codes clearly in the frame
        - Ensure good lighting for best results
        - Tap the capture button when ready
        """)
        
        camera_image = st.camera_input(
            "Take a picture of your QR frame",
            help="Position your frame with QR codes in the camera view and click the capture button"
        )
    
    # Process either uploaded file or camera image
    image = None
    image_source = None
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        image_source = "File Upload"
    elif camera_image is not None:
        image = Image.open(camera_image)
        image_source = "Camera Capture"
    
    if image is not None:
        # Display image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader(f"📸 {image_source}")
            st.image(image, caption=f"Source: {image_source}", use_container_width=True)
            
            # Image info
            st.info(f"**Image Size:** {image.size[0]} × {image.size[1]} pixels")
            if image_source == "Camera Capture":
                st.success("📷 Camera image captured successfully!")
        
        with col2:
            st.subheader("🔍 Scanning...")
            
            # Convert to array for processing
            image_array = np.array(image)
            
            # Scan for QR codes
            with st.spinner("Detecting QR codes..."):
                results = scanner.scan_image(image_array)
            
            if "error" in results:
                st.error(f"❌ Error: {results['error']}")
            else:
                # Display results summary
                modules_found = results["modules_detected"]
                if modules_found > 0:
                    st.success(f"✅ Found {modules_found} QR code(s)!")
                    
                    # Quick stats
                    st.metric("Modules Detected", modules_found)
                    st.metric("Frame Size", f"{results['frame_dimensions']['width']}×{results['frame_dimensions']['height']}")
                else:
                    st.warning("⚠️ No QR codes detected in the image")
        
        # Results section
        if image is not None and "modules" in results and len(results["modules"]) > 0:
            st.header("📊 Scan Results")
            
            # Tabs for different views
            tab1, tab2, tab3, tab4 = st.tabs(["🗺️ Visualization", "📋 Data Table", "📝 Raw JSON", "📥 Download"])
            
            with tab1:
                st.subheader("Interactive QR Code Map")
                fig = create_visualization(results, image_array)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.warning("Could not create visualization")
            
            with tab2:
                st.subheader("Module Information")
                df = create_data_table(results)
                if df is not None:
                    st.dataframe(df, use_container_width=True)
                    
                    # Module details
                    st.subheader("🔍 Module Details")
                    for module in results["modules"]:
                        with st.expander(f"Module {module['module_id']}: {module['device_info'].get('device_id', 'Unknown')}"):
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("**Position Information:**")
                                pos = module["position"]
                                st.write(f"- Center: ({pos['center']['x']}, {pos['center']['y']})")
                                st.write(f"- Size: {pos['bounding_box']['width']} × {pos['bounding_box']['height']}")
                                st.write(f"- Bounding Box: ({pos['bounding_box']['min_x']}, {pos['bounding_box']['min_y']}) to ({pos['bounding_box']['max_x']}, {pos['bounding_box']['max_y']})")
                            
                            with col2:
                                st.write("**QR Code Data:**")
                                st.code(module["qr_code_data"], language="text")
                                st.write("**Device Information:**")
                                st.json(module["device_info"])
            
            with tab3:
                st.subheader("Raw JSON Output")
                st.json(results)
            
            with tab4:
                st.subheader("Download Results")
                st.markdown("Download the scan results in JSON format for integration with other systems.")
                
                # Download button
                json_str = json.dumps(results, indent=2)
                st.download_button(
                    label="📥 Download JSON Results",
                    data=json_str,
                    file_name=f"qr_scan_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )
                
                # CSV download for table data
                df = create_data_table(results)
                if df is not None:
                    csv = df.to_csv(index=False)
                    st.download_button(
                        label="📊 Download CSV Table",
                        data=csv,
                        file_name=f"qr_modules_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                        mime="text/csv"
                    )
    
    # Footer
    st.markdown("---")
    st.markdown("**QR Frame Scanner** - Detect and analyze multiple QR codes in frames | Built with Streamlit 🚀")

if __name__ == "__main__":
    main()

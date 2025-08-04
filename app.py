import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
import os

# Create a directory for uploads if it doesn't exist
UPLOAD_DIR = "user_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Function to detect and decode barcodes
def decode_barcodes(image):
    decoded_objects = decode(image)
    barcode_data = []
    for obj in decoded_objects:
        barcode_data.append({
            'data': obj.data.decode('utf-8'),
            'type': obj.type
        })
    return barcode_data

st.title("Multi-Barcode Decoder App")

st.write("Upload an image containing one or more barcodes to decode them.")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png", "bmp", "gif", "webp"])

if uploaded_file is not None:
    try:
        # Save the uploaded file to disk
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getvalue())
        
        # Now open the saved file with PIL
        image = Image.open(file_path)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        
        barcodes = decode_barcodes(image)
        
        if barcodes:
            st.success(f"Found {len(barcodes)} barcode(s)!")
            for i, bc in enumerate(barcodes, 1):
                st.write(f"**Barcode {i}:**")
                st.write(f"- Type: {bc['type']}")
                st.write(f"- Data: {bc['data']}")
        else:
            st.warning("No barcodes detected in the image.")
        
        # Optional: Clean up the file after processing (to save space)
        os.remove(file_path)
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        st.error("Please ensure you've uploaded a valid image file (e.g., JPG, PNG) and try again.")

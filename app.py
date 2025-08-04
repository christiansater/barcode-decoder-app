import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image

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
        uploaded_file.seek(0)  # Reset file pointer to the start
        image = Image.open(uploaded_file)
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
    except Exception as e:
        st.error(f"Error processing the image: {e}")
        st.error("Please ensure you've uploaded a valid image file (e.g., JPG, PNG) and try again.")

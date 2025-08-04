import streamlit as st
from pyzbar.pyzbar import decode
from PIL import Image
from io import BytesIO
import pillow_heif  # Import to register HEIF/HEIC support
import pandas as pd

# Function to detect and decode barcodes from an image
def decode_barcodes(image):
    decoded_objects = decode(image)
    barcode_data = []
    for obj in decoded_objects:
        barcode_data.append({
            'type': obj.type,
            'data': obj.data.decode('utf-8')
        })
    return barcode_data

st.title("Multi-Barcode Decoder App")

st.write("Upload one or more images containing barcodes to decode them. Results can be exported as an Excel file.")

uploaded_files = st.file_uploader("Choose images...", type=["jpg", "jpeg", "png", "bmp", "gif", "webp", "heic", "heif"], accept_multiple_files=True)

if uploaded_files:
    all_barcodes = []  # To collect data for Excel export
    for uploaded_file in uploaded_files:
        try:
            # Use BytesIO to open the image from memory
            image_bytes = uploaded_file.getvalue()
            image = Image.open(BytesIO(image_bytes))
            st.image(image, caption=f"Uploaded Image: {uploaded_file.name}", use_column_width=True)
            
            barcodes = decode_barcodes(image)
            
            if barcodes:
                st.success(f"Found {len(barcodes)} barcode(s) in {uploaded_file.name}!")
                for i, bc in enumerate(barcodes, 1):
                    st.write(f"**Barcode {i} in {uploaded_file.name}:**")
                    st.write(f"- Type: {bc['type']}")
                    st.write(f"- Data: {bc['data']}")
                    
                    # Collect for export
                    all_barcodes.append({
                        'Image Name': uploaded_file.name,
                        'Barcode Index': i,
                        'Type': bc['type'],
                        'Data': bc['data']
                    })
            else:
                st.warning(f"No barcodes detected in {uploaded_file.name}.")
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {e}")
    
    # If there are barcodes, provide Excel download
    if all_barcodes:
        df = pd.DataFrame(all_barcodes)
        excel_buffer = BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False)
        excel_buffer.seek(0)
        
        st.download_button(
            label="Download Excel File",
            data=excel_buffer,
            file_name="decoded_barcodes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

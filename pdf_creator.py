import streamlit as st
from PIL import Image
import io
import zipfile
import tempfile
import os

def process_zip_to_pdf(zip_file):
    """Convert images from zip file to PDF."""
    try:
        # Create a temporary directory to extract zip contents
        with tempfile.TemporaryDirectory() as temp_dir:
            # Extract zip contents
            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)
            
            # Get all image files
            images = []
            valid_extensions = {'.jpg', '.jpeg', '.png'}
            
            # Walk through all files in temp directory
            for root, _, files in os.walk(temp_dir):
                for file in sorted(files):  # Sort files for consistent order
                    if any(file.lower().endswith(ext) for ext in valid_extensions):
                        image_path = os.path.join(root, file)
                        try:
                            img = Image.open(image_path)
                            # Convert to RGB if necessary
                            if img.mode != 'RGB':
                                img = img.convert('RGB')
                            images.append(img)
                        except Exception as e:
                            st.warning(f"Skipped {file}: {str(e)}")
            
            if not images:
                st.error("No valid images found in the ZIP file")
                return None
            
            # Create PDF in memory
            pdf_buffer = io.BytesIO()
            # Save first image as PDF with remaining images appended
            images[0].save(
                pdf_buffer,
                "PDF",
                save_all=True,
                append_images=images[1:],
                resolution=100.0
            )
            
            return pdf_buffer.getvalue()
            
    except Exception as e:
        st.error(f"Error processing ZIP file: {str(e)}")
        return None

def main():
    st.title("ZIP to PDF Converter")
    st.write("Upload a ZIP file containing images to convert them into a single PDF file.")

    # File uploader for ZIP
    uploaded_file = st.file_uploader(
        "Choose a ZIP file",
        type=['zip']
    )

    if uploaded_file:
        st.write(f"Uploaded: {uploaded_file.name}")
        
        if st.button("Convert to PDF"):
            with st.spinner("Converting images from ZIP to PDF..."):
                pdf_bytes = process_zip_to_pdf(uploaded_file)
                
                if pdf_bytes:
                    st.success("Conversion completed!")
                    st.download_button(
                        label="Download PDF",
                        data=pdf_bytes,
                        file_name="converted_images.pdf",
                        mime="application/pdf"
                    )
        
        st.info("""
        📝 Notes:
        - Supported image formats: JPG, JPEG, PNG
        - Images will be ordered alphabetically by filename
        - The ZIP file should contain only images you want to convert
        """)

if __name__ == "__main__":
    main()

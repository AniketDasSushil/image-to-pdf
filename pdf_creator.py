import os
from PIL import Image

def combine_images_to_pdf(folder_path):
    # Get all image files in the folder
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    
    if not image_files:
        print("No image files found in the specified folder.")
        return
    
    # Sort the files to ensure a consistent order
    image_files.sort()
    
    # Open all images
    images = []
    for image_file in image_files:
        try:
            image_path = os.path.join(folder_path, image_file)
            with Image.open(image_path) as img:
                # Convert image to RGB mode if it's not already
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                # Create a copy of the image in memory
                img_copy = img.copy()
                images.append(img_copy)
            print(f"Successfully processed: {image_file}")
        except Exception as e:
            print(f"Error processing {image_file}: {str(e)}")
    
    if not images:
        print("No valid images found in the folder.")
        return
    
    # Define the output PDF file path
    pdf_filename = "combined_images.pdf"
    pdf_path = os.path.join(folder_path, pdf_filename)
    
    # Save images as PDF
    try:
        images[0].save(pdf_path, "PDF", save_all=True, append_images=images[1:])
        print(f"PDF created successfully: {pdf_path}")
    except Exception as e:
        print(f"Error creating PDF: {str(e)}")
        print("Details of processed images:")
        for i, img in enumerate(images):
            print(f"Image {i+1}: Size={img.size}, Mode={img.mode}")

# Example usage
folder_path = r"C:\Users\adas4\Downloads\544733953"  # Replace with your folder path
combine_images_to_pdf(folder_path)

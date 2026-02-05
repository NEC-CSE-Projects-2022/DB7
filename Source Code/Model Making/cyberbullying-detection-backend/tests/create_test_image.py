from PIL import Image, ImageDraw
import os

def create_test_image():
    # Create directory if it doesn't exist
    os.makedirs('tests/data', exist_ok=True)
    
    # Create a new image with white background
    img = Image.new('RGB', (800, 200), color='white')
    d = ImageDraw.Draw(img)
    
    # Add test text to image
    test_text = "This is a test image with some text"
    d.text((10, 80), test_text, fill='black')
    
    # Save path
    save_path = os.path.join('tests', 'data', 'test_image.png')
    img.save(save_path)
    print(f"Created test image at: {save_path}")

if __name__ == "__main__":
    create_test_image()
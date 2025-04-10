import os
from PIL import Image, ImageDraw, ImageFont
import qrcode
from psd_tools import PSDImage

def mm_to_pixels(mm, dpi=300):
    """Convert millimeters to pixels at the given DPI"""
    return int((mm / 25.4) * dpi)

def generate_qr_code(data, mm_size=(95, 95), dpi=300):
    """Generate a QR code with the specified size in millimeters"""
    # Convert mm to pixels
    size_pixels = (mm_to_pixels(mm_size[0], dpi), mm_to_pixels(mm_size[1], dpi))
    
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(size_pixels)
    return img

def process_psd_with_codes(psd_path, codes_path, output_dir, qr_size_mm=(95, 95), dpi=300):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Read codes from file
    with open(codes_path, 'r') as f:
        codes = [line.strip() for line in f if line.strip()]
    
    # Process codes in pairs
    for i in range(0, len(codes), 2):
        if i + 1 >= len(codes):
            print(f"Skipping unpaired code: {codes[i]}")
            break
            
        code1 = codes[i]
        code2 = codes[i+1]
        iteration = (i // 2) + 1
        
        print(f"Processing iteration {iteration}: {code1} and {code2}")
        
        # Open the PSD file
        psd = PSDImage.open(psd_path)
        
        # Find the text and QR code layers
        text_layer1 = None
        text_layer2 = None
        qr_layer1 = None
        qr_layer2 = None
        
        for layer in psd.descendants():
            if layer.name == "UniqueCode_01":
                text_layer1 = layer
            elif layer.name == "UniqueCode_02":
                text_layer2 = layer
            elif layer.name == "QRCode_01":
                qr_layer1 = layer
            elif layer.name == "QRCode_02":
                qr_layer2 = layer
        
        if not all([text_layer1, text_layer2, qr_layer1, qr_layer2]):
            print("Could not find all required layers!")
            missing = []
            if not text_layer1: missing.append("UniqueCode_01")
            if not text_layer2: missing.append("UniqueCode_02") 
            if not qr_layer1: missing.append("QRCode_01")
            if not qr_layer2: missing.append("QRCode_02")
            print(f"Missing layers: {', '.join(missing)}")
            continue
        
        # Create working PSD image
        psd_image = psd.composite()
        
        # Get original positions for reference
        text1_bbox = text_layer1.bbox
        text2_bbox = text_layer2.bbox
        qr1_bbox = qr_layer1.bbox
        qr2_bbox = qr_layer2.bbox
        
        # Create QR codes with specified dimensions in mm
        qr1_img = generate_qr_code(code1, qr_size_mm, dpi)
        qr2_img = generate_qr_code(code2, qr_size_mm, dpi)
        
        # Convert to RGBA mode
        if qr1_img.mode != 'RGBA':
            qr1_img = qr1_img.convert('RGBA')
        if qr2_img.mode != 'RGBA':
            qr2_img = qr2_img.convert('RGBA')
        
        # Paste QR codes onto the composite at the original layer positions
        psd_image.paste(qr1_img, (qr1_bbox[0], qr1_bbox[1]))
        psd_image.paste(qr2_img, (qr2_bbox[0], qr2_bbox[1]))
        
        # Create font for text
        # Using a default font - you may want to use a specific font with appropriate size
        font = ImageFont.truetype("BebasNeue-Regular.ttf", size=133)
        
        # Add text
        draw = ImageDraw.Draw(psd_image)
        draw.text((text1_bbox[0], text1_bbox[1]), code1, fill="black", font=font)
        draw.text((text2_bbox[0], text2_bbox[1]), code2, fill="black", font=font)
        
        # Save the result
        output_path = os.path.join(output_dir, f"output_{iteration:04d}.png")
        psd_image.save(output_path)
        print(f"Saved: {output_path}")

if __name__ == "__main__":
    # Configuration
    PSD_FILE_PATH = "E:\\Pathfinder\\Marathon2k25\\ChestNumbers-Design.psb"  # Path to your PSD file
    CODES_FILE_PATH = "codes.txt"        # Path to your codes file
    OUTPUT_DIRECTORY = "codes_output"          # Output directory for generated PNGs
    QR_SIZE_MM = (95, 95)                # QR code size in millimeters
    DPI = 300                            # Resolution for conversion from mm to pixels
    
    process_psd_with_codes(PSD_FILE_PATH, CODES_FILE_PATH, OUTPUT_DIRECTORY, QR_SIZE_MM, DPI)
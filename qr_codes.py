import os
import argparse
import qrcode

def mm_to_pixels(mm, dpi=300):
    """Convert millimeters to pixels at the given DPI"""
    return int((mm / 25.4) * dpi)

def generate_qr_code(data, output_path, mm_size=(95, 95), dpi=300):
    """Generate a QR code with the specified size in millimeters and save to file"""
    # Convert mm to pixels
    size_pixels = (mm_to_pixels(mm_size[0], dpi), mm_to_pixels(mm_size[1], dpi))
    
    # Create QR code
    qr = qrcode.QRCode(
        version=1,  # Auto-determine version based on data
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # Medium error correction
        box_size=10,
        border=4,
        )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create image
    img = qr.make_image(fill_color="black", back_color="white")
    img = img.resize(size_pixels)
    
    # Save image
    img.save(output_path)
    print(f"QR code saved to: {output_path}")
    return img

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate QR codes at 95mm x 95mm size')
    parser.add_argument('--data', type=str, help='Data to encode in the QR code')
    parser.add_argument('--file', type=str, help='File containing data (one code per line)')
    parser.add_argument('--output', type=str, default='output', help='Output directory')
    parser.add_argument('--dpi', type=int, default=300, help='DPI for converting mm to pixels')
    parser.add_argument('--size', type=int, nargs=2, default=[95, 95], help='Size in mm (width height)')
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Input validation
    if not args.data and not args.file:
        # If no arguments, use interactive mode
        print("No input provided. Entering interactive mode.")
        while True:
            data = input("Enter QR code content (or 'exit' to quit): ")
            if data.lower() == 'exit':
                break
            if data:
                output_path = os.path.join(args.output, f"qr_{data.replace(' ', '_')}.png")
                generate_qr_code(data, output_path, args.size, args.dpi)
    
    # Process single data item
    elif args.data:
        output_path = os.path.join(args.output, f"qr_{args.data.replace(' ', '_')}.png")
        generate_qr_code(args.data, output_path, args.size, args.dpi)
    
    # Process file with multiple items
    elif args.file:
        with open(args.file, 'r') as f:
            for i, line in enumerate(f):
                data = line.strip()
                if data:
                    output_path = os.path.join(args.output, f"qr_{i+1:04d}.png")
                    generate_qr_code(data, output_path, args.size, args.dpi)

if __name__ == "__main__":
    main()
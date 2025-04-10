from photoshop import Session 

import qrcode
from PIL import Image
import os

def generate_qr_code(data, size_pixels, output_file='qr_code.png'):
    # Generate basic QR code
    qr = qrcode.QRCode(
        version=1,  # Automatically determine version based on data length
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,  # Temporary; will resize later
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    # Create the QR image
    img = qr.make_image(fill_color="black", back_color="white").convert('RGB')
    img = img.resize((size_pixels, size_pixels))

    # Save the image
    img.save(output_file)
    print(f"QR code saved to '{output_file}' with size {size_pixels}x{size_pixels}px")
    return img

with open("codes-2  .txt","r") as f:
    codes = [line.strip("\n") for line in f.readlines()]
    # for code in codes:
    #     generate_qr_code(code, size_pixels=1122, output_file=f"qr_codes/{code}.png")
    f.close()

with Session() as ps:
    doc = ps.app.open("E:\\Pathfinder\\Marathon2k25\\ChestNumbers-Design.psb")
    replace_contents = ps.app.stringIDToTypeID("placedLayerReplaceContents")
    idNull = ps.app.charIDToTypeID("null")

    textLayer1 = None
    textLayer2 = None

    qrLayer1 = doc.artLayers["QRCode_01"]
    qrLayer2 = doc.artLayers["QRCode_02"]

    for layer in doc.layers:
        if layer.name == "UniqueCode_01":
            textLayer1 = layer
        elif layer.name == "UniqueCode_02":
            textLayer2 = layer
        else:
            continue
    
    for i in range(0, len(codes), 2):
        code_pair = (codes[i], codes[i+1])
        print(i, code_pair)
        # continue

        doc.activeLayer = qrLayer1
        desc1 = ps.ActionDescriptor()
        desc1.putPath(idNull, os.path.join("E:\\Projects\\chest-numbers-script\\qr_codes",f"{code_pair[0]}.png"))
        textLayer1.textItem.contents = code_pair[0]
        ps.app.executeAction(replace_contents, desc1)

        doc.activeLayer = qrLayer2
        desc2 = ps.ActionDescriptor()
        desc2.putPath(idNull, os.path.join("E:\\Projects\\chest-numbers-script\\qr_codes",f"{code_pair[1]}.png"))
        textLayer2.textItem.contents = code_pair[1]
        ps.app.executeAction(replace_contents, desc2)

        png_file = os.path.join('E:\\Projects\\chest-numbers-script\\outputs',f"{code_pair[1]}.png")

        ps.active_document.saveAs(png_file, ps.PNGSaveOptions())
        # os.startfile(png_file)

        

        

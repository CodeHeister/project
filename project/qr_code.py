import qrcode
import qrcode.image.svg
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from PIL import Image, ImageDraw, ImageFont
import base64
import os
from io import BytesIO
from functools import cache 
from dataclasses import dataclass
from decimal import Decimal
from .settings import BASE_DIR

@dataclass
class QrCodeFactory:
    data: str

    def png(self, text=None):
        # Create a QR code instance
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
        )

        # Add data to the QR code
        qr.add_data(self.data)
        qr.make(fit=True)

        # Create an image from the QR code
        img = qr.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer())

        if text and isinstance(text, str):
            # Add white space below for text
            new_height = img.size[1] + 30  # Increase the height as needed
            labled_image = Image.new("RGB", (img.size[0], new_height), color="white")
            labled_image.paste(img, (0, 0))

            img = labled_image

            draw = ImageDraw.Draw(img)
        
            # Provide the correct path to the Inter font file
            font_path = os.path.join(BASE_DIR, 'static', 'fonts', 'inter.ttf') # Replace with the actual path
            font_size = 18  # Set the desired font size

            font = ImageFont.truetype(font_path, font_size)
            
            text_size = get_text_dimensions(text, font)
            text_position = ((img.size[0] - text_size[0]) // 2, img.size[1] - text_size[1] - 18)
            draw.text(text_position, text, font=font, fill="black")

        # Convert the image to bytes
        img_bytes = BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes.seek(0)
        img_data = img_bytes.read()

        # Encode the image data in base64
        img_base64 = base64.b64encode(img_data).decode('utf-8').replace("\n", "")

        # Create the data URI
        img_data_uri = "data:image/png;base64," + img_base64

        return img_data_uri

    def svg(self):

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=2,
            image_factory=qrcode.image.svg.SvgPathImage,
            )
        qr.add_data(self.data)
        qr.make(fit=True)
        
        img = qr.make_image(attrib={'class': 'qr-code'})

        return img.to_string(encoding='unicode')

def get_text_dimensions(text_string, font):
    ascent, descent = font.getmetrics()

    text_width = font.getmask(text_string).getbbox()[2]
    text_height = font.getmask(text_string).getbbox()[3] + descent

    return (text_width, text_height)

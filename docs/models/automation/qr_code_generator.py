import qrcode
import io
import base64
import os

URL_PREFIX = "https://github.com/msampathkumar/msampathkumar.github.io/tree/master/docs/models/reports"

def generate_qr_code(output_filename: str) -> str:
    """Generates a QR code for the given URL and returns it as a base64 encoded PNG string."""
    qr_code_url = f"{URL_PREFIX}/{output_filename}"
    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(qr_code_url)
    qr.make(fit=True)
    # img = qr.make_image(fill_color='black', back_color='white')
    img = qr.make_image(fill_color='green', back_color='white')

    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    
    return base64.b64encode(buffered.getvalue()).decode()

import qrcode
import re
from io import BytesIO

def generate_qr_from_file(file_path: str) -> BytesIO:
    with open(file_path, 'r') as file:
        conf = file.read()

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=1,
    )
    qr.add_data(conf)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    byte_io = BytesIO()
    img.save(byte_io)
    byte_io.seek(0)
    
    return byte_io

def is_valid_username(username: str) -> bool:
    return bool(re.match(r"^[a-zA-Z0-9_-]+$", username)) and len(username) < 16

def is_username_in_clients(username: str, clients: str) -> bool:
    return username in re.findall(r"\d+\)\s([a-zA-Z0-9_]+)", clients)
           

import qrcode
import re
from io import BytesIO
from .constants import WG_CONF_PATH

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

def get_next_available_ip():
    used_ip = set()

    with open(WG_CONF_PATH, "r") as file:
        for line in file:
            match = re.search(r"AllowedIPs\s*=\s*10\.66\.66\.(\d+)/32", line)
            if match:
                used_ip.add(int(match.group(1)))

    for i in range(2, 255):
        if i not in used_ip:
            return str(i)

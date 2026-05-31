import qrcode
import os

# Change this whenever ngrok URL changes
BASE_URL = "https://argentina-unvenerable-lorita.ngrok-free.dev/"

# Vehicles you want QR codes for
vehicles = [
    "CAR001",
    "CAR002",
    "CAR003",
    "CAR004",
    "CAR006",
    "CAR007",
    "CAR008",
    "CAR009"
]

# Create folder for QR codes
output_folder = "qr_codes"
os.makedirs(output_folder, exist_ok=True)

for vehicle in vehicles:

    # URL that QR will open
    url = f"{BASE_URL}/vehicle/{vehicle}"

    # Generate QR
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )

    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")

    # Save QR
    filename = f"{output_folder}/{vehicle}_QR.png"
    img.save(filename)

    print(f"✅ QR generated for {vehicle}")
    print(f"   → {url}")
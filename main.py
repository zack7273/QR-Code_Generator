import qrcode

# Get the URL to be encoded
url = "https://www.google.com/"

# Create a QRCode object
qr = qrcode.QRCode()

# Add the URL to the QRCode object
qr.add_data(url)

# Generate the QRCode image
img = qr.make_image()

# Save the QRCode image
img.save("qr_code.png")

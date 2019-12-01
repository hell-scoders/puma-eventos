import qrcode
from PIL import Image
from pyzbar.pyzbar import decode
#Send img to the mail/save it maybe?.
qr=qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
        )
        
qr.add_data("Matame matame matame matame matame")
qr.make(fit=True)
img=qr.make_image()
img.save("hell.jpg")
#Reads and decodes qr.
data=decode(Image.open("hell.jpg"))
print(data[0].data)

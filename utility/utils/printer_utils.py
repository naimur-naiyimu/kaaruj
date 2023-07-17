from zebra import Zebra
from zplgrf import GRF

path_image = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\bar3.png"
def convert_zpl(image_path):
    with open(image_path, 'rb') as img:
        grf = GRF.from_image(img.read(), 'LABEL')
        grf.optimise_barcodes()
        zpl_code = grf.to_zpl()
    # return f"^XA{str(zpl_code)}"
    main_str = str(zpl_code).replace("FO0,0","FO60,30")
    return f"^XA{main_str}"

def print_barcode(image_path):
    z = Zebra()
    Q = z.getqueues()
    z.setqueue(Q[0])
    label = convert_zpl(path_image)
    z.output(label)



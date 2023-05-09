from PIL import Image
import os.path as op

def convert_image(file):
    """
    file = (uuid, name, srctype, targettype)
    """
    image = Image.open(f'uploads/{file[1]}', 'r')
    if image.mode != "RGBA" and file[3].lower() == "png":
        image = image.convert("RGBA")

    output_filename = op.splitext(file[1])[0]+'.'+file[3].lower()

    image.save(f'converted/{output_filename}', file[3].lower())

    print(f"Image converted and saved as {output_filename}")

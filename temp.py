from PIL import Image
import os.path as op

def convert_image(file):
    """
    file = (uuid, name, srctype, targettype)
    """
    image = Image.open(f'Test Data/ImageData/{file[1]}', 'r')
    if image.mode != "RGBA" and file[3].lower() == "png":
        image = image.convert("RGBA")
    if image.mode != "RGB" and file[3].lower() == "jpg":
        image = image.convert("RGB")
    

    output_filename = op.splitext(file[1])[0]+'.'+file[3].lower()

    image.save(f'converted/{output_filename}')

    print(f"Image converted and saved as {output_filename}")


file = ('dedd','leaves_oak_carried.tga','jpg','png')
convert_image(file)

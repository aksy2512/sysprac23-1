from PIL import Image

def convert_image(file):
    image = Image.open(f'uploads/{file[1]}', 'r')
    if image.mode != "RGBA" and file[3].lower() == "png":
        image = image.convert("RGBA")

    output_filename = f"{file[1].split('.')[0]}.{file[3].lower()}"

    image.save(f'converted/{output_filename}', file[3].lower())

    print(f"Image converted and saved as {output_filename}")

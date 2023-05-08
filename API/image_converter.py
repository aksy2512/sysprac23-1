from PIL import Image

def convert_image(input_filename, to_format):
    image = Image.open(input_filename)
    if image.mode != "RGBA" and to_format == "png":
        image = image.convert("RGBA")

    output_filename = f"{input_filename.split('.')[0]}.{to_format}"

    image.save(output_filename, to_format)

    print(f"Image converted and saved as {output_filename}")

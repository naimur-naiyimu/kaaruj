from PIL import Image, ImageDraw, ImageFont
from django.conf import settings
import uuid,os
from coreapp.helper import print_log
def insert_text(image_path, text, output_path, size, add_x=0, position_y=0,color=0):
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    font_size = size
    font_path = rf"{settings.MEDIA_ROOT}/bar_codes/base/font/arial.ttf"
    font = ImageFont.truetype(font_path, font_size)
    image_width, image_height = image.size
    print(image_width, image_height)
    text_width, text_height = draw.textsize(text, font=font)
    position_x = (image_width - text_width) / 2 + add_x
    position = (position_x, position_y)
    text_color = color
    draw.text(position, text, font=font, fill=text_color)
    image.save(output_path)

    return image

def insert_image(image_path, inserted_image_path, output_path, position_y):
    background_image = Image.open(image_path)
    inserted_image = Image.open(inserted_image_path)

    # Calculate the position to insert the image at the center along the X-axis
    position_x = (background_image.width - inserted_image.width) // 2
    position = (position_x, position_y)

    # Paste the inserted image onto the background image at the calculated position
    background_image.paste(inserted_image, position)

    # Save the modified image
    background_image.save(output_path)
    return background_image

# Example usage
image_path = rf"{settings.MEDIA_ROOT}/bar_codes/base/white.png"
output_path = rf"{settings.MEDIA_ROOT}/bar_codes/base/out/out.png"

print_log("test_path" + image_path + " " + output_path)
# image_path = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\white.png"
# output_path = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\out\out.png"
def resize_image_barcode(input_image_path, output_image_path, new_height, new_width):
    image = Image.open(input_image_path)
    width, height = image.size
    aspect_ratio = float(width) / float(height)
    new_width = int(aspect_ratio * new_height)
    resized_image = image.resize((new_width, new_height))
    resized_image.save(output_image_path)


def add_images_and_text(price,product_name,sku,generated_barcode_path):
    try:
        text = price
        text2 = product_name[:24]
        text3 = sku
        # insert_position = (10, 120)  # Position to insert the image
        modified_image = insert_text(image_path, text, output_path, size=30, add_x=0, position_y=2,color='white')
        modified_image = insert_text(output_path, text2, output_path, size=30, add_x=0, position_y=60)
        modified_image = insert_text(output_path, text3, output_path, size=30, add_x=0, position_y=210)
        insert_image(output_path, generated_barcode_path, generated_barcode_path, 110)
        resize_image_barcode(generated_barcode_path, generated_barcode_path, 200, 180)
        return modified_image
    except Exception as e:
        import traceback
        from coreapp.helper import print_log
        error_text = f"Error in generate_product_barcode:  \n {traceback.format_exc()}"
        print_log(error_text)
# add_images_and_text(text,text2,text3,inserted_image_path)

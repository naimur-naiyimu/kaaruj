from PIL import Image, ImageDraw, ImageFont

def insert_text(image_path, text, output_path,add_position_x,position_y):
    # Open the image
    image = Image.open(image_path)
    
    # Create a drawing object
    draw = ImageDraw.Draw(image)
    
    # Define the font size and font type
    font_size = 50
    font = ImageFont.truetype("arial.ttf", font_size)
    
    # Get the dimensions of the image
    image_width, image_height = image.size
    
    # Get the dimensions of the text
    text_width, text_height = draw.textsize(text, font=font)
    
    # Determine the position to place the text (center horizontally, top vertically)
    position_x = (image_width - text_width) / 2 + add_position_x
    position = (position_x, position_y)
    
    # Set the text color
    text_color = 0  # Black color
    
    # Insert the text onto the image
    draw.text(position, text, font=font, fill=text_color)
    
    # Save the modified image
    image.save(output_path)

def add_image_after_text(base_image_path, overlay_image_path,  output_path):
    product_price = "250 BDT"
    product_name = "Indian Dhuti Smart"
    # Insert text onto the base image
    insert_text(base_image_path, product_price, output_path,0,20)
    insert_text(base_image_path, product_name, output_path,20,50)

    # Open the resulting image with the text
    image_with_text = Image.open(output_path)

    # Open the overlay image
    overlay_image = Image.open(overlay_image_path)

    # Calculate the position to paste the overlay image (after the text)
    position = (0, 100)

    # Create a new image by compositing the image with text and overlay image
    new_image = Image.new("RGB", (image_with_text.width, image_with_text.height + overlay_image.height))
    new_image.paste(image_with_text, (0, 0))
    new_image.paste(overlay_image, position)

    # Open the base image
    base_image = Image.open(base_image_path)

    # Calculate the position to insert the new image (after the text)
    insert_position = (0, 0)

    # Create the final image by compositing the base image and the new image with text and overlay
    final_image = Image.new("RGB", (base_image.width, base_image.height + new_image.height))
    final_image.paste(base_image, (0, 0))
    final_image.paste(new_image, insert_position)

    # Save the resulting image
    final_image.save(output_path)


# Example usage
base_image_path = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\white.png"
overlay_image_path = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\bar.png"
# image_path = "img/white.png"
output_path = r"H:\DevStream\Kaaruj_ecom\utility\utils\img\out\out.png"

# insert_text(image_path, text, output_path)
add_image_after_text(base_image_path, overlay_image_path, output_path)
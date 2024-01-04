from PIL import Image, ImageDraw
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

def generate_image(width=400, height=400, num_shapes=random.randint(5, 10)):
    # Create a white image
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)

    for _ in range(num_shapes):
        # Randomly choose a shape (circle, rectangle, or polygon)
        shape_type = random.choice([ "rectangle"])

        if shape_type == "circle":
            # Generate a random circle
            radius = random.randint(10, 50)
            center = (random.randint(radius, width - radius), random.randint(radius, height - radius))
            draw.ellipse([(center[0] - radius, center[1] - radius),
                          (center[0] + radius, center[1] + radius)], fill=0)

        elif shape_type == "rectangle":
            # Generate a random rectangle
            size = (random.randint(10, width / 10), random.randint(10, height / 10))
            top_left = (random.randint(0, width - size[0]), random.randint(0, height - size[1]))
            bottom_right = (top_left[0] + size[0], top_left[1] + size[1])
            draw.rectangle([top_left, bottom_right], fill=0)

        # elif shape_type == "polygon":
        #     # Generate a random polygon
        #     num_vertices = random.randint(3, 5)
        #     vertices = [(random.randint(0, width), random.randint(0, height)) for _ in range(num_vertices)]
        #     draw.polygon(vertices, outline=0, fill=0)

    

    directory = "generated_images"
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)
    base_filename = "generated_image"
    # Find the next available filename
    i = 1
    filename = f"{base_filename}_{i}.png"
    while os.path.exists(os.path.join(directory, filename)):
        i += 1
        filename = f"{base_filename}_{i}.png"

    # Save the image to the directory with the numbered filename
    save_path = os.path.join(directory, filename)

    # Save the image to a file
    img.save(save_path)
    return save_path


    

if __name__ == "__main__":
    generated_image = generate_image(width=1000, height=1000, num_shapes=50)


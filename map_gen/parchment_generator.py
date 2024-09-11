from PIL import Image, ImageDraw, ImageFilter
import numpy as np

# Function to generate parchment texture
def generate_parchment_texture(base_color, width=3840, height=2160):
    # Create a new image with the base color
    img = Image.new('RGB', (width, height), base_color)
    draw = ImageDraw.Draw(img)

    # Add noise to the image
    noise = np.random.normal(0, 25, (height, width, 3))
    noise = noise.astype(np.uint8)
    noise_img = Image.fromarray(noise, 'RGB')
    img = Image.blend(img, noise_img, alpha=0.2)

    # Apply a blur filter to soften the noise
    img = img.filter(ImageFilter.GaussianBlur(2))

    # Add some random darker spots to simulate aging and burning
    for _ in range(2000):
        x = np.random.randint(0, width)
        y = np.random.randint(0, height)
        radius = np.random.randint(1, 20)
        color = (np.random.randint(50, 100), np.random.randint(30, 60), np.random.randint(10, 30), 100)
        draw.ellipse((x-radius, y-radius, x+radius, y+radius), fill=color)

    # Apply another blur to blend the spots
    img = img.filter(ImageFilter.GaussianBlur(1))

    # Save the image
    img.save('parchment_texture.png')

# Example usage
base_color = (210, 180, 140)  # Tan color
generate_parchment_texture(base_color)

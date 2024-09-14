import torch
from diffusers import StableDiffusionPipeline
from moviepy.editor import ImageSequenceClip
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the pipeline components once
model_id = "CompVis/stable-diffusion-v1-4"
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16 if device == "cuda" else torch.float32)
pipe = pipe.to(device)

def generate_images_from_text(text, num_images=10):
    image_paths = []rrr33333333333
    for i in range(num_images):
        image = pipe(text).images[0]
        image_path = f'frame_{i}.png'
        image.save(image_path)
        image_paths.append(image_path)
    return image_paths

def create_video_from_images(image_paths, output_video_path, fps=1):
    if not image_paths:
        print("No images to create a video.")
        return

    clip = ImageSequenceClip(image_paths, fps=fps)
    clip.write_videofile(output_video_path, codec='libx264')

@app.route('/generate-video', methods=['POST'])
def generate_video():
    data = request.json
    text = data.get('text')
    num_images = data.get('num_images', 10)
    fps = data.get('fps', 1)
    output_video_path = './output.mp4'

    image_paths = generate_images_from_text(text, num_images)
    create_video_from_images(image_paths, output_video_path)

    return jsonify({'output_video_path': output_video_path})

@app.route('/generate-images', methods=['POST'])
def generate_images():
    data = request.json
    text = data.get('text')
    num_images = data.get('num_images', 10)

    image_paths = generate_images_from_text(text, num_images)

    return jsonify({'image_paths': image_paths})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

# Generated by Copilot
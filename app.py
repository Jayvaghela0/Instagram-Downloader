from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from diffusers import StableDiffusionPipeline
import torch

app = Flask(__name__)
CORS(app)

# Stable Diffusion मॉडल लोड करें
model_id = "stabilityai/stable-diffusion-2"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe = pipe.to("cuda" if torch.cuda.is_available() else "cpu")

@app.route("/")
def home():
    return "Flask App is Running!"
    
@app.route('/generate', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get('prompt', '')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        with torch.autocast("cuda" if torch.cuda.is_available() else "cpu"):
            image = pipe(prompt).images[0]
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    image_path = "generated_image.png"
    image.save(image_path)

    return jsonify({"image_url": f"https://your-project-name.up.railway.app/images/{image_path}"})

@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('.', filename)

if __name__ == '__main__':
    app.run(debug=True)

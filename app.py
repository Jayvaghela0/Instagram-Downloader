from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS  # CORS को इम्पोर्ट करें
from diffusers import StableDiffusionPipeline  # Hugging Face Diffusers लाइब्रेरी
import torch  # PyTorch लाइब्रेरी

# Flask ऐप इनिशियलाइज़ करें
app = Flask(__name__)
CORS(app)  # CORS को एनेबल करें

# Stable Diffusion मॉडल लोड करें
model_id = "stabilityai/stable-diffusion-2"  # मॉडल का नाम
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)

# मॉडल को GPU पर लोड करें (यदि उपलब्ध हो)
device = "cuda" if torch.cuda.is_available() else "cpu"
pipe = pipe.to(device)

# इमेज जेनरेट करने के लिए API एंडपॉइंट
@app.route('/generate', methods=['POST'])
def generate_image():
    # यूजर का टेक्स्ट इनपुट लें
    data = request.json
    prompt = data.get('prompt', '')

    # यदि टेक्स्ट इनपुट खाली है, तो एरर रिटर्न करें
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    # इमेज जेनरेट करें
    try:
        with torch.autocast(device):  # GPU/CPU के लिए ऑटोकास्ट
            image = pipe(prompt).images[0]  # इमेज जेनरेट करें
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    # इमेज को सेव करें
    image_path = "generated_image.png"
    image.save(image_path)

    # इमेज का URL रिटर्न करें
    return jsonify({"image_url": f"http://127.0.0.1:5000/images/{image_path}"})

# इमेज को सर्व करने के लिए एंडपॉइंट
@app.route('/images/<path:filename>')
def serve_image(filename):
    return send_from_directory('.', filename)

# ऐप को रन करें
if __name__ == '__main__':
    app.run(debug=True)

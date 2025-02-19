# app.py

from flask import Flask, request, render_template
import requests

app = Flask(__name__)

# Home route for rendering frontend
@app.route('/')
def home():
    return render_template('index.html')  # Your Blogger frontend here

# Route for downloading Instagram Reel
@app.route('/download', methods=['POST'])
def download():
    url = request.form.get('url')
    
    if url:
        # Here you would add the logic to download the video using the URL.
        # For demonstration, let's return a success message with the URL.
        return f"Processing your request for: {url}"

    return 'Please provide a valid URL.'

if __name__ == '__main__':
    app.run(debug=True)

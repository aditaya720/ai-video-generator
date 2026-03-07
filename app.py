import os
from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import urllib.parse

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    # Serve the main HTML file
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt", "")

    # Agar prompt khali ho toh error return karega
    if not prompt:
        return jsonify({"error": "no prompt"}), 400

    # Prompt ko URL format me encode karna
    prompt_encoded = urllib.parse.quote(prompt)
    
    # YAHAN CHANGE KIYA GAYA HAI:
    # width=768 aur height=1024 add kiya gaya hai taaki image lambi bane (Portrait mode)
    # nologo=true se image par watermark nahi aayega
    url = f"https://image.pollinations.ai/prompt/{prompt_encoded}?width=768&height=1024&nologo=true"

    try:
        # API ko call karna aur 60 seconds ka timeout set karna
        response = requests.get(url, timeout=60)
        
        # Agar API error de toh catch karega
        response.raise_for_status() 

        # Image ko base64 me convert karna
        image_base64 = base64.b64encode(response.content).decode("utf-8")

        # Frontend ko base64 image bhejna
        return jsonify({
            "image": "data:image/png;base64," + image_base64
        })

    except requests.exceptions.RequestException as e:
        print(f"API Error: {e}")
        return jsonify({"error": "Image generation failed due to API timeout or error"}), 500
        
    except Exception as e:
        print(f"Server Error: {e}")
        return jsonify({"error": "An unexpected server error occurred"}), 500

if __name__ == "__main__":
    # Render dynamic port assign karta hai
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

from flask import Flask, request, jsonify, send_from_directory
import requests
from PIL import Image
from io import BytesIO
import urllib.parse

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()
    prompt = data.get("prompt", "")

    # encode prompt
    prompt_encoded = urllib.parse.quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"

    try:
        response = requests.get(url, timeout=30)

        if response.status_code != 200:
            return jsonify({"error": "AI server error"})

        img = Image.open(BytesIO(response.content))
        img.save("output.png")

        return jsonify({"image": "/output.png"})

    except Exception as e:
        return jsonify({"error": str(e)})


@app.route("/output.png")
def get_image():
    return send_from_directory(".", "output.png")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

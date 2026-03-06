from flask import Flask, request, jsonify, send_from_directory
import requests
from PIL import Image
from io import BytesIO

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():

    prompt = request.json["prompt"]

    url = f"https://image.pollinations.ai/prompt/{prompt}"
    response = requests.get(url)

    img = Image.open(BytesIO(response.content))
    img.save("output.png")

    return jsonify({"image": "output.png"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

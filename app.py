from flask import Flask, request, jsonify, send_from_directory
import requests
import base64
import urllib.parse

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()
    prompt = data.get("prompt","")

    if prompt == "":
        return jsonify({"error":"no prompt"})

    prompt_encoded = urllib.parse.quote(prompt)

    url = f"https://image.pollinations.ai/prompt/{prompt_encoded}"

    response = requests.get(url)

    image_base64 = base64.b64encode(response.content).decode("utf-8")

    return jsonify({
        "image": "data:image/png;base64," + image_base64
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

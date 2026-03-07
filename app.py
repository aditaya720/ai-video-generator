from flask import Flask, request, jsonify, send_from_directory
import urllib.parse

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():

    data = request.get_json()
    prompt = data.get("prompt", "")

    if prompt == "":
        return jsonify({"error": "No prompt"})

    prompt_encoded = urllib.parse.quote(prompt)

    image_url = "https://image.pollinations.ai/prompt/" + prompt_encoded

    return jsonify({
        "image": image_url
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

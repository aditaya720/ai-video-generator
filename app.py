from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "AI Video Generator Running"

@app.route("/generate", methods=["POST"])
def generate():

    prompt = request.json["prompt"]

    result = "Video generated for: " + prompt

    return jsonify({"result": result})

app.run(host="0.0.0.0", port=5000)

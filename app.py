from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__, static_folder=".")

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

@app.route("/generate", methods=["POST"])
def generate():

    prompt = request.json["prompt"]

    result = "Video generated for: " + prompt

    return jsonify({"video": "", "result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

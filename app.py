from flask import Flask, render_template, request, send_file
import whisper
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = whisper.load_model("base")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    if request.method == "POST":
        if "video" not in request.files:
            return "No file part", 400
        file = request.files["video"]
        if file.filename == "":
            return "No selected file", 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        result = model.transcribe(filepath, task="translate")  # ترجمة إلى الإنجليزية
        transcript = result["text"]

    return render_template("index.html", transcript=transcript)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
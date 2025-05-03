from flask import Flask, render_template, request
import whisper
import os
import requests
from werkzeug.utils import secure_filename

app = Flask(__name__)
model = whisper.load_model("tiny")

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

GOOGLE_API_KEY = "AIzaSyBQ7uFp3SOhzIYQHQRe3bTULVr2JwQSKWw"
TARGET_LANGUAGE = "ar"

def translate_text(text, target_lang="ar"):
    url = "https://translation.googleapis.com/language/translate/v2"
    params = {
        "q": text,
        "target": target_lang,
        "key": GOOGLE_API_KEY
    }
    response = requests.post(url, data=params)
    print("Google Translate API Response:", response.text)  # Debug print
    if response.status_code == 200:
        try:
            return response.json()["data"]["translations"][0]["translatedText"]
        except Exception as e:
            return f"خطأ في قراءة الترجمة: {e}"
    else:
        return "خطأ في الاتصال بترجمة Google"

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    translated_text = ""
    if request.method == "POST":
        if "video" not in request.files:
            return "لم يتم تحميل ملف", 400
        file = request.files["video"]
        if file.filename == "":
            return "لم يتم اختيار ملف", 400
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        result = model.transcribe(filepath)
        transcript = result["text"]
        translated_text = translate_text(transcript, TARGET_LANGUAGE)

    return render_template("index.html", transcript=translated_text)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
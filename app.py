import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename

from pdf_reader import get_pdf_info
from config_loader import load_config
from region_text_extractor import extract_text_from_regions
from region_translator import translate_regions
from pdf_modifier import apply_translations_to_pdf


# -----------------------------
# App setup
# -----------------------------
app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
ALLOWED_EXTENSIONS = {"pdf"}


# -----------------------------
# Utility functions
# -----------------------------
def ensure_upload_folder():
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# -----------------------------
# Health check
# -----------------------------
@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "PDF Translation Service is running"})


# -----------------------------
# Verify PDF (stateless)
# -----------------------------
@app.route("/verify-pdf", methods=["POST"])
def verify_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "Only PDF files allowed"}), 400

    ensure_upload_folder()

    input_path = os.path.join(UPLOAD_FOLDER, "verify_input.pdf")
    file.save(input_path)

    info = get_pdf_info(input_path)

    return jsonify({
        "page_count": info.get("page_count"),
        "is_encrypted": info.get("is_encrypted")
    })


# -----------------------------
# Translate PDF (MAIN ENDPOINT)
# -----------------------------
@app.route("/translate-pdf", methods=["POST"])
def translate_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "Empty filename"}), 400

        if not allowed_file(file.filename):
            return jsonify({"error": "Only PDF files allowed"}), 400

        ensure_upload_folder()

        input_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
        output_path = os.path.join(UPLOAD_FOLDER, "output.pdf")

        # Save uploaded PDF
        file.save(input_path)

        # Load configuration
        config = load_config()
        if not isinstance(config, dict):
            return jsonify({"error": "Invalid config file"}), 500

        regions = config.get("all_pages", [])

        # Extract text
        extracted = extract_text_from_regions(input_path, regions)
        if not extracted:
            return jsonify({"error": "Text extraction failed"}), 500

        # Translate text
        translated = translate_regions(extracted)
        if not translated:
            return jsonify({"error": "Translation failed"}), 500

        # Apply translations to PDF
        apply_translations_to_pdf(
            input_pdf_path=input_path,
            output_pdf_path=output_path,
            translated_regions=translated
        )

        if not os.path.exists(output_path):
            return jsonify({"error": "Output PDF not generated"}), 500

        return send_file(
            output_path,
            as_attachment=True,
            download_name="translated_bill.pdf",
            mimetype="application/pdf"
        )

    except Exception as e:
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


# -----------------------------
# Entry point (Render + Local)
# -----------------------------
if __name__ == "__main__":
    ensure_upload_folder()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    # For local development, use:   
    
import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from pdf_reader import get_pdf_info
from config_loader import load_config
from region_text_extractor import extract_text_from_regions
from region_translator import translate_regions
from pdf_modifier import apply_translations_to_pdf



app = Flask(__name__)
CORS(app)

UPLOAD_FOLDER = "uploads"
def clear_uploads_folder():
    for filename in os.listdir(UPLOAD_FOLDER):
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

@app.route("/")
def index():
    return "PDF Upload Service is running."

@app.route("/upload", methods=["POST"])
def upload_pdf():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Empty filename"}), 400

    clear_uploads_folder()

    save_path = os.path.join(UPLOAD_FOLDER, "input.pdf")
    file.save(save_path)

    return jsonify({
        "message": "PDF uploaded successfully",
        "file_path": save_path
    })


@app.route("/verify-pdf", methods=["GET"])
def verify_pdf():
    pdf_path = "uploads/input.pdf"

    if not os.path.exists(pdf_path):
        return jsonify({"error": "No PDF found"}), 404

    info = get_pdf_info(pdf_path)

    return jsonify({
        "message": "PDF verified successfully",
        "page_count": info["page_count"],
        "is_encrypted": info["is_encrypted"]
    })

@app.route("/extract-regions", methods=["GET"])
def extract_regions():
    pdf_path = "uploads/input.pdf"

    if not os.path.exists(pdf_path):
        return jsonify({"error": "No PDF uploaded"}), 404

    config = load_config()
    regions = config.get("all_pages", [])

    extracted = extract_text_from_regions(pdf_path, regions)

    return jsonify({
        "message": "Region-based extraction successful",
        "regions": extracted
    })


@app.route("/translate-regions", methods=["GET"])
def translate_regions_api():
    pdf_path = "uploads/input.pdf"

    if not os.path.exists(pdf_path):
        return jsonify({"error": "No PDF uploaded"}), 404

    config = load_config()
    regions = config.get("all_pages", [])

    extracted = extract_text_from_regions(pdf_path, regions)
    translated = translate_regions(extracted)

    return jsonify({
        "message": "Region translation successful",
        "data": translated
    })

@app.route("/translate-pdf", methods=["POST"])
def translate_pdf():
    pdf_path = "uploads/input.pdf"
    output_path = "uploads/output.pdf"

    if not os.path.exists(pdf_path):
        return jsonify({"error": "No PDF uploaded"}), 404

    config = load_config()
    regions = config.get("all_pages", [])

    extracted = extract_text_from_regions(pdf_path, regions)
    translated = translate_regions(extracted)

    apply_translations_to_pdf(
        input_pdf_path=pdf_path,
        output_pdf_path=output_path,
        translated_regions=translated
    )

    return send_file(
        output_path,
        as_attachment=True,
        download_name="translated_bill.pdf"
    )


if __name__ == "__main__":
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

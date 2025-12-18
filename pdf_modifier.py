import fitz  # PyMuPDF
import os

# ---- FONT CONFIG (LOCKED) ----
FONT_NAME = "NotoSansDevanagari"
FONT_PATH = "fonts/NotoSansDevanagari-Regular.ttf"

# Safety check (fail fast if font missing)
if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Hindi font not found at {FONT_PATH}")


def pad_bbox(bbox, padding_top=2, padding_bottom=14):
    """
    Expands the bounding box vertically to accommodate Hindi (Devanagari)
    characters which require more vertical space.
    """
    x0, y0, x1, y1 = bbox
    return (x0, y0 - padding_top, x1, y1 + padding_bottom)


def apply_translations_to_pdf(
    input_pdf_path,
    output_pdf_path,
    translated_regions
):
    """
    Applies Hindi translations to the PDF by:
    1. Covering original English text with a white rectangle
    2. Writing Hindi text inside the same (padded) region
    """

    doc = fitz.open(input_pdf_path)

    for page in doc:
        page_index = page.number

        for region in translated_regions:
            if region["page"] != page_index:
                continue

            hindi_text = region.get("hindi_text", "").strip()
            if not hindi_text:
                continue

            # Original bbox from config
            original_bbox = region["rect"]

            # Pad bbox for Hindi text height
            bbox = pad_bbox(original_bbox)

            # 1. Hide English text
            page.draw_rect(
                bbox,
                fill=(1, 1, 1),
                color = None,
                overlay=True
            )

            # 2. Insert Hindi text (guaranteed fit logic)
            inserted = False
            for font_size in range(10, 5, -1):
                rc = page.insert_textbox(
                    bbox,
                    hindi_text,
                    fontsize=font_size,
                    fontname=FONT_NAME,
                    fontfile=FONT_PATH,
                    color=(0, 0, 0),
                    align=fitz.TEXT_ALIGN_CENTER
                )
                if rc >= 0:
                    inserted = True
                    break

            # Fail-safe: log if text could not be inserted
            if not inserted:
                print(
                    f"[WARN] Hindi text did not fit on page {page_index} "
                    f"for region {region.get('region_name')}"
                )

    doc.save(output_pdf_path)

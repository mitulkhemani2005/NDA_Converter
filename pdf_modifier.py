import fitz  # PyMuPDF
import os

# ================= FONT CONFIG =================
FONT_NAME = "NotoSansDevanagari"
FONT_PATH = "fonts/NotoSansDevanagari-Regular.ttf"

if not os.path.exists(FONT_PATH):
    raise FileNotFoundError(f"Hindi font not found at {FONT_PATH}")


# ================= BBOX UTILS =================
def pad_bbox(bbox, padding_top=2, padding_bottom=14):
    """
    Padding ONLY for Hindi text height.
    Overlay rectangle must NEVER use padded bbox.
    """
    x0, y0, x1, y1 = bbox
    return (x0, y0 - padding_top, x1, y1 + padding_bottom)


# ================= TEXT INSERT =================
def insert_centered_text(page, bbox, text):
    """
    Inserts Hindi text exactly once, centered horizontally and vertically.
    Uses Shape for dry-run measurement to avoid duplicate rendering.
    """

    x0, y0, x1, y1 = bbox

    fitted_font_size = None
    unused_space = None

    # -------- Pass 1: Measure using Shape (NO DRAW) --------
    for font_size in range(10, 5, -1):
        shape = page.new_shape()
        rc = shape.insert_textbox(
            bbox,
            text,
            fontsize=font_size,
            fontname=FONT_NAME,
            fontfile=FONT_PATH,
            align=fitz.TEXT_ALIGN_CENTER
        )
        # DO NOT COMMIT SHAPE
        if rc >= 0:
            fitted_font_size = font_size
            unused_space = rc
            break

    if fitted_font_size is None:
        return False

    # -------- Vertical centering --------
    vertical_shift = unused_space / 2

    centered_bbox = (
        x0,
        y0 + vertical_shift,
        x1,
        y1
    )

    # -------- Pass 2: Final render (ONLY ONCE) --------
    page.insert_textbox(
        centered_bbox,
        text,
        fontsize=fitted_font_size,
        fontname=FONT_NAME,
        fontfile=FONT_PATH,
        color=(0, 0, 0),
        align=fitz.TEXT_ALIGN_CENTER
    )

    return True


# ================= MAIN MODIFIER =================
def apply_translations_to_pdf(
    input_pdf_path,
    output_pdf_path,
    translated_regions
):
    """
    FINAL RULES:
    - Overlay rectangle uses EXACT config.json coordinates
    - Hindi text is rendered ONCE and centered correctly
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

            # 1️⃣ Exact rectangle from config.json
            original_bbox = tuple(region["rect"])

            # 2️⃣ Padded bbox ONLY for Hindi text
            text_bbox = pad_bbox(original_bbox)

            # 3️⃣ Erase English text (NO BORDER)
            page.draw_rect(
                original_bbox,
                fill=(1, 1, 1),
                color=None,
                overlay=True
            )

            # 4️⃣ Insert Hindi text ONCE
            success = insert_centered_text(
                page=page,
                bbox=text_bbox,
                text=hindi_text
            )

            if not success:
                print(
                    f"[WARN] Hindi text did not fit "
                    f"(page={page_index}, region={region.get('region_name')})"
                )

    doc.save(output_pdf_path)

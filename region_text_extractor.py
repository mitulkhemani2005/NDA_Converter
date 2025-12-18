import fitz  # PyMuPDF

def extract_text_from_regions(pdf_path, regions):
    doc = fitz.open(pdf_path)
    results = []

    for page_index, page in enumerate(doc):
        page_dict = page.get_text("dict")

        for region in regions:
            x_min, y_min, x_max, y_max = region["rect"]
            collected = []

            for block in page_dict["blocks"]:
                if block["type"] != 0:
                    continue  # not text

                for line in block["lines"]:
                    for span in line["spans"]:
                        x0, y0, x1, y1 = span["bbox"]
                        text = span["text"].strip()

                        if not text:
                            continue

                        # intersection check
                        intersects = not (
                            x1 < x_min or
                            x0 > x_max or
                            y1 < y_min or
                            y0 > y_max
                        )

                        if intersects:
                            collected.append(text)

            results.append({
                "page": page_index,
                "region_name": region["name"],
                "rect": region["rect"],
                "text": " ".join(collected)
            })

    return results

from googletrans import Translator
import re

translator = Translator()

def translate_to_hindi(text):
    if not text.strip():
        return text

    # Protect numbers (invoice safety)
    protected = re.sub(
        r"\d+",
        lambda m: f"__NUM_{m.group()}__",
        text
    )

    translated = translator.translate(
        protected,
        src="en",
        dest="hi"
    ).text

    # Restore numbers
    translated = re.sub(
        r"__NUM_(\d+)__",
        r"\1",
        translated
    )

    return translated

import re

# Define terms to ignore (metadata, not lab tests)
IGNORE_KEYWORDS = [
    "AGE", "SEX", "DATE", "ADDRESS", "DOCTOR", "DR", "PLOT",
    "CONTACT", "REGD", "PREPARED", "BY", "SONU", "MAGAR", "FLOOR"
]

def extract_lab_values_dynamic(text):
    """
    Extract lab values while ignoring metadata like Age, Sex, Date, etc.
    """
    labs = {}
    t = text.upper().replace("\n", " ")

    # Match like: TEST_NAME 123.45 or TEST_NAME : 123
    matches = re.findall(r"([A-Z][A-Z\s\-]{1,50})[:\s]+([\d.,]+)", t)

    for name, val in matches:
        name = name.strip()

        # Skip ignored keywords
        if any(skip in name for skip in IGNORE_KEYWORDS):
            continue

        # Normalize test name
        name = re.sub(r"\s+", " ", name).title()

        # Parse numeric value
        val = val.replace(',', '')
        try:
            val = float(val)
        except:
            pass

        labs[name] = val

    return labs

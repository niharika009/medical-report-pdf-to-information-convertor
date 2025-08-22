import re

def extract_key_info(text):
    """
    Extract key-value info dynamically from any medical report.
    Returns a dictionary of {key: value}.
    """
    info = {}
    # Pattern: 'TestName : 123', 'TestName 123', 'TestName = 123'
    pattern = re.compile(r"([A-Za-z][A-Za-z\s/-]{1,50})[:=\s]+([\d.,]+)")

    for match in pattern.finditer(text):
        key = match.group(1).strip()
        val = match.group(2).replace(',', '')
        try:
            val = float(val)
        except:
            pass
        info[key] = val

    return info

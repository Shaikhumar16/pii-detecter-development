import re
import csv
import json

# === CONFIG ===
INPUT_DATA = [
    {"record_id": 1, "text": "Customer John Doe lives at 123 Main St, email john@example.com, phone 9876543210."},
    {"record_id": 2, "text": "Order placed by Alice with email alice.wonder@wonderland.io, phone 1234567890."},
    {"record_id": 3, "text": "This record has no sensitive info at all."}
]

OUTPUT_FILE = "redacted_output_Umar.csv"   # ✅ Fixed for Windows


# === REGEX PATTERNS ===
patterns = {
    "email": re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"),
    "phone": re.compile(r"\b\d{10}\b"),
    "address": re.compile(r"\d{1,5}\s\w+(?:\s\w+)*\s(?:St|Street|Ave|Avenue|Rd|Road|Blvd|Lane|Ln)\b", re.IGNORECASE),
    "name": re.compile(r"\b([A-Z][a-z]+ [A-Z][a-z]+)\b")
}


def detect_and_redact(text):
    redactions = {}
    is_pii = False

    for pii_type, pattern in patterns.items():
        matches = pattern.findall(text)
        if matches:
            is_pii = True
            redactions[pii_type] = matches
            # Replace with [REDACTED]
            for match in matches:
                text = text.replace(match, "[REDACTED]")

    return text, redactions, is_pii


def run_detector():
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        # REQUIRED header
        writer.writerow(["record_id", "redacted_data_json", "is_pii"])

        for record in INPUT_DATA:
            redacted_text, redactions, is_pii = detect_and_redact(record["text"])
            writer.writerow([
                record["record_id"],
                json.dumps({"original": record["text"], "redacted": redacted_text, "pii_found": redactions}),
                str(is_pii)
            ])


if __name__ == "__main__":
    run_detector()
    print(f"[+] Detection complete. Output written to {OUTPUT_FILE}")

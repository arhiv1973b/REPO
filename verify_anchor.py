# verify_anchor.py
import hashlib
import json

EXPECTED_HASH = "35c29a878a005007dec2cc5a76bc289193f8cbd9c9e4e494ee66ae41c30c1b30"
FILE_PATH = "evidence_matrix_fincombank.json"

def compute_sha256(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    # Temporarily reset hash_sha256 to placeholder used during generation
    data["evidence_matrix"]["cryptographic_anchor"]["hash_sha256"] = "PENDING_CALCULATION"
    raw = json.dumps(data, sort_keys=True, ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()

if __name__ == "__main__":
    actual_hash = compute_sha256(FILE_PATH)
    print(f"Computed SHA-256: {actual_hash}")
    if actual_hash == EXPECTED_HASH:
        print("[OK] Hash matches the anchored value.")
    else:
        print("[ALERT] Hash mismatch! File may have been altered.")

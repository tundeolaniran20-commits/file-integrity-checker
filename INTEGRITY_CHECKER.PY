#!/usr/bin/env python3
"""
File Integrity Checker
A simple tool to calculate and verify SHA256 hashes of files.
Useful for detecting unauthorized file changes.
"""

import hashlib
import os
import json
from datetime import datetime

def calculate_hash(filepath):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha256.update(chunk)
        return sha256.hexdigest()
    except Exception as e:
        return f"Error: {e}"

def create_baseline(directory, output_file="baseline.json"):
    """Create a baseline of file hashes"""
    baseline = {
        "created_at": datetime.now().isoformat(),
        "files": {}
    }

    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            file_hash = calculate_hash(filepath)
            baseline["files"][filepath] = file_hash
            print(f"[+] Hashed: {filepath}")

    with open(output_file, "w") as f:
        json.dump(baseline, f, indent=4)

    print(f"\n[✓] Baseline saved to {output_file}")

def verify_integrity(baseline_file="baseline.json"):
    """Check files against the baseline"""
    if not os.path.exists(baseline_file):
        print("[!] Baseline file not found. Create one first.")
        return

    with open(baseline_file, "r") as f:
        baseline = json.load(f)

    print(f"Checking integrity (Baseline created: {baseline['created_at']})\n")

    modified = []
    missing = []

    for filepath, old_hash in baseline["files"].items():
        if not os.path.exists(filepath):
            missing.append(filepath)
            continue

        current_hash = calculate_hash(filepath)
        if current_hash != old_hash:
            modified.append(filepath)

    if not modified and not missing:
        print("[✓] All files are intact. No changes detected.")
    else:
        if modified:
            print("[!] Modified files detected:")
            for f in modified:
                print(f"    - {f}")
        if missing:
            print("[!] Missing files:")
            for f in missing:
                print(f"    - {f}")

def main():
    print("=" * 50)
    print("     FILE INTEGRITY CHECKER")
    print("=" * 50)
    print("\n1. Create baseline")
    print("2. Verify integrity")
    print("3. Exit")

    choice = input("\nSelect an option (1-3): ").strip()

    if choice == "1":
        directory = input("Enter directory to scan (or . for current): ").strip()
        if not directory:
            directory = "."
        create_baseline(directory)
    elif choice == "2":
        verify_integrity()
    elif choice == "3":
        print("Goodbye!")
    else:
        print("Invalid option.")

if __name__ == "__main__":
    main()

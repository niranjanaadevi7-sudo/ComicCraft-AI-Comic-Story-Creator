import subprocess
import sys
import json
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def run_script(script_name):
    """Run another Python script and return its output."""

    script_path = BASE_DIR / script_name

    print("\n" + "=" * 60)
    print(f"Running: {script_name}")
    print("=" * 60)

    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=True,
        text=True,
        cwd=str(BASE_DIR)
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        if result.stderr:
            print("\nERROR:")
            print(result.stderr)
        return None

    return result.stdout


def extract_json(text):
    if not text:
        return None

    cleaned = text.replace("```json", "").replace("```", "").strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError:
        return None


def save_json(data, filename):
    output_path = BASE_DIR / filename

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)

    print(f"\nSaved: {output_path}")


def main():
    print("=" * 60)
    print("COMICCRAFT")
    print("=" * 60)

    print("\nSTEP 1: Generating comic outline...")
    outline_output = run_script("gemini_flash.py")

    if outline_output is None:
        print("Outline generation failed.")
        return

    print("\nSTEP 2: Generating story...")
    story_output = run_script("gemini_pro.py")

    if story_output is None:
        print("Story generation failed.")
        return

    print("\nCOMICCRAFT PIPELINE COMPLETED")


if __name__ == "__main__":
    main()
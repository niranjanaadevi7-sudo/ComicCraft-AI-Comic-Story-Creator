import os
import json
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# ---------------------------------------------------------
# SETUP
# ---------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    print("ERROR: GEMINI_API_KEY was not found in .env")
    raise SystemExit(1)

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-3.1-flash-image"

OUTLINE_FILE = BASE_DIR / "comic_outline.json"

IMAGE_DIR = BASE_DIR / "generated_images"
IMAGE_DIR.mkdir(exist_ok=True)


# ---------------------------------------------------------
# LOAD COMIC OUTLINE
# ---------------------------------------------------------

def load_outline():
    if not OUTLINE_FILE.exists():
        print("ERROR: comic_outline.json was not found.")
        print(f"Expected location: {OUTLINE_FILE}")
        raise SystemExit(1)

    try:
        with open(OUTLINE_FILE, "r", encoding="utf-8") as file:
            return json.load(file)

    except json.JSONDecodeError as error:
        print("ERROR: comic_outline.json contains invalid JSON.")
        print(error)
        raise SystemExit(1)


# ---------------------------------------------------------
# GENERATE ONE PANEL
# ---------------------------------------------------------

def generate_panel(panel):
    panel_number = panel.get("panel_number")
    title = panel.get("title", "Untitled")
    scene_description = panel.get("scene_description", "")
    image_prompt = panel.get("image_prompt", "")

    print("\n" + "=" * 60)
    print(f"GENERATING PANEL {panel_number}")
    print(f"Title: {title}")
    print("=" * 60)

    prompt = f"""
Create a single comic-book panel for a college adventure story.

IMPORTANT CHARACTER CONSISTENCY:
The main character is Maya, a 19-year-old college student.
She has messy brown hair, round glasses, and wears a green hoodie.
The robot is a small quirky retro-futuristic robot.

PANEL TITLE:
{title}

SCENE:
{scene_description}

IMAGE STYLE:
{image_prompt}

Make this a polished colorful modern comic-book illustration.
Use clean bold outlines, expressive characters, vibrant colors,
clear visual storytelling, and a fun college-adventure atmosphere.

Do not create multiple panels.
Create ONLY the single requested comic panel.
"""

    try:
        response = client.models.generate_content(
            model=MODEL,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_modalities=["IMAGE"],
                response_format={
                    "image": {
                        "aspect_ratio": "16:9",
                        "image_size": "1K"
                    }
                }
            )
        )

        for part in response.parts:
            if part.text is not None:
                print("Model message:", part.text)

            elif part.as_image():
                image = part.as_image()

                output_file = IMAGE_DIR / f"panel_{panel_number}.png"

                image.save(output_file)

                print("\nSUCCESS!")
                print(f"Panel saved to:")
                print(output_file)

                return True

        print("\nERROR: No image was returned by Gemini.")
        return False

    except Exception as error:
        print("\nIMAGE GENERATION FAILED")
        print(error)
        return False


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------

def main():

    print("=" * 60)
    print("COMICCRAFT")
    print("AI COMIC IMAGE GENERATION")
    print("=" * 60)

    outline = load_outline()

    panels = outline.get("panels", [])

    if not panels:
        print("ERROR: No panels found in comic_outline.json.")
        return

    print(f"\nFound {len(panels)} comic panels.")

    print("\nImages will be saved in:")
    print(IMAGE_DIR)

    successful = 0

    for panel in panels:

        success = generate_panel(panel)

        if success:
            successful += 1

        # Small pause between requests
        time.sleep(3)

    print("\n" + "=" * 60)
    print("IMAGE GENERATION COMPLETE")
    print("=" * 60)

    print(f"\nSuccessfully generated: {successful}/{len(panels)} panels")

    print(f"\nImages are located in:")
    print(IMAGE_DIR)


if __name__ == "__main__":
    main()
import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")

client = genai.Client(api_key=api_key)

MODELS = [
    "gemini-3.5-flash"
]


def generate_story(outline):

    prompt = f"""
You are a comic story writer.

Create narration, dialogue and captions for every panel
using the following comic outline.

{json.dumps(outline, indent=2)}

Rules:

1. Keep the characters consistent.
2. Follow the outline.
3. Keep narration short.
4. Make dialogue natural.
5. Keep captions short.
6. Keep exactly the same number of panels.
7. Return only valid JSON.

Return this structure:

{{
    "panels": [
        {{
            "panel_number": 1,
            "narration": "Short narration",
            "dialogue": "Character: Dialogue",
            "caption": "Short caption"
        }}
    ]
}}
"""

    expected_panels = len(outline["panels"])

    for model in MODELS:

        print()
        print("=" * 50)
        print("Trying model:", model)
        print("=" * 50)

        try:

            response = client.models.generate_content(
                model=model,
                contents=prompt,
                config={
                    "response_mime_type": "application/json",
                    "automatic_function_calling": {
                        "disable": True
                    }
                }
            )

            result = json.loads(response.text)

            if "panels" not in result:
                raise ValueError("No panels found in response.")

            if len(result["panels"]) != expected_panels:
                raise ValueError(
                    "Wrong number of panels returned."
                )

            required_fields = [
                "panel_number",
                "narration",
                "dialogue",
                "caption"
            ]

            for panel in result["panels"]:

                for field in required_fields:

                    if field not in panel:
                        raise ValueError(
                            f"Missing field: {field}"
                        )

            print()
            print("SUCCESS!")
            print("Model used:", model)

            return result

        except Exception as error:

            error_text = str(error)

            if "429" in error_text or "RESOURCE_EXHAUSTED" in error_text:

                print("Quota limit reached.")
                print("Trying next model...")

            elif "503" in error_text or "UNAVAILABLE" in error_text:

                print("Model temporarily unavailable.")
                print("Trying next model...")

            else:

                print("Model failed.")
                print("Error:", error)
                print("Trying next model...")


    raise RuntimeError(
        "All Gemini models failed. Please try again later."
    )


if __name__ == "__main__":

    test_outline = {
        "panels": [

            {
                "panel_number": 1,
                "title": "The Campus Treasure",
                "scene_description": (
                    "Maya discovers a small brass robot "
                    "behind the college science building."
                ),
                "image_prompt": (
                    "Colorful comic book style, "
                    "college student discovering a small robot."
                )
            },

            {
                "panel_number": 2,
                "title": "The Prophecy",
                "scene_description": (
                    "The robot comes to life and "
                    "shows Maya a prediction."
                ),
                "image_prompt": (
                    "Comic book style, robot showing "
                    "a glowing holographic prediction."
                )
            },

            {
                "panel_number": 3,
                "title": "Instant Realization",
                "scene_description": (
                    "The prediction comes true."
                ),
                "image_prompt": (
                    "Comic book style, shocked student "
                    "watching the prediction happen."
                )
            },

            {
                "panel_number": 4,
                "title": "The Big Plan",
                "scene_description": (
                    "Maya decides to use the robot's "
                    "predictions to enter the science fair."
                ),
                "image_prompt": (
                    "Comic book style, student planning "
                    "a science fair project with a robot."
                )
            },

            {
                "panel_number": 5,
                "title": "Let's Make History",
                "scene_description": (
                    "Maya prepares for the science fair "
                    "with the robot."
                ),
                "image_prompt": (
                    "Comic book style, student and robot "
                    "ready for an exciting adventure."
                )
            }
        ]
    }

    try:

        result = generate_story(test_outline)

        print()
        print("=" * 50)
        print("STORY DETAILS")
        print("=" * 50)
        print()

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

        print()
        print("=" * 50)
        print("GENERATION COMPLETE")
        print("=" * 50)

    except Exception as error:

        print()
        print("=" * 50)
        print("GENERATION FAILED")
        print("=" * 50)
        print()
        print(error)
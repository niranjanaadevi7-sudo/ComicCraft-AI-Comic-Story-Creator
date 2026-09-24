import os
import json
import time

from dotenv import load_dotenv
from google import genai


# ==========================================
# LOAD API KEY
# ==========================================

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY was not found in .env")


# ==========================================
# CREATE GEMINI CLIENT
# ==========================================

client = genai.Client(api_key=api_key)


# ==========================================
# GENERATE COMIC OUTLINE
# ==========================================

def generate_outline(
    story_prompt,
    character,
    setting,
    tone,
    art_style,
    number_of_panels=5
):

    prompt = f"""
Create a {number_of_panels}-panel comic outline.

Story: {story_prompt}
Character: {character}
Setting: {setting}
Tone: {tone}
Art style: {art_style}

For every panel give:
panel_number, title, scene_description, image_prompt.

The story must have a beginning, middle, and ending.
Keep the character consistent.

Return ONLY JSON:

{{
  "panels": [
    {{
      "panel_number": 1,
      "title": "title",
      "scene_description": "description",
      "image_prompt": "prompt"
    }}
  ]
}}

Create exactly {number_of_panels} panels.
"""


    # Models to try
    models = [
        "gemini-3.5-flash",
        "gemini-3.5-flash-lite"
    ]


    for model in models:

        print()
        print("=" * 50)
        print(f"Trying model: {model}")
        print("=" * 50)


        for attempt in range(3):

            try:

                print(
                    f"Attempt {attempt + 1}/3..."
                )


                response = client.models.generate_content(

                    model=model,

                    contents=prompt,

                    config={
                        "response_mime_type": "application/json"
                    }
                )


                result = json.loads(response.text)


                # Check panels
                if "panels" not in result:

                    raise ValueError(
                        "Gemini response does not contain panels."
                    )


                # Check number of panels
                if len(result["panels"]) != number_of_panels:

                    raise ValueError(
                        f"Expected {number_of_panels} panels, "
                        f"but received {len(result['panels'])}."
                    )


                # Check required fields
                required_fields = [
                    "panel_number",
                    "title",
                    "scene_description",
                    "image_prompt"
                ]


                for panel in result["panels"]:

                    for field in required_fields:

                        if field not in panel:

                            raise ValueError(
                                f"Panel is missing field: {field}"
                            )


                print()
                print("SUCCESS!")
                print(f"Model used: {model}")
                print("Comic outline generated successfully.")


                return result


            except Exception as error:

                print()
                print(
                    f"Request failed: {error}"
                )


                # Retry
                if attempt < 2:

                    wait_time = 10 * (attempt + 1)

                    print(
                        f"Waiting {wait_time} seconds..."
                    )

                    time.sleep(wait_time)


                else:

                    print(
                        f"Model {model} failed after 3 attempts."
                    )


        print()
        print(
            f"Moving to fallback model..."
        )


    raise RuntimeError(
        "All available Gemini models failed. "
        "Please try again later."
    )


# ==========================================
# TEST THE FUNCTION
# ==========================================

if __name__ == "__main__":

    result = generate_outline(

        story_prompt=(
            "A college student discovers a robot "
            "that can predict the future."
        ),
        
            
    

        character=(
            "Maya, a curious 19-year-old "
            "college student"
           
        ),

        setting=(
            "A modern college campus"
        ),

        tone=(
            "Funny and adventurous"
        ),

        art_style=(
            "Colorful modern comic book style"
        ),

        number_of_panels=5
    )


    # ==========================================
    # DISPLAY RESULT
    # ==========================================

    print()
    print("=" * 50)
    print("COMIC OUTLINE")
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
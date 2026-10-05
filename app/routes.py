from fastapi import APIRouter
from pydantic import BaseModel
from image_generator import generate_image
import os
import json

router = APIRouter()


class ImageRequest(BaseModel):
    prompt: str


@router.get("/test-image")
def test_image():
    output_path = "static/panels/api_test.png"

    generate_image(
        "a cute cartoon robot in a colorful city, comic book style",
        output_path
    )

    return {
        "message": "Image generated successfully",
        "path": output_path
    }


@router.post("/generate")
def generate(request: ImageRequest):
    output_path = "static/panels/generated.png"

    generate_image(
        request.prompt,
        output_path
    )

    return {
        "message": "Image generated successfully",
        "path": output_path
    }


@router.post("/generate-comic/json")
def generate_comic_from_json():
    with open("comic_story.json", "r", encoding="utf-8") as file:
        story = json.load(file)

    generated_images = []

    for panel in story["panels"]:
        panel_number = panel["panel_number"]

        prompt = (
            f"Comic book panel, colorful cartoon style, "
            f"{panel['narration']}. "
            f"{panel['dialogue']}. "
            f"{panel['caption']}."
        )

        output_path = f"static/panels/panel_{panel_number}.png"

        generate_image(prompt, output_path)

        generated_images.append(output_path)

    return {
        "message": "Comic generated successfully",
        "images": generated_images
    }
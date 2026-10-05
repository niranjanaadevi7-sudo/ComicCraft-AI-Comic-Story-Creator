from fastapi import APIRouter
from fastapi import Request
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from image_generator import generate_image
from layout_builder import build_comic_layout
from exporters import export_comic_to_pdf

import json
import os

router = APIRouter()

templates = Jinja2Templates(directory="templates")


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
def generate_comic_from_json(request: Request):

    with open("comic_story.json", "r", encoding="utf-8") as file:
        story = json.load(file)

    story_panels = []
    image_paths = []

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

        story_panels.append({
            "panel": panel_number,
            "title": panel["caption"],
            "scene_description": panel["narration"],
            "narration": panel["narration"],
            "dialogue": panel["dialogue"]
        })

        image_paths.append(
            f"/static/panels/panel_{panel_number}.png"
        )

    comic = build_comic_layout(
        story_panels,
        image_paths
    )

    return templates.TemplateResponse(
        request=request,
        name="comic_preview.html",
        context={
            "request": request,
            "comic": comic
        }
    )


@router.get("/export")
def export_pdf():

    with open("comic_story.json", "r", encoding="utf-8") as file:
        story = json.load(file)

    story_panels = []
    image_paths = []

    for panel in story["panels"]:

        panel_number = panel["panel_number"]

        story_panels.append({
            "panel": panel_number,
            "title": panel["caption"],
            "scene_description": panel["narration"],
            "narration": panel["narration"],
            "dialogue": panel["dialogue"]
        })

        image_paths.append(
            f"static/panels/panel_{panel_number}.png"
        )

    comic_layout = build_comic_layout(
        story_panels,
        image_paths
    )

    output_path = "static/exports/comic.pdf"

    os.makedirs("static/exports", exist_ok=True)

    export_comic_to_pdf(
        comic_layout,
        output_path
    )

    return {
        "message": "PDF exported successfully!",
        "path": output_path
    }

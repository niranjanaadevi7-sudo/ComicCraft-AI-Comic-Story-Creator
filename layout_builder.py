def build_comic_layout(story_panels, image_paths):
    """
    Combines story information with generated images
    to create the final comic layout.
    """

    comic_layout = []

    for i, panel in enumerate(story_panels):

        comic_panel = {
            "panel": panel.get("panel", i + 1),
            "title": panel.get("title", ""),
            "image": image_paths[i],
            "scene_description": panel.get("scene_description", ""),
            "narration": panel.get("narration", ""),
            "dialogue": panel.get("dialogue", "")
        }

        comic_layout.append(comic_panel)

    return comic_layout

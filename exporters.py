from fpdf import FPDF


def export_comic_to_pdf(comic_layout, output_path):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    for panel in comic_layout:
        pdf.add_page()

        pdf.set_font("Arial", "B", 18)
        pdf.cell(0, 10, f"Panel {panel['panel']}: {panel['title']}", ln=True)

        if panel["image"]:
            pdf.image(panel["image"], x=10, y=30, w=190)

        pdf.set_font("Arial", "", 12)
        pdf.ln(100)

        pdf.multi_cell(
            0,
            8,
            f"Scene: {panel['scene_description']}"
        )

        pdf.multi_cell(
            0,
            8,
            f"Narration: {panel['narration']}"
        )

        pdf.multi_cell(
            0,
            8,
            f"Dialogue: {panel['dialogue']}"
        )

    pdf.output(output_path)

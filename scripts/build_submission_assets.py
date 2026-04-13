from pathlib import Path

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt
from reportlab.pdfbase import pdfdoc
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Preformatted, SimpleDocTemplate, Spacer
import hashlib

BASE_DIR = Path(__file__).resolve().parents[1]
DOCS_DIR = BASE_DIR / "docs"
SLIDES_DIR = BASE_DIR / "slides"


def _safe_md5(*args, **kwargs):
    return hashlib.md5()


pdfdoc.md5 = _safe_md5


def markdown_to_pdf(source_path: Path, target_path: Path, title: str) -> None:
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        "BodyStyle",
        parent=styles["BodyText"],
        fontName="Helvetica",
        fontSize=10,
        leading=14,
        alignment=TA_LEFT,
        spaceAfter=6,
    )
    heading1 = ParagraphStyle(
        "Heading1Custom",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1F3A5F"),
        spaceBefore=8,
        spaceAfter=10,
    )
    heading2 = ParagraphStyle(
        "Heading2Custom",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=14,
        leading=18,
        textColor=colors.HexColor("#2D5D7B"),
        spaceBefore=6,
        spaceAfter=8,
    )
    bullet_style = ParagraphStyle(
        "BulletStyle",
        parent=body_style,
        leftIndent=12,
        bulletIndent=0,
    )
    code_style = ParagraphStyle(
        "CodeStyle",
        parent=body_style,
        fontName="Courier",
        fontSize=8.5,
        leading=11,
        backColor=colors.HexColor("#F4F6F8"),
        leftIndent=8,
        rightIndent=8,
    )

    story = [Paragraph(title, heading1), Spacer(1, 8)]
    in_code_block = False
    code_lines = []

    for raw_line in source_path.read_text().splitlines():
        line = raw_line.rstrip()
        if line.startswith("```"):
            if in_code_block:
                story.append(Preformatted("\n".join(code_lines), code_style))
                story.append(Spacer(1, 8))
                code_lines = []
                in_code_block = False
            else:
                in_code_block = True
            continue

        if in_code_block:
            code_lines.append(line)
            continue

        if not line:
            story.append(Spacer(1, 6))
            continue

        if line.startswith("# "):
            story.append(Paragraph(line[2:], heading1))
        elif line.startswith("## "):
            story.append(Paragraph(line[3:], heading2))
        elif line.startswith("### "):
            story.append(Paragraph(line[4:], heading2))
        elif line.startswith("- "):
            story.append(Paragraph(line[2:], bullet_style, bulletText="•"))
        elif line[0:2].isdigit() and line[1:3] == ". ":
            story.append(Paragraph(line[3:], bullet_style))
        else:
            story.append(Paragraph(line, body_style))

    doc = SimpleDocTemplate(
        str(target_path),
        pagesize=A4,
        topMargin=36,
        bottomMargin=36,
        leftMargin=48,
        rightMargin=48,
    )
    doc.build(story)


def build_presentation(target_path: Path) -> None:
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    dark_bg = RGBColor(28, 41, 76)
    light_bg = RGBColor(245, 246, 240)
    accent = RGBColor(249, 97, 103)
    teal = RGBColor(6, 90, 130)
    body = RGBColor(39, 44, 52)
    white = RGBColor(255, 255, 255)

    slides = [
        (
            "BookScope API",
            "Google Books ingestion, local catalog ownership, personal bookshelf workflows, explainable recommendations, and reading analytics.",
            dark_bg,
            white,
        ),
        (
            "Problem and Scope",
            "Public metadata alone does not support a user's reading workflow. BookScope stores imported book metadata locally and builds CRUD, reviews, recommendations, and analytics on top of that local database.",
            light_bg,
            body,
        ),
        (
            "Architecture",
            "The project is organized into accounts, catalog, engagement, and analytics modules. Django REST Framework handles routing, serialization, filtering, pagination, and JWT-protected endpoints.",
            light_bg,
            body,
        ),
        (
            "Data Model",
            "Core entities are Author, Genre, Book, BookshelfEntry, and Review. The model supports many-to-many links for catalog metadata and user-specific constraints for bookshelf and review ownership.",
            light_bg,
            body,
        ),
        (
            "Google Books Ingestion",
            "Metadata is fetched, normalized, and written into SQLite so the API remains database-driven. The ingestion pipeline handles authors, categories, ISBN values, publication dates, and missing fields.",
            light_bg,
            body,
        ),
        (
            "Core API Capabilities",
            "The API supports authentication, catalog browsing and management, personal bookshelf CRUD, review CRUD, and machine-readable documentation generation.",
            light_bg,
            body,
        ),
        (
            "Recommendation and Analytics",
            "Recommendations are rule-based and explainable, combining genre affinity, author affinity, external rating quality, and local popularity. Analytics expose genre popularity, reading summary, rating distribution, and top authors.",
            light_bg,
            body,
        ),
        (
            "Testing and Error Handling",
            "Automated tests cover authentication, catalog operations, engagement rules, recommendations, and analytics. API errors are returned in a structured JSON format with status code discipline.",
            light_bg,
            body,
        ),
        (
            "Version Control and Deliverables",
            "The final submission includes a public repository, README, API documentation, technical report, slides, and a declared GenAI appendix. Commit history is organized by feature groups rather than by a single final dump.",
            light_bg,
            body,
        ),
        (
            "Limitations and Next Steps",
            "SQLite is appropriate for coursework-scale delivery but not for large concurrent traffic. The current recommendation engine favors explainability over ML complexity, leaving room for future ranking improvements.",
            dark_bg,
            white,
        ),
    ]

    for index, (title, text, background, foreground) in enumerate(slides):
        slide = prs.slides.add_slide(prs.slide_layouts[6])
        slide.background.fill.solid()
        slide.background.fill.fore_color.rgb = background

        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.6), Inches(11.6), Inches(0.9))
        title_frame = title_box.text_frame
        title_frame.word_wrap = True
        title_paragraph = title_frame.paragraphs[0]
        title_paragraph.text = title
        title_paragraph.font.size = Pt(28 if index else 30)
        title_paragraph.font.bold = True
        title_paragraph.font.color.rgb = foreground

        accent_shape = slide.shapes.add_shape(
            1,
            Inches(0.8),
            Inches(1.7),
            Inches(1.3),
            Inches(0.14),
        )
        accent_shape.fill.solid()
        accent_shape.fill.fore_color.rgb = accent if index % 2 == 0 else teal
        accent_shape.line.fill.background()

        content_box = slide.shapes.add_textbox(Inches(0.95), Inches(2.05), Inches(11.3), Inches(3.9))
        content_frame = content_box.text_frame
        content_frame.word_wrap = True
        content_frame.margin_left = 0
        content_frame.margin_right = 0
        content_frame.margin_top = 0
        content_frame.margin_bottom = 0
        content_paragraph = content_frame.paragraphs[0]
        content_paragraph.alignment = PP_ALIGN.LEFT
        content_paragraph.text = text
        content_paragraph.font.size = Pt(20 if index in (0, 9) else 18)
        content_paragraph.font.color.rgb = foreground

        footer_box = slide.shapes.add_textbox(Inches(10.9), Inches(6.8), Inches(1.1), Inches(0.3))
        footer_frame = footer_box.text_frame
        footer_paragraph = footer_frame.paragraphs[0]
        footer_paragraph.alignment = PP_ALIGN.RIGHT
        footer_paragraph.text = f"{index + 1:02d}"
        footer_paragraph.font.size = Pt(10)
        footer_paragraph.font.color.rgb = foreground

    prs.save(str(target_path))


def main():
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    SLIDES_DIR.mkdir(parents=True, exist_ok=True)

    markdown_to_pdf(
        DOCS_DIR / "api_documentation.md",
        DOCS_DIR / "api_documentation.pdf",
        "BookScope API Documentation",
    )
    markdown_to_pdf(
        DOCS_DIR / "technical_report.md",
        DOCS_DIR / "technical_report.pdf",
        "BookScope API Technical Report",
    )
    markdown_to_pdf(
        DOCS_DIR / "genai_usage_appendix.md",
        DOCS_DIR / "genai_usage_appendix.pdf",
        "BookScope GenAI Usage Appendix",
    )
    build_presentation(SLIDES_DIR / "bookscope_presentation.pptx")


if __name__ == "__main__":
    main()

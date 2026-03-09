from __future__ import annotations

from pathlib import Path

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "sample_pdfs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

PDFS = {
    "01_ai_in_football_scouting.pdf": {
        "title": "AI in Football Scouting",
        "sections": [
            (
                "Overview",
                "Football scouting teams increasingly use machine learning models to rank players, compare tactical profiles, and identify recruitment opportunities across large video and event datasets. These systems reduce manual screening time but should support, not replace, human judgment.",
            ),
            (
                "Common data sources",
                "Typical scouting pipelines combine event data, tracking data, video annotations, medical history summaries, and contract information. Data quality strongly affects model reliability because small inconsistencies in player roles or competition level can distort recommendations.",
            ),
            (
                "Bias and fairness",
                "Bias can appear when historical transfer activity is used as a training target. If past decisions favored players from a narrow set of leagues, the model may reproduce that bias. A governance process should review model outputs, explain feature importance, and compare recommendations across demographic and competition groups.",
            ),
            (
                "Practical recommendation",
                "A useful scouting assistant should present a shortlist, confidence level, and the evidence behind every recommendation. Clubs should log accepted and rejected suggestions so the model can be audited and improved over time.",
            ),
        ],
    },
    "02_match_analysis_with_computer_vision.pdf": {
        "title": "Match Analysis with Computer Vision",
        "sections": [
            (
                "Overview",
                "Computer vision can detect players, the ball, and field zones from match footage. This supports automatic event tagging, off-ball movement analysis, and tactical pattern discovery.",
            ),
            (
                "Technical pipeline",
                "A practical pipeline often includes frame extraction, object detection, player tracking, camera calibration, and event classification. The combination of tracking and calibration makes it possible to estimate team shape, passing lanes, pressing triggers, and transitions.",
            ),
            (
                "Operational value",
                "Coaches benefit when the system turns raw tracking outputs into interpretable indicators such as line compactness, recovery speed, overload creation, and defensive spacing after possession loss. Analysts still need to validate unusual results because occlusions and camera angle changes can affect accuracy.",
            ),
            (
                "Deployment note",
                "For production use, teams should define latency targets, storage policies, and validation benchmarks before trusting automated insights during live analysis or pre-match preparation.",
            ),
        ],
    },
    "03_predictive_models_for_injury_prevention.pdf": {
        "title": "Predictive Models for Injury Prevention",
        "sections": [
            (
                "Overview",
                "Injury prevention models estimate risk by combining workload history, recovery metrics, prior injury patterns, match congestion, travel, and training intensity. Their goal is risk reduction rather than perfect prediction.",
            ),
            (
                "Important signals",
                "Acute-to-chronic workload ratios, sleep quality indicators, return-to-play history, and subjective wellness reports are often more useful when interpreted together. A single variable rarely explains injury risk in isolation.",
            ),
            (
                "Decision support",
                "Medical and performance teams can use model outputs to adjust training load, recovery sessions, squad rotation, and monitoring frequency. The model should highlight uncertainty so practitioners do not mistake a risk estimate for a medical diagnosis.",
            ),
            (
                "Responsible use",
                "Sensitive health-related information requires careful access controls, retention policies, and communication boundaries. Clubs should ensure that predictions are used to support athlete welfare rather than to unfairly penalize players.",
            ),
        ],
    },
    "04_responsible_ai_in_sports.pdf": {
        "title": "Responsible AI in Sports",
        "sections": [
            (
                "Overview",
                "Responsible AI in sport requires transparency, privacy protection, bias monitoring, and clear accountability for human decision-makers. The more sensitive the decision, the stronger the governance process should be.",
            ),
            (
                "Governance principles",
                "Teams should document model purpose, data provenance, performance limits, review frequency, and escalation paths when outputs conflict with expert assessment. This documentation supports trust and makes audits easier.",
            ),
            (
                "Human oversight",
                "Human oversight is essential in scouting, health, and tactical evaluation. Automated systems may summarize evidence quickly, but final decisions should remain with qualified staff who can weigh context that the model cannot observe.",
            ),
            (
                "Implementation checklist",
                "A strong implementation plan includes consent review, retention rules, fallback procedures, bias testing, and periodic retraining only when new data has been validated. Responsible deployment is an ongoing operational process, not a one-time compliance task.",
            ),
        ],
    },
}


def wrap_text(text: str, max_width: float, font_name: str, font_size: int) -> list[str]:
    words = text.split()
    lines: list[str] = []
    current = []
    for word in words:
        candidate = " ".join(current + [word])
        if stringWidth(candidate, font_name, font_size) <= max_width or not current:
            current.append(word)
        else:
            lines.append(" ".join(current))
            current = [word]
    if current:
        lines.append(" ".join(current))
    return lines


def build_pdf(filename: str, title: str, sections: list[tuple[str, str]]) -> None:
    output_path = OUT_DIR / filename
    c = canvas.Canvas(str(output_path), pagesize=A4)
    width, height = A4

    margin_x = 2.2 * cm
    top_y = height - 2.5 * cm
    bottom_y = 2.2 * cm

    c.setTitle(title)
    c.setAuthor("OpenAI - generated sample content")

    y = top_y
    c.setFont("Helvetica-Bold", 20)
    c.drawString(margin_x, y, title)
    y -= 1.0 * cm

    c.setFont("Helvetica", 10)
    subtitle = "Sample PDF included to make the DIO challenge repository runnable immediately."
    c.drawString(margin_x, y, subtitle)
    y -= 1.0 * cm

    for heading, paragraph in sections:
        if y < bottom_y + 4 * cm:
            c.showPage()
            y = top_y
        c.setFont("Helvetica-Bold", 14)
        c.drawString(margin_x, y, heading)
        y -= 0.6 * cm
        c.setFont("Helvetica", 11)
        for line in wrap_text(paragraph, width - 2 * margin_x, "Helvetica", 11):
            if y < bottom_y:
                c.showPage()
                y = top_y
                c.setFont("Helvetica", 11)
            c.drawString(margin_x, y, line)
            y -= 0.5 * cm
        y -= 0.5 * cm

    c.save()


if __name__ == "__main__":
    for filename, payload in PDFS.items():
        build_pdf(filename, payload["title"], payload["sections"])
    print(f"Created {len(PDFS)} sample PDFs in {OUT_DIR}")

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
import os

REPORT_FOLDER = "reports"
os.makedirs(REPORT_FOLDER, exist_ok=True)


def generate_report(user, result, recommendation):

    filename = f"{user['name']}_Report.pdf"
    filepath = os.path.join(REPORT_FOLDER, filename)

    document = SimpleDocTemplate(filepath)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("<b>AgriCrop AI Report</b>", styles["Title"]))
    content.append(Paragraph(f"Farmer: {user['name']}", styles["Normal"]))
    content.append(Paragraph(f"Disease: {result['disease']}", styles["Normal"]))
    content.append(Paragraph(f"Confidence: {result['confidence']}%", styles["Normal"]))
    content.append(Paragraph(f"Description: {recommendation['description']}", styles["Normal"]))
    content.append(Paragraph(f"Treatment: {recommendation['treatment']}", styles["Normal"]))
    content.append(Paragraph(f"Fertilizer: {recommendation['fertilizer']}", styles["Normal"]))
    content.append(Paragraph(f"Irrigation: {recommendation['irrigation']}", styles["Normal"]))
    content.append(Paragraph(f"Precautions: {recommendation['precautions']}", styles["Normal"]))

    document.build(content)

    return filepath
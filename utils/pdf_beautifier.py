import pdfplumber
from weasyprint import HTML

def extract_structured_html(pdf_path):
    html = "<html><head><style>"
    html += """
    body { font-family: Arial; padding: 40px; line-height: 1.6; }
    h1, h2, h3 { color: #2c3e50; }
    h1 { font-size: 26px; }
    h2 { font-size: 22px; }
    h3 { font-size: 18px; }
    p { font-size: 14px; }
    li { margin-bottom: 5px; }
    </style></head><body>
    """

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words(use_text_flow=True, keep_blank_chars=False)
            for w in words:
                size = float(w['size'])
                text = w['text'].strip()

                if size > 20:
                    html += f"<h1>{text}</h1>"
                elif size > 16:
                    html += f"<h2>{text}</h2>"
                elif size > 14:
                    html += f"<h3>{text}</h3>"
                else:
                    if text.startswith(("-", "•", "*")):
                        html += f"<ul><li>{text}</li></ul>"
                    else:
                        html += f"<p>{text}</p>"

    html += "</body></html>"
    return html

def beautify_pdf(input_pdf_path: str, output_pdf_path: str = "beautified_notes.pdf") -> str:
    html_content = extract_structured_html(input_pdf_path)
    HTML(string=html_content).write_pdf(output_pdf_path)
    return output_pdf_path

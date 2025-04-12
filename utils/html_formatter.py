import pdfkit

def html_to_pdf(html_string, output_path="styled_notes.pdf"):
    # 👇 Use the full path to wkhtmltopdf
    path_to_wkhtmltopdf = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
    config = pdfkit.configuration(wkhtmltopdf=path_to_wkhtmltopdf)

    options = {
        'page-size': 'A4',
        'encoding': "UTF-8",
        'quiet': ''
    }

    pdfkit.from_string(html_string, output_path, options=options, configuration=config)
    return output_path


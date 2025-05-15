from xhtml2pdf import pisa
import os

def export_insight_to_pdf(insight, filename='insight.pdf'):
    html = f"""
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                font-size: 14px;
            }}
            h1 {{
                color: #5a2e0d;
                font-size: 20px;
            }}
            pre {{
                background-color: #f4f4f4;
                padding: 10px;
                border: 1px solid #ccc;
                white-space: pre-wrap;
            }}
        </style>
    </head>
    <body>
        <h1>AI-Generated Insight</h1>
        <pre>{insight}</pre>
    </body>
    </html>
    """
    with open(filename, "wb") as pdf_file:
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
    return pisa_status.err == 0

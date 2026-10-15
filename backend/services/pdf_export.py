import io
import logging

try:
    from weasyprint import HTML, CSS
    WEASYPRINT_INSTALLED = True
except (ImportError, OSError, Exception):
    WEASYPRINT_INSTALLED = False

logger = logging.getLogger('ats_resume_scorer')

def generate_combined_pdf(html_docs: dict[str, str]) -> bytes:
    # 1. Try WeasyPrint if system libraries (Pango/Cairo) are present
    if WEASYPRINT_INSTALLED:
        try:
            documents = []
            for name, html_str in html_docs.items():
                doc = HTML(string=html_str).render()
                documents.append(doc)
            if documents:
                first_doc = documents[0]
                for other_doc in documents[1:]:
                    for page in other_doc.pages:
                        first_doc.pages.append(page)
                return first_doc.write_pdf()
        except Exception as exc:
            logger.warning(f"WeasyPrint rendering failed ({exc}), falling back to xhtml2pdf")
            
    # 2. Pure-Python fallback using xhtml2pdf
    try:
        from xhtml2pdf import pisa
        combined_html = '<div style="page-break-after:always;"></div>'.join(html_docs.values())
        out = io.BytesIO()
        pisa_status = pisa.CreatePDF(combined_html, dest=out)
        if pisa_status.err:
            logger.warning(f"xhtml2pdf completed with warning code: {pisa_status.err}")
        pdf_bytes = out.getvalue()
        if pdf_bytes:
            return pdf_bytes
        raise RuntimeError("xhtml2pdf produced empty output")
    except Exception as exc:
        logger.error(f"xhtml2pdf fallback rendering failed: {exc}")
        raise RuntimeError(f"PDF generation failed: {exc}")

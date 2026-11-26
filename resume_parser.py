import pymupdf


def extract_text_from_pdf(pdf_file):

    extracted_text = ""

    try:
        pdf_document = pymupdf.open(
            stream=pdf_file.read(),
            filetype="pdf"
        )

        for page in pdf_document:
            extracted_text += page.get_text() + "\n"

        pdf_document.close()

        return extracted_text

    except Exception as error:
        print("PDF Extraction Error:", error)
        return ""
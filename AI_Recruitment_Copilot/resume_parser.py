import PyPDF2
from docx import Document

def extract_text(uploaded_file):
    """
    Extracts text from PDF or DOCX resumes.
    Returns the extracted text as a string.
    """

    if uploaded_file is None:
        return ""

    filename = uploaded_file.name.lower()

    # ---------- PDF ----------
    if filename.endswith(".pdf"):
        try:
            reader = PyPDF2.PdfReader(uploaded_file)

            text = ""

            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"

            return text.strip()

        except Exception as e:
            return f"Error reading PDF: {e}"

    # ---------- DOCX ----------
    elif filename.endswith(".docx"):
        try:
            doc = Document(uploaded_file)

            text = ""

            for para in doc.paragraphs:
                text += para.text + "\n"

            return text.strip()

        except Exception as e:
            return f"Error reading DOCX: {e}"

    # ---------- Unsupported ----------
    else:
        return "Unsupported file format. Please upload a PDF or DOCX file."